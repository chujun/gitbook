# feign性能优化配置之http client超时配置
# 项目背景
开发项目先配置了Hystrix,而没有对feign的http client进行配置
# 问题
线上一个服务接口(基础服务的一个查询接口)响应时间过长,超过熔断超时时间3s,导致该接口熔断器超时，
但是却导致服务的另一个常用查询接口(查询旧机订单接口)触发熔断
# 分析
正常来说，应该不至于影响其他接口的性能，
除非请求过高资源不够，或者被慢接口拖垮，造成雪崩

项目hystrix配置信息如下
```
# Hystrix
feign.hystrix.enabled=true
hystrix.command.default.execution.isolation.thread.timeoutInMilliseconds=3000
hystrix.threadpool.default.coreSize=10
hystrix.threadpool.default.maximumSize=20
hystrix.threadpool.default.allowMaximumSizeToDivergeFromCoreSize=true
hystrix.threadpool.default.maxQueueSize=100
hystrix.threadpool.default.queueSizeRejectionThreshold=101
```

查询hystrix官网文档*How-it-Works*部分提到了
熔断器线程超时，容器线程响应系统异常超时,
然而http client线程不一定阻断，可能还在等慢接口响应(其实是没有必要等待响应了)
(那怎么验证这里的想法呢?后面验证部分有方式)
>Please note that there's no way to force the latent thread to stop work - 
the best Hystrix can do on the JVM is to throw it an InterruptedException. 
If the work wrapped by Hystrix does not respect InterruptedExceptions,
the thread in the Hystrix thread pool will continue its work, though the client already received a TimeoutException.
This behavior can saturate the Hystrix thread pool, though the load is 'correctly shed'.
Most Java HTTP client libraries do not interpret InterruptedExceptions. 
So make sure to correctly configure connection and read/write timeouts on the HTTP clients.

#解决方案
配置feign的http client超时
```
# feign
feign.httpclient.enabled=true
feign.httpclient.max-connections-per-route=200
feign.httpclient.max-connections=200
feign.client.default-to-properties=false
feign.client.config.default.connect-timeout=1000
feign.client.config.default.read-timeout=3050
```

#验证
##思路
max-connections表示线程池的最大连接数

max-connections-per-route表示一个url的最大连接数,可以通过这个属性制造场景，
##方案
假设上面设想(熔断器超时并不会打断http client的线程执行)正确,
A服务A1接口直接feign调用B服务B1接口
该B1接口具有下面特征
* 1.普通值耗时很长，sleep表示,假设20s
* 2.特殊值情况下，直接返回，耗时很短


###场景1
httpclient配置,hystrix不变
```
feign.httpclient.enabled=true
#限定为1
feign.httpclient.max-connections-per-route=1
feign.httpclient.max-connections=200
feign.client.default-to-properties=false
#不配置http client超时
#feign.client.config.default.connect-timeout=1000
#feign.client.config.default.read-timeout=3050
```
Request1(普通值)先请求,熔断器超时,
然后再Request2(特殊值)请求,因为http client唯一的线程还被阻塞在Request1的feign响应中,而不能处理Request2，
最终也导致Request2，熔断器超时

### 场景2
httpclient配置,hystrix不变
```
# feign
feign.httpclient.enabled=true
feign.httpclient.max-connections-per-route=200
feign.httpclient.max-connections=200
feign.client.default-to-properties=false
feign.client.config.default.connect-timeout=1000
feign.client.config.default.read-timeout=3050
```
仍然是Request1(普通值)先请求,熔断器超时,
然后再Request2(特殊值)请求，不同的是,这时http client该url唯一的线程已经被超时设置打断，可以为新请求工作
最终也导致Request2，所以返回成功响应

##实验
### 主要代码如下
B服务B1接口主要逻辑如下
```
    @Value("${config.mock.long.cost.millisecond:500}")
    private Integer longCostMillSecond;

    @Value("${config.open.random:false}")
    private Boolean openRandom;

    @Value("${config.random.hold:300}")
    private Integer randomHold;
    
    @Override
    public DataResponse<Boolean> testLongCost(@PathVariable("key") final String key) {
        if (StringUtils.isNotEmpty(key) && key.contains("111")) {
            return DataResponse.of(true);
        }
        Integer sleep = Objects.equals(true, openRandom) ? RandomUtil.randomInt(randomHold) + longCostMillSecond : longCostMillSecond;
        try {
            Thread.sleep(sleep);
        } catch (InterruptedException e) {
            log.error("sleep fail", e);
            // Restore interrupted state...
            Thread.currentThread().interrupt();
        }
        return DataResponse.of(true);
    }
```
apollo配置如下
```
config.mock.long.cost.millisecond = 20000
config.open.random = true
config.random.hold = 1000
```
A服务A1接口主要代码逻辑如下
```java
@Api(value = "v2/base-trade-in-orders", tags = {"以旧换新订单-新"})
@RequestMapping("v2/base-trade-in-orders")
public interface BaseTradeInOrder{
    @GetMapping(value = "/test/detail/{orderNo}")
    @ApiOperation(value = "测试订单详情")
    DataResponse<TradeInOrder> testGet(@PathVariable("orderNo") String orderNo);
}
```
```
    @Override
    public DataResponse<TradeInOrder> testGet(@PathVariable("orderNo") final String orderNo) {
        //就是feign调用B服务接口了
        intlFqlRepository.testLongCost(orderNo);
        return DataResponse.of(null);
    }
```

### 先模拟场景一
主要整体配置如下
```
# feign
feign.httpclient.enabled=true
feign.httpclient.max-connections-per-route=1
feign.httpclient.max-connections=200
feign.client.default-to-properties=false
#feign.client.config.default.connect-timeout=1000
#feign.client.config.default.read-timeout=3050
# Hystrix
feign.hystrix.enabled=true
hystrix.command.default.execution.isolation.thread.timeoutInMilliseconds=3000
hystrix.threadpool.default.coreSize=10
hystrix.threadpool.default.maximumSize=20
hystrix.threadpool.default.allowMaximumSizeToDivergeFromCoreSize=true
hystrix.threadpool.default.maxQueueSize=100
hystrix.threadpool.default.queueSizeRejectionThreshold=101
```
```bash
curl http://localhost:8080/trade-in-center/v2/base-trade-in-orders/test/detail/2000
{"code":500,"resultMessage":"系统异常：IntlFqlClient#testLongCost(String) timed-out and no fallback available."}%
立刻执行
curl http://localhost:8080/trade-in-center/v2/base-trade-in-orders/test/detail/200111000
{"code":500,"resultMessage":"系统异常：IntlFqlClient#testLongCost(String) timed-out and no fallback available."}%
```
日志信息如下
```
%accordion%第一次请求A服务日志信息%accordion%

2020-11-24 18:54:43.193 [http-nio-8080-exec-5]  INFO [trade-in-center,6a53ad034caa47b3,6a53ad034caa47b3,false] com.aihuishou.service.tic.repository.trade_in_foundation.IntlFqlRepositoryImpl - ActiveConnections:   0,IdleConnections:  10,ThreadsAwaitingConnection:   0,TotalConnections:  10
2020-11-24 18:54:46.199 [http-nio-8080-exec-5] ERROR [trade-in-center,6a53ad034caa47b3,6a53ad034caa47b3,false] com.aihuishou.common.framework.springmvc.advice.ExceptionHandlerAdvice - 当前程序进入到异常捕获器，出错的 url 为：[ http://localhost:8080/trade-in-center/v2/base-trade-in-orders/test/detail/2000 ]，出错的参数为：[ {"body-param":"","form-param":"{}"} ]
com.netflix.hystrix.exception.HystrixRuntimeException: IntlFqlClient#testLongCost(String) timed-out and no fallback available.
	at com.netflix.hystrix.AbstractCommand$22.call(AbstractCommand.java:822)
	at com.netflix.hystrix.AbstractCommand$22.call(AbstractCommand.java:807)
	at rx.internal.operators.OperatorOnErrorResumeNextViaFunction$4.onError(OperatorOnErrorResumeNextViaFunction.java:140)
	at rx.internal.operators.OnSubscribeDoOnEach$DoOnEachSubscriber.onError(OnSubscribeDoOnEach.java:87)
	at rx.internal.operators.OnSubscribeDoOnEach$DoOnEachSubscriber.onError(OnSubscribeDoOnEach.java:87)
	at com.netflix.hystrix.AbstractCommand$DeprecatedOnFallbackHookApplication$1.onError(AbstractCommand.java:1472)
	at com.netflix.hystrix.AbstractCommand$FallbackHookApplication$1.onError(AbstractCommand.java:1397)
	at rx.internal.operators.OnSubscribeDoOnEach$DoOnEachSubscriber.onError(OnSubscribeDoOnEach.java:87)
	at rx.observers.Subscribers$5.onError(Subscribers.java:230)
	at rx.internal.operators.OnSubscribeThrow.call(OnSubscribeThrow.java:44)
	at rx.internal.operators.OnSubscribeThrow.call(OnSubscribeThrow.java:28)
	at rx.Observable.unsafeSubscribe(Observable.java:10151)
	at rx.internal.operators.OnSubscribeDefer.call(OnSubscribeDefer.java:51)
	at rx.internal.operators.OnSubscribeDefer.call(OnSubscribeDefer.java:35)
	at rx.Observable.unsafeSubscribe(Observable.java:10151)
	at rx.internal.operators.OnSubscribeDoOnEach.call(OnSubscribeDoOnEach.java:41)
	at rx.internal.operators.OnSubscribeDoOnEach.call(OnSubscribeDoOnEach.java:30)
	at rx.internal.operators.OnSubscribeLift.call(OnSubscribeLift.java:48)
	at rx.internal.operators.OnSubscribeLift.call(OnSubscribeLift.java:30)
	at rx.internal.operators.OnSubscribeLift.call(OnSubscribeLift.java:48)
	at rx.internal.operators.OnSubscribeLift.call(OnSubscribeLift.java:30)
	at rx.Observable.unsafeSubscribe(Observable.java:10151)
	at rx.internal.operators.OnSubscribeDoOnEach.call(OnSubscribeDoOnEach.java:41)
	at rx.internal.operators.OnSubscribeDoOnEach.call(OnSubscribeDoOnEach.java:30)
	at rx.Observable.unsafeSubscribe(Observable.java:10151)
	at rx.internal.operators.OnSubscribeDoOnEach.call(OnSubscribeDoOnEach.java:41)
	at rx.internal.operators.OnSubscribeDoOnEach.call(OnSubscribeDoOnEach.java:30)
	at rx.internal.operators.OnSubscribeLift.call(OnSubscribeLift.java:48)
	at rx.internal.operators.OnSubscribeLift.call(OnSubscribeLift.java:30)
	at rx.Observable.unsafeSubscribe(Observable.java:10151)
	at rx.internal.operators.OnSubscribeDoOnEach.call(OnSubscribeDoOnEach.java:41)
	at rx.internal.operators.OnSubscribeDoOnEach.call(OnSubscribeDoOnEach.java:30)
	at rx.internal.operators.OnSubscribeLift.call(OnSubscribeLift.java:48)
	at rx.internal.operators.OnSubscribeLift.call(OnSubscribeLift.java:30)
	at rx.Observable.unsafeSubscribe(Observable.java:10151)
	at rx.internal.operators.OperatorOnErrorResumeNextViaFunction$4.onError(OperatorOnErrorResumeNextViaFunction.java:142)
	at rx.internal.operators.OnSubscribeDoOnEach$DoOnEachSubscriber.onError(OnSubscribeDoOnEach.java:87)
	at rx.internal.operators.OnSubscribeDoOnEach$DoOnEachSubscriber.onError(OnSubscribeDoOnEach.java:87)
	at com.netflix.hystrix.AbstractCommand$HystrixObservableTimeoutOperator$1.run(AbstractCommand.java:1142)
	at com.netflix.hystrix.strategy.concurrency.HystrixContextRunnable$1.call(HystrixContextRunnable.java:41)
	at com.netflix.hystrix.strategy.concurrency.HystrixContextRunnable$1.call(HystrixContextRunnable.java:37)
	at com.aihuishou.common.feign.hystrix.RequestContextHolderHystrixConcurrencyStrategy$WrappedCallable.call(RequestContextHolderHystrixConcurrencyStrategy.java:113)
	at org.springframework.cloud.sleuth.instrument.async.TraceCallable.call(TraceCallable.java:69)
	at com.netflix.hystrix.strategy.concurrency.HystrixContextRunnable.run(HystrixContextRunnable.java:57)
	at com.netflix.hystrix.AbstractCommand$HystrixObservableTimeoutOperator$2.tick(AbstractCommand.java:1159)
	at com.netflix.hystrix.util.HystrixTimer$1.run(HystrixTimer.java:99)
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511)
	at java.util.concurrent.FutureTask.runAndReset(FutureTask.java:308)
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.access$301(ScheduledThreadPoolExecutor.java:180)
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.run(ScheduledThreadPoolExecutor.java:294)
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
	at java.lang.Thread.run(Thread.java:748)
Caused by: java.util.concurrent.TimeoutException: null
	at com.netflix.hystrix.AbstractCommand.handleTimeoutViaFallback(AbstractCommand.java:997)
	at com.netflix.hystrix.AbstractCommand.access$500(AbstractCommand.java:60)
	at com.netflix.hystrix.AbstractCommand$12.call(AbstractCommand.java:609)
	at com.netflix.hystrix.AbstractCommand$12.call(AbstractCommand.java:601)
	at rx.internal.operators.OperatorOnErrorResumeNextViaFunction$4.onError(OperatorOnErrorResumeNextViaFunction.java:140)
	... 17 common frames omitted
2020-11-24 18:54:46.201 [http-nio-8080-exec-5]  INFO [trade-in-center,6a53ad034caa47b3,6a53ad034caa47b3,false] com.aihuishou.common.framework.logger.LoggerFilter - 
> request-time: 2020-11-24 18:54:43.190
> url: http://localhost:8080/trade-in-center/v2/base-trade-in-orders/test/detail/2000
> http-method: GET
> content-type: -
> content-length: -
> host: localhost:8080
> user-agent: curl/7.64.1
> x-forwarded-for: -
> extra-param: {"traceid":"6a53ad034caa47b3"}
> body-param: -

< response-time: 2020-11-24 18:54:46.201
< http-code: 200
< content-type: application/json;charset=UTF-8
< take-time: 3011
< response-data: {"code":500,"resultMessage":"系统异常：IntlFqlClient#testLongCost(String) timed-out and no fallback available."}

2020-11-24 18:54:46.416 [SimpleAsyncTaskExecutor-4]  INFO [trade-in-center,6abb7e0b365e61f9,6abb7e0b365e61f9,false] com.aihuishou.common.util.DingTalkUtils - 预警发送成功 -> {"markdown":{"title":"钉钉机器人预警","text":"<font face=\"微软雅黑\" color=#ff0000 size=4> 服务发生非预期异常 </font>  \r\n> ENV : null  \r\n> TRACE_ID : 6a53ad034caa47b3  \r\n> 业务环节 : /trade-in-center/v2/base-trade-in-orders/test/detail/2000  \r\n> 方法名 : GET  \r\n> 方法入参 : {\"body-param\":\"\",\"form-param\":\"{}\"}  \r\n> 额外信息 : null  \r\n> 时间 : 2020-11-24 18:54:43.190  \r\n> 异常信息 : IntlFqlClient#testLongCost(String) timed-out and no fallback available.  \r\n"},"msgtype":"markdown"}
2020-11-24 18:54:47.809 [http-nio-8080-exec-6]  INFO [trade-in-center,950a6403b6cf9e95,950a6403b6cf9e95,false] com.aihuishou.service.tic.repository.trade_in_foundation.IntlFqlRepositoryImpl - ActiveConnections:   0,IdleConnections:  10,ThreadsAwaitingConnection:   0,TotalConnections:  10
2020-11-24 18:54:50.818 [hystrix-IntlFqlClient-6]  INFO [trade-in-center,950a6403b6cf9e95,9196bc76a54af583,false] com.aihuishou.common.feign.customiz.FeignInfoLogger - 
[IntlFqlClient#testLongCost] ---> GET http://localhost:18080/trade-in-foundation/fql/test/mock/long-ms/200111000 HTTP/1.1
[IntlFqlClient#testLongCost] user-agent: curl/7.64.1
[IntlFqlClient#testLongCost] ---> END HTTP (0-byte body)
[IntlFqlClient#testLongCost] <--- ERROR RequestAbortedException: Request aborted (3004ms)
[IntlFqlClient#testLongCost] org.apache.http.impl.execchain.RequestAbortedException: Request aborted
	at org.apache.http.impl.execchain.MainClientExec.execute(MainClientExec.java:193)
	at brave.httpclient.TracingMainExec.execute(TracingMainExec.java:55)
	at org.apache.http.impl.execchain.ProtocolExec.execute(ProtocolExec.java:186)
	at brave.httpclient.TracingProtocolExec.execute(TracingProtocolExec.java:41)
	at org.apache.http.impl.execchain.RetryExec.execute(RetryExec.java:89)
	at org.apache.http.impl.execchain.RedirectExec.execute(RedirectExec.java:110)
	at org.apache.http.impl.client.InternalHttpClient.doExecute(InternalHttpClient.java:185)
	at org.apache.http.impl.client.CloseableHttpClient.execute(CloseableHttpClient.java:83)
	at org.apache.http.impl.client.CloseableHttpClient.execute(CloseableHttpClient.java:108)
	at org.apache.http.impl.client.CloseableHttpClient.execute(CloseableHttpClient.java:56)
	at feign.httpclient.ApacheHttpClient.execute(ApacheHttpClient.java:85)
	at org.springframework.cloud.sleuth.instrument.web.client.feign.TracingFeignClient.execute(TracingFeignClient.java:100)
	at org.springframework.cloud.sleuth.instrument.web.client.feign.LazyTracingFeignClient.execute(LazyTracingFeignClient.java:59)
	at feign.SynchronousMethodHandler.executeAndDecode(SynchronousMethodHandler.java:108)
	at feign.SynchronousMethodHandler.invoke(SynchronousMethodHandler.java:78)
	at feign.hystrix.HystrixInvocationHandler$1.run(HystrixInvocationHandler.java:106)
	at com.netflix.hystrix.HystrixCommand$2.call(HystrixCommand.java:302)
	at com.netflix.hystrix.HystrixCommand$2.call(HystrixCommand.java:298)
	at rx.internal.operators.OnSubscribeDefer.call(OnSubscribeDefer.java:46)
	at rx.internal.operators.OnSubscribeDefer.call(OnSubscribeDefer.java:35)
	at rx.internal.operators.OnSubscribeLift.call(OnSubscribeLift.java:48)
	at rx.internal.operators.OnSubscribeLift.call(OnSubscribeLift.java:30)
	at rx.internal.operators.OnSubscribeLift.call(OnSubscribeLift.java:48)
	at rx.internal.operators.OnSubscribeLift.call(OnSubscribeLift.java:30)
	at rx.internal.operators.OnSubscribeLift.call(OnSubscribeLift.java:48)
	at rx.internal.operators.OnSubscribeLift.call(OnSubscribeLift.java:30)
	at rx.Observable.unsafeSubscribe(Observable.java:10151)
	at rx.internal.operators.OnSubscribeDefer.call(OnSubscribeDefer.java:51)
	at rx.internal.operators.OnSubscribeDefer.call(OnSubscribeDefer.java:35)
	at rx.Observable.unsafeSubscribe(Observable.java:10151)
	at rx.internal.operators.OnSubscribeDoOnEach.call(OnSubscribeDoOnEach.java:41)
	at rx.internal.operators.OnSubscribeDoOnEach.call(OnSubscribeDoOnEach.java:30)
	at rx.internal.operators.OnSubscribeLift.call(OnSubscribeLift.java:48)
	at rx.internal.operators.OnSubscribeLift.call(OnSubscribeLift.java:30)
	at rx.Observable.unsafeSubscribe(Observable.java:10151)
	at rx.internal.operators.OperatorSubscribeOn$1.call(OperatorSubscribeOn.java:94)
	at com.netflix.hystrix.strategy.concurrency.HystrixContexSchedulerAction$1.call(HystrixContexSchedulerAction.java:56)
	at com.netflix.hystrix.strategy.concurrency.HystrixContexSchedulerAction$1.call(HystrixContexSchedulerAction.java:47)
	at com.aihuishou.common.feign.hystrix.RequestContextHolderHystrixConcurrencyStrategy$WrappedCallable.call(RequestContextHolderHystrixConcurrencyStrategy.java:113)
	at org.springframework.cloud.sleuth.instrument.async.TraceCallable.call(TraceCallable.java:69)
	at com.netflix.hystrix.strategy.concurrency.HystrixContexSchedulerAction.call(HystrixContexSchedulerAction.java:69)
	at rx.internal.schedulers.ScheduledAction.run(ScheduledAction.java:55)
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511)
	at java.util.concurrent.FutureTask.run(FutureTask.java:266)
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
	at java.lang.Thread.run(Thread.java:748)
Caused by: java.lang.InterruptedException
	at java.util.concurrent.locks.AbstractQueuedSynchronizer$ConditionObject.reportInterruptAfterWait(AbstractQueuedSynchronizer.java:2014)
	at java.util.concurrent.locks.AbstractQueuedSynchronizer$ConditionObject.await(AbstractQueuedSynchronizer.java:2048)
	at org.apache.http.pool.AbstractConnPool.getPoolEntryBlocking(AbstractConnPool.java:393)
	at org.apache.http.pool.AbstractConnPool.access$300(AbstractConnPool.java:70)
	at org.apache.http.pool.AbstractConnPool$2.get(AbstractConnPool.java:253)
	at org.apache.http.pool.AbstractConnPool$2.get(AbstractConnPool.java:198)
	at org.apache.http.impl.conn.PoolingHttpClientConnectionManager.leaseConnection(PoolingHttpClientConnectionManager.java:306)
	at org.apache.http.impl.conn.PoolingHttpClientConnectionManager$1.get(PoolingHttpClientConnectionManager.java:282)
	at org.apache.http.impl.execchain.MainClientExec.execute(MainClientExec.java:190)
	... 46 more

[IntlFqlClient#testLongCost] <--- END ERROR

2020-11-24 18:54:50.818 [http-nio-8080-exec-6] ERROR [trade-in-center,950a6403b6cf9e95,950a6403b6cf9e95,false] com.aihuishou.common.framework.springmvc.advice.ExceptionHandlerAdvice - 当前程序进入到异常捕获器，出错的 url 为：[ http://localhost:8080/trade-in-center/v2/base-trade-in-orders/test/detail/200111000 ]，出错的参数为：[ {"body-param":"","form-param":"{}"} ]
com.netflix.hystrix.exception.HystrixRuntimeException: IntlFqlClient#testLongCost(String) timed-out and no fallback available.
	at com.netflix.hystrix.AbstractCommand$22.call(AbstractCommand.java:822)
	at com.netflix.hystrix.AbstractCommand$22.call(AbstractCommand.java:807)
	at rx.internal.operators.OperatorOnErrorResumeNextViaFunction$4.onError(OperatorOnErrorResumeNextViaFunction.java:140)
	at rx.internal.operators.OnSubscribeDoOnEach$DoOnEachSubscriber.onError(OnSubscribeDoOnEach.java:87)
	at rx.internal.operators.OnSubscribeDoOnEach$DoOnEachSubscriber.onError(OnSubscribeDoOnEach.java:87)
	at com.netflix.hystrix.AbstractCommand$DeprecatedOnFallbackHookApplication$1.onError(AbstractCommand.java:1472)
	at com.netflix.hystrix.AbstractCommand$FallbackHookApplication$1.onError(AbstractCommand.java:1397)
	at rx.internal.operators.OnSubscribeDoOnEach$DoOnEachSubscriber.onError(OnSubscribeDoOnEach.java:87)
	at rx.observers.Subscribers$5.onError(Subscribers.java:230)
	at rx.internal.operators.OnSubscribeThrow.call(OnSubscribeThrow.java:44)
	at rx.internal.operators.OnSubscribeThrow.call(OnSubscribeThrow.java:28)
	at rx.Observable.unsafeSubscribe(Observable.java:10151)
	at rx.internal.operators.OnSubscribeDefer.call(OnSubscribeDefer.java:51)
	at rx.internal.operators.OnSubscribeDefer.call(OnSubscribeDefer.java:35)
	at rx.Observable.unsafeSubscribe(Observable.java:10151)
	at rx.internal.operators.OnSubscribeDoOnEach.call(OnSubscribeDoOnEach.java:41)
	at rx.internal.operators.OnSubscribeDoOnEach.call(OnSubscribeDoOnEach.java:30)
	at rx.internal.operators.OnSubscribeLift.call(OnSubscribeLift.java:48)
	at rx.internal.operators.OnSubscribeLift.call(OnSubscribeLift.java:30)
	at rx.internal.operators.OnSubscribeLift.call(OnSubscribeLift.java:48)
	at rx.internal.operators.OnSubscribeLift.call(OnSubscribeLift.java:30)
	at rx.Observable.unsafeSubscribe(Observable.java:10151)
	at rx.internal.operators.OnSubscribeDoOnEach.call(OnSubscribeDoOnEach.java:41)
	at rx.internal.operators.OnSubscribeDoOnEach.call(OnSubscribeDoOnEach.java:30)
	at rx.Observable.unsafeSubscribe(Observable.java:10151)
	at rx.internal.operators.OnSubscribeDoOnEach.call(OnSubscribeDoOnEach.java:41)
	at rx.internal.operators.OnSubscribeDoOnEach.call(OnSubscribeDoOnEach.java:30)
	at rx.internal.operators.OnSubscribeLift.call(OnSubscribeLift.java:48)
	at rx.internal.operators.OnSubscribeLift.call(OnSubscribeLift.java:30)
	at rx.Observable.unsafeSubscribe(Observable.java:10151)
	at rx.internal.operators.OnSubscribeDoOnEach.call(OnSubscribeDoOnEach.java:41)
	at rx.internal.operators.OnSubscribeDoOnEach.call(OnSubscribeDoOnEach.java:30)
	at rx.internal.operators.OnSubscribeLift.call(OnSubscribeLift.java:48)
	at rx.internal.operators.OnSubscribeLift.call(OnSubscribeLift.java:30)
	at rx.Observable.unsafeSubscribe(Observable.java:10151)
	at rx.internal.operators.OperatorOnErrorResumeNextViaFunction$4.onError(OperatorOnErrorResumeNextViaFunction.java:142)
	at rx.internal.operators.OnSubscribeDoOnEach$DoOnEachSubscriber.onError(OnSubscribeDoOnEach.java:87)
	at rx.internal.operators.OnSubscribeDoOnEach$DoOnEachSubscriber.onError(OnSubscribeDoOnEach.java:87)
	at com.netflix.hystrix.AbstractCommand$HystrixObservableTimeoutOperator$1.run(AbstractCommand.java:1142)
	at com.netflix.hystrix.strategy.concurrency.HystrixContextRunnable$1.call(HystrixContextRunnable.java:41)
	at com.netflix.hystrix.strategy.concurrency.HystrixContextRunnable$1.call(HystrixContextRunnable.java:37)
	at com.aihuishou.common.feign.hystrix.RequestContextHolderHystrixConcurrencyStrategy$WrappedCallable.call(RequestContextHolderHystrixConcurrencyStrategy.java:113)
	at org.springframework.cloud.sleuth.instrument.async.TraceCallable.call(TraceCallable.java:69)
	at com.netflix.hystrix.strategy.concurrency.HystrixContextRunnable.run(HystrixContextRunnable.java:57)
	at com.netflix.hystrix.AbstractCommand$HystrixObservableTimeoutOperator$2.tick(AbstractCommand.java:1159)
	at com.netflix.hystrix.util.HystrixTimer$1.run(HystrixTimer.java:99)
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511)
	at java.util.concurrent.FutureTask.runAndReset(FutureTask.java:308)
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.access$301(ScheduledThreadPoolExecutor.java:180)
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.run(ScheduledThreadPoolExecutor.java:294)
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
	at java.lang.Thread.run(Thread.java:748)
Caused by: java.util.concurrent.TimeoutException: null
	at com.netflix.hystrix.AbstractCommand.handleTimeoutViaFallback(AbstractCommand.java:997)
	at com.netflix.hystrix.AbstractCommand.access$500(AbstractCommand.java:60)
	at com.netflix.hystrix.AbstractCommand$12.call(AbstractCommand.java:609)
	at com.netflix.hystrix.AbstractCommand$12.call(AbstractCommand.java:601)
	at rx.internal.operators.OperatorOnErrorResumeNextViaFunction$4.onError(OperatorOnErrorResumeNextViaFunction.java:140)
	... 17 common frames omitted
2020-11-24 18:54:50.820 [http-nio-8080-exec-6]  INFO [trade-in-center,950a6403b6cf9e95,950a6403b6cf9e95,false] com.aihuishou.common.framework.logger.LoggerFilter - 
> request-time: 2020-11-24 18:54:47.806
> url: http://localhost:8080/trade-in-center/v2/base-trade-in-orders/test/detail/200111000
> http-method: GET
> content-type: -
> content-length: -
> host: localhost:8080
> user-agent: curl/7.64.1
> x-forwarded-for: -
> extra-param: {"traceid":"950a6403b6cf9e95"}
> body-param: -

< response-time: 2020-11-24 18:54:50.820
< http-code: 200
< content-type: application/json;charset=UTF-8
< take-time: 3014
< response-data: {"code":500,"resultMessage":"系统异常：IntlFqlClient#testLongCost(String) timed-out and no fallback available."}

2020-11-24 18:54:51.006 [SimpleAsyncTaskExecutor-5]  INFO [trade-in-center,ab6bb9eb86ce7e73,ab6bb9eb86ce7e73,false] com.aihuishou.common.util.DingTalkUtils - 预警发送成功 -> {"markdown":{"title":"钉钉机器人预警","text":"<font face=\"微软雅黑\" color=#ff0000 size=4> 服务发生非预期异常 </font>  \r\n> ENV : null  \r\n> TRACE_ID : 950a6403b6cf9e95  \r\n> 业务环节 : /trade-in-center/v2/base-trade-in-orders/test/detail/200111000  \r\n> 方法名 : GET  \r\n> 方法入参 : {\"body-param\":\"\",\"form-param\":\"{}\"}  \r\n> 额外信息 : null  \r\n> 时间 : 2020-11-24 18:54:47.806  \r\n> 异常信息 : IntlFqlClient#testLongCost(String) timed-out and no fallback available.  \r\n"},"msgtype":"markdown"}
2020-11-24 18:55:03.730 [hystrix-IntlFqlClient-5]  INFO [trade-in-center,6a53ad034caa47b3,e26a9993b0572801,false] com.aihuishou.common.feign.customiz.FeignInfoLogger - 
[IntlFqlClient#testLongCost] ---> GET http://localhost:18080/trade-in-foundation/fql/test/mock/long-ms/2000 HTTP/1.1
[IntlFqlClient#testLongCost] user-agent: curl/7.64.1
[IntlFqlClient#testLongCost] ---> END HTTP (0-byte body)
[IntlFqlClient#testLongCost] <--- HTTP/1.1 200  (20535ms)
[IntlFqlClient#testLongCost] connection: keep-alive
[IntlFqlClient#testLongCost] content-length: 43
[IntlFqlClient#testLongCost] content-type: application/json;charset=UTF-8
[IntlFqlClient#testLongCost] date: Tue, 24 Nov 2020 10:55:03 GMT
[IntlFqlClient#testLongCost] keep-alive: timeout=60
[IntlFqlClient#testLongCost] 
[IntlFqlClient#testLongCost] {"code":200,"resultMessage":"","data":true}
[IntlFqlClient#testLongCost] <--- END HTTP (43-byte body)

%/accordion%
```

### 再模拟场景二
主要整体配置信息如下
```
# feign
feign.httpclient.enabled=true
feign.httpclient.max-connections-per-route=1
feign.httpclient.max-connections=200
feign.client.default-to-properties=false
feign.client.config.default.connect-timeout=1000
feign.client.config.default.read-timeout=3050
# Hystrix
feign.hystrix.enabled=true
hystrix.command.default.execution.isolation.thread.timeoutInMilliseconds=3000
hystrix.threadpool.default.coreSize=10
hystrix.threadpool.default.maximumSize=20
hystrix.threadpool.default.allowMaximumSizeToDivergeFromCoreSize=true
hystrix.threadpool.default.maxQueueSize=100
hystrix.threadpool.default.queueSizeRejectionThreshold=101
```
```bash
curl http://localhost:8080/trade-in-center/v2/base-trade-in-orders/test/detail/200001
{"code":500,"resultMessage":"系统异常：IntlFqlClient#testLongCost(String) timed-out and no fallback available."}%
curl http://localhost:8080/trade-in-center/v2/base-trade-in-orders/test/detail/20011102
{"code":200,"resultMessage":"","data":null}%
```
日志信息如下
```
%accordion%第二次请求A服务日志如下%accordion%

2020-11-24 19:06:55.495 [http-nio-8080-exec-2]  INFO [trade-in-center,961f7dcc1fc7aaec,961f7dcc1fc7aaec,false] com.aihuishou.service.tic.repository.trade_in_foundation.IntlFqlRepositoryImpl - ActiveConnections:   0,IdleConnections:  10,ThreadsAwaitingConnection:   0,TotalConnections:  10
2020-11-24 19:06:58.527 [http-nio-8080-exec-2] ERROR [trade-in-center,961f7dcc1fc7aaec,961f7dcc1fc7aaec,false] com.aihuishou.common.framework.springmvc.advice.ExceptionHandlerAdvice - 当前程序进入到异常捕获器，出错的 url 为：[ http://localhost:8080/trade-in-center/v2/base-trade-in-orders/test/detail/200001 ]，出错的参数为：[ {"body-param":"","form-param":"{}"} ]
com.netflix.hystrix.exception.HystrixRuntimeException: IntlFqlClient#testLongCost(String) timed-out and no fallback available.
	at com.netflix.hystrix.AbstractCommand$22.call(AbstractCommand.java:822)
	at com.netflix.hystrix.AbstractCommand$22.call(AbstractCommand.java:807)
	at rx.internal.operators.OperatorOnErrorResumeNextViaFunction$4.onError(OperatorOnErrorResumeNextViaFunction.java:140)
	at rx.internal.operators.OnSubscribeDoOnEach$DoOnEachSubscriber.onError(OnSubscribeDoOnEach.java:87)
	at rx.internal.operators.OnSubscribeDoOnEach$DoOnEachSubscriber.onError(OnSubscribeDoOnEach.java:87)
	at com.netflix.hystrix.AbstractCommand$DeprecatedOnFallbackHookApplication$1.onError(AbstractCommand.java:1472)
	at com.netflix.hystrix.AbstractCommand$FallbackHookApplication$1.onError(AbstractCommand.java:1397)
	at rx.internal.operators.OnSubscribeDoOnEach$DoOnEachSubscriber.onError(OnSubscribeDoOnEach.java:87)
	at rx.observers.Subscribers$5.onError(Subscribers.java:230)
	at rx.internal.operators.OnSubscribeThrow.call(OnSubscribeThrow.java:44)
	at rx.internal.operators.OnSubscribeThrow.call(OnSubscribeThrow.java:28)
	at rx.Observable.unsafeSubscribe(Observable.java:10151)
	at rx.internal.operators.OnSubscribeDefer.call(OnSubscribeDefer.java:51)
	at rx.internal.operators.OnSubscribeDefer.call(OnSubscribeDefer.java:35)
	at rx.Observable.unsafeSubscribe(Observable.java:10151)
	at rx.internal.operators.OnSubscribeDoOnEach.call(OnSubscribeDoOnEach.java:41)
	at rx.internal.operators.OnSubscribeDoOnEach.call(OnSubscribeDoOnEach.java:30)
	at rx.internal.operators.OnSubscribeLift.call(OnSubscribeLift.java:48)
	at rx.internal.operators.OnSubscribeLift.call(OnSubscribeLift.java:30)
	at rx.internal.operators.OnSubscribeLift.call(OnSubscribeLift.java:48)
	at rx.internal.operators.OnSubscribeLift.call(OnSubscribeLift.java:30)
	at rx.Observable.unsafeSubscribe(Observable.java:10151)
	at rx.internal.operators.OnSubscribeDoOnEach.call(OnSubscribeDoOnEach.java:41)
	at rx.internal.operators.OnSubscribeDoOnEach.call(OnSubscribeDoOnEach.java:30)
	at rx.Observable.unsafeSubscribe(Observable.java:10151)
	at rx.internal.operators.OnSubscribeDoOnEach.call(OnSubscribeDoOnEach.java:41)
	at rx.internal.operators.OnSubscribeDoOnEach.call(OnSubscribeDoOnEach.java:30)
	at rx.internal.operators.OnSubscribeLift.call(OnSubscribeLift.java:48)
	at rx.internal.operators.OnSubscribeLift.call(OnSubscribeLift.java:30)
	at rx.Observable.unsafeSubscribe(Observable.java:10151)
	at rx.internal.operators.OnSubscribeDoOnEach.call(OnSubscribeDoOnEach.java:41)
	at rx.internal.operators.OnSubscribeDoOnEach.call(OnSubscribeDoOnEach.java:30)
	at rx.internal.operators.OnSubscribeLift.call(OnSubscribeLift.java:48)
	at rx.internal.operators.OnSubscribeLift.call(OnSubscribeLift.java:30)
	at rx.Observable.unsafeSubscribe(Observable.java:10151)
	at rx.internal.operators.OperatorOnErrorResumeNextViaFunction$4.onError(OperatorOnErrorResumeNextViaFunction.java:142)
	at rx.internal.operators.OnSubscribeDoOnEach$DoOnEachSubscriber.onError(OnSubscribeDoOnEach.java:87)
	at rx.internal.operators.OnSubscribeDoOnEach$DoOnEachSubscriber.onError(OnSubscribeDoOnEach.java:87)
	at com.netflix.hystrix.AbstractCommand$HystrixObservableTimeoutOperator$1.run(AbstractCommand.java:1142)
	at com.netflix.hystrix.strategy.concurrency.HystrixContextRunnable$1.call(HystrixContextRunnable.java:41)
	at com.netflix.hystrix.strategy.concurrency.HystrixContextRunnable$1.call(HystrixContextRunnable.java:37)
	at com.aihuishou.common.feign.hystrix.RequestContextHolderHystrixConcurrencyStrategy$WrappedCallable.call(RequestContextHolderHystrixConcurrencyStrategy.java:113)
	at org.springframework.cloud.sleuth.instrument.async.TraceCallable.call(TraceCallable.java:69)
	at com.netflix.hystrix.strategy.concurrency.HystrixContextRunnable.run(HystrixContextRunnable.java:57)
	at com.netflix.hystrix.AbstractCommand$HystrixObservableTimeoutOperator$2.tick(AbstractCommand.java:1159)
	at com.netflix.hystrix.util.HystrixTimer$1.run(HystrixTimer.java:99)
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511)
	at java.util.concurrent.FutureTask.runAndReset(FutureTask.java:308)
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.access$301(ScheduledThreadPoolExecutor.java:180)
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.run(ScheduledThreadPoolExecutor.java:294)
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
	at java.lang.Thread.run(Thread.java:748)
Caused by: java.util.concurrent.TimeoutException: null
	at com.netflix.hystrix.AbstractCommand.handleTimeoutViaFallback(AbstractCommand.java:997)
	at com.netflix.hystrix.AbstractCommand.access$500(AbstractCommand.java:60)
	at com.netflix.hystrix.AbstractCommand$12.call(AbstractCommand.java:609)
	at com.netflix.hystrix.AbstractCommand$12.call(AbstractCommand.java:601)
	at rx.internal.operators.OperatorOnErrorResumeNextViaFunction$4.onError(OperatorOnErrorResumeNextViaFunction.java:140)
	... 17 common frames omitted
2020-11-24 19:06:58.534 [http-nio-8080-exec-2]  INFO [trade-in-center,961f7dcc1fc7aaec,961f7dcc1fc7aaec,false] org.springframework.scheduling.annotation.AnnotationAsyncExecutionInterceptor - More than one TaskExecutor bean found within the context, and none is named 'taskExecutor'. Mark one of them as primary or name it 'taskExecutor' (possibly as an alias) in order to use it for async processing: [aggExecutor, aggregatorThreadPoolExecutor]
2020-11-24 19:06:58.538 [http-nio-8080-exec-2]  INFO [trade-in-center,961f7dcc1fc7aaec,961f7dcc1fc7aaec,false] com.aihuishou.common.framework.logger.LoggerFilter - 
> request-time: 2020-11-24 19:06:55.490
> url: http://localhost:8080/trade-in-center/v2/base-trade-in-orders/test/detail/200001
> http-method: GET
> content-type: -
> content-length: -
> host: localhost:8080
> user-agent: curl/7.64.1
> x-forwarded-for: -
> extra-param: {"traceid":"961f7dcc1fc7aaec"}
> body-param: -

< response-time: 2020-11-24 19:06:58.537
< http-code: 200
< content-type: application/json;charset=UTF-8
< take-time: 3047
< response-data: {"code":500,"resultMessage":"系统异常：IntlFqlClient#testLongCost(String) timed-out and no fallback available."}

2020-11-24 19:06:58.556 [hystrix-IntlFqlClient-2]  INFO [trade-in-center,961f7dcc1fc7aaec,3a15a861f8b1c62a,false] com.aihuishou.common.feign.customiz.FeignInfoLogger - 
[IntlFqlClient#testLongCost] ---> GET http://localhost:18080/trade-in-foundation/fql/test/mock/long-ms/200001 HTTP/1.1
[IntlFqlClient#testLongCost] user-agent: curl/7.64.1
[IntlFqlClient#testLongCost] ---> END HTTP (0-byte body)
[IntlFqlClient#testLongCost] <--- ERROR SocketTimeoutException: Read timed out (3056ms)
[IntlFqlClient#testLongCost] java.net.SocketTimeoutException: Read timed out
	at java.net.SocketInputStream.socketRead0(Native Method)
	at java.net.SocketInputStream.socketRead(SocketInputStream.java:116)
	at java.net.SocketInputStream.read(SocketInputStream.java:171)
	at java.net.SocketInputStream.read(SocketInputStream.java:141)
	at org.apache.http.impl.io.SessionInputBufferImpl.streamRead(SessionInputBufferImpl.java:137)
	at org.apache.http.impl.io.SessionInputBufferImpl.fillBuffer(SessionInputBufferImpl.java:153)
	at org.apache.http.impl.io.SessionInputBufferImpl.readLine(SessionInputBufferImpl.java:280)
	at org.apache.http.impl.conn.DefaultHttpResponseParser.parseHead(DefaultHttpResponseParser.java:138)
	at org.apache.http.impl.conn.DefaultHttpResponseParser.parseHead(DefaultHttpResponseParser.java:56)
	at org.apache.http.impl.io.AbstractMessageParser.parse(AbstractMessageParser.java:259)
	at org.apache.http.impl.DefaultBHttpClientConnection.receiveResponseHeader(DefaultBHttpClientConnection.java:163)
	at org.apache.http.impl.conn.CPoolProxy.receiveResponseHeader(CPoolProxy.java:157)
	at org.apache.http.protocol.HttpRequestExecutor.doReceiveResponse(HttpRequestExecutor.java:273)
	at org.apache.http.protocol.HttpRequestExecutor.execute(HttpRequestExecutor.java:125)
	at org.apache.http.impl.execchain.MainClientExec.execute(MainClientExec.java:272)
	at brave.httpclient.TracingMainExec.execute(TracingMainExec.java:55)
	at org.apache.http.impl.execchain.ProtocolExec.execute(ProtocolExec.java:186)
	at brave.httpclient.TracingProtocolExec.execute(TracingProtocolExec.java:41)
	at org.apache.http.impl.execchain.RetryExec.execute(RetryExec.java:89)
	at org.apache.http.impl.execchain.RedirectExec.execute(RedirectExec.java:110)
	at org.apache.http.impl.client.InternalHttpClient.doExecute(InternalHttpClient.java:185)
	at org.apache.http.impl.client.CloseableHttpClient.execute(CloseableHttpClient.java:83)
	at org.apache.http.impl.client.CloseableHttpClient.execute(CloseableHttpClient.java:108)
	at org.apache.http.impl.client.CloseableHttpClient.execute(CloseableHttpClient.java:56)
	at feign.httpclient.ApacheHttpClient.execute(ApacheHttpClient.java:85)
	at org.springframework.cloud.sleuth.instrument.web.client.feign.TracingFeignClient.execute(TracingFeignClient.java:100)
	at org.springframework.cloud.sleuth.instrument.web.client.feign.LazyTracingFeignClient.execute(LazyTracingFeignClient.java:59)
	at feign.SynchronousMethodHandler.executeAndDecode(SynchronousMethodHandler.java:108)
	at feign.SynchronousMethodHandler.invoke(SynchronousMethodHandler.java:78)
	at feign.hystrix.HystrixInvocationHandler$1.run(HystrixInvocationHandler.java:106)
	at com.netflix.hystrix.HystrixCommand$2.call(HystrixCommand.java:302)
	at com.netflix.hystrix.HystrixCommand$2.call(HystrixCommand.java:298)
	at rx.internal.operators.OnSubscribeDefer.call(OnSubscribeDefer.java:46)
	at rx.internal.operators.OnSubscribeDefer.call(OnSubscribeDefer.java:35)
	at rx.internal.operators.OnSubscribeLift.call(OnSubscribeLift.java:48)
	at rx.internal.operators.OnSubscribeLift.call(OnSubscribeLift.java:30)
	at rx.internal.operators.OnSubscribeLift.call(OnSubscribeLift.java:48)
	at rx.internal.operators.OnSubscribeLift.call(OnSubscribeLift.java:30)
	at rx.internal.operators.OnSubscribeLift.call(OnSubscribeLift.java:48)
	at rx.internal.operators.OnSubscribeLift.call(OnSubscribeLift.java:30)
	at rx.Observable.unsafeSubscribe(Observable.java:10151)
	at rx.internal.operators.OnSubscribeDefer.call(OnSubscribeDefer.java:51)
	at rx.internal.operators.OnSubscribeDefer.call(OnSubscribeDefer.java:35)
	at rx.Observable.unsafeSubscribe(Observable.java:10151)
	at rx.internal.operators.OnSubscribeDoOnEach.call(OnSubscribeDoOnEach.java:41)
	at rx.internal.operators.OnSubscribeDoOnEach.call(OnSubscribeDoOnEach.java:30)
	at rx.internal.operators.OnSubscribeLift.call(OnSubscribeLift.java:48)
	at rx.internal.operators.OnSubscribeLift.call(OnSubscribeLift.java:30)
	at rx.Observable.unsafeSubscribe(Observable.java:10151)
	at rx.internal.operators.OperatorSubscribeOn$1.call(OperatorSubscribeOn.java:94)
	at com.netflix.hystrix.strategy.concurrency.HystrixContexSchedulerAction$1.call(HystrixContexSchedulerAction.java:56)
	at com.netflix.hystrix.strategy.concurrency.HystrixContexSchedulerAction$1.call(HystrixContexSchedulerAction.java:47)
	at com.aihuishou.common.feign.hystrix.RequestContextHolderHystrixConcurrencyStrategy$WrappedCallable.call(RequestContextHolderHystrixConcurrencyStrategy.java:113)
	at org.springframework.cloud.sleuth.instrument.async.TraceCallable.call(TraceCallable.java:69)
	at com.netflix.hystrix.strategy.concurrency.HystrixContexSchedulerAction.call(HystrixContexSchedulerAction.java:69)
	at rx.internal.schedulers.ScheduledAction.run(ScheduledAction.java:55)
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511)
	at java.util.concurrent.FutureTask.run(FutureTask.java:266)
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
	at java.lang.Thread.run(Thread.java:748)

[IntlFqlClient#testLongCost] <--- END ERROR

2020-11-24 19:06:58.986 [SimpleAsyncTaskExecutor-1]  INFO [trade-in-center,488fc29b23702cae,488fc29b23702cae,false] com.aihuishou.common.util.DingTalkUtils - 预警发送成功 -> {"markdown":{"title":"钉钉机器人预警","text":"<font face=\"微软雅黑\" color=#ff0000 size=4> 服务发生非预期异常 </font>  \r\n> ENV : null  \r\n> TRACE_ID : 961f7dcc1fc7aaec  \r\n> 业务环节 : /trade-in-center/v2/base-trade-in-orders/test/detail/200001  \r\n> 方法名 : GET  \r\n> 方法入参 : {\"body-param\":\"\",\"form-param\":\"{}\"}  \r\n> 额外信息 : null  \r\n> 时间 : 2020-11-24 19:06:55.490  \r\n> 异常信息 : IntlFqlClient#testLongCost(String) timed-out and no fallback available.  \r\n"},"msgtype":"markdown"}
2020-11-24 19:07:00.245 [http-nio-8080-exec-3]  INFO [trade-in-center,d4dd8ba70c7ca13f,d4dd8ba70c7ca13f,false] com.aihuishou.service.tic.repository.trade_in_foundation.IntlFqlRepositoryImpl - ActiveConnections:   0,IdleConnections:  10,ThreadsAwaitingConnection:   0,TotalConnections:  10
2020-11-24 19:07:00.273 [hystrix-IntlFqlClient-3]  INFO [trade-in-center,d4dd8ba70c7ca13f,bae1dccc1cf086da,false] com.aihuishou.common.feign.customiz.FeignInfoLogger - 
[IntlFqlClient#testLongCost] ---> GET http://localhost:18080/trade-in-foundation/fql/test/mock/long-ms/20011102 HTTP/1.1
[IntlFqlClient#testLongCost] user-agent: curl/7.64.1
[IntlFqlClient#testLongCost] ---> END HTTP (0-byte body)
[IntlFqlClient#testLongCost] <--- HTTP/1.1 200  (24ms)
[IntlFqlClient#testLongCost] connection: keep-alive
[IntlFqlClient#testLongCost] content-length: 43
[IntlFqlClient#testLongCost] content-type: application/json;charset=UTF-8
[IntlFqlClient#testLongCost] date: Tue, 24 Nov 2020 11:07:00 GMT
[IntlFqlClient#testLongCost] keep-alive: timeout=60
[IntlFqlClient#testLongCost] 
[IntlFqlClient#testLongCost] {"code":200,"resultMessage":"","data":true}
[IntlFqlClient#testLongCost] <--- END HTTP (43-byte body)

2020-11-24 19:07:00.277 [http-nio-8080-exec-3]  INFO [trade-in-center,d4dd8ba70c7ca13f,d4dd8ba70c7ca13f,false] com.aihuishou.service.tic.repository.trade_in_foundation.IntlFqlRepositoryImpl - ActiveConnections:   0,IdleConnections:  10,ThreadsAwaitingConnection:   0,TotalConnections:  10
2020-11-24 19:07:00.279 [http-nio-8080-exec-3]  INFO [trade-in-center,d4dd8ba70c7ca13f,d4dd8ba70c7ca13f,false] com.aihuishou.common.framework.logger.LoggerFilter - 
> request-time: 2020-11-24 19:07:00.237
> url: http://localhost:8080/trade-in-center/v2/base-trade-in-orders/test/detail/20011102
> http-method: GET
> content-type: -
> content-length: -
> host: localhost:8080
> user-agent: curl/7.64.1
> x-forwarded-for: -
> extra-param: {"traceid":"d4dd8ba70c7ca13f"}
> body-param: -

< response-time: 2020-11-24 19:07:00.279
< http-code: 200
< content-type: application/json;charset=UTF-8
< take-time: 42
< response-data: {"code":200,"resultMessage":"","data":null}

%/accordion%
```

#doc
[hystrix/how it works](https://github.com/Netflix/Hystrix/wiki/How-it-Works) 