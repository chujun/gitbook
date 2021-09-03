#

#              

# 应知应会

## 如何实时统计线程中的活跃数量

***探究activeCount方法实现*** ***大致预估值***

并不严格是某一时刻的真实存活数量，而是大致的预估值， 通过线程的ThreadGroup大致统计,

=当前线程组的线程活跃数量+其下的子线程组的线程活跃数量

统计线程组实时存活数量通过线程组的快照方式，加锁策略生成线程组快照数组方式
(基于ThreadGroup组数结构的某一层加锁，而非全局ThreadGroup数加锁，减少锁粒度)统计

```java
public class Thread {
    /**
     * Returns an estimate of the number of active threads in the current
     * thread's {@linkplain java.lang.ThreadGroup thread group} and its
     * subgroups. Recursively iterates over all subgroups in the current
     * thread's thread group.
     *
     * <p> The value returned is only an estimate because the number of
     * threads may change dynamically while this method traverses internal
     * data structures, and might be affected by the presence of certain
     * system threads. This method is intended primarily for debugging
     * and monitoring purposes.
     *
     * @return an estimate of the number of active threads in the current
     *          thread's thread group and in any other thread group that
     *          has the current thread's thread group as an ancestor
     */
    public static int activeCount() {
        return currentThread().getThreadGroup().activeCount();
    }
}

public class ThreadGroup {
    /**
     * Returns an estimate of the number of active threads in this thread
     * group and its subgroups. Recursively iterates over all subgroups in
     * this thread group.
     *
     * <p> The value returned is only an estimate because the number of
     * threads may change dynamically while this method traverses internal
     * data structures, and might be affected by the presence of certain
     * system threads. This method is intended primarily for debugging
     * and monitoring purposes.
     *
     * @return an estimate of the number of active threads in this thread
     *          group and in any other thread group that has this thread
     *          group as an ancestor
     *
     * @since JDK1.0
     */
    public int activeCount() {
        int result;
        // Snapshot sub-group data so we don't hold this lock
        // while our children are computing.
        int ngroupsSnapshot;
        //子ThreadGroup的快照版本
        ThreadGroup[] groupsSnapshot;
        //ThreadGroup分层上锁策略，基于树的某一层上锁
        synchronized (this) {
            if (destroyed) {
                return 0;
            }
            result = nthreads;
            ngroupsSnapshot = ngroups;
            if (groups != null) {
                groupsSnapshot = Arrays.copyOf(groups, ngroupsSnapshot);
            } else {
                groupsSnapshot = null;
            }
        }
        for (int i = 0; i < ngroupsSnapshot; i++) {
            //同步块外再统计累加子ThreadGroup活跃线程数量
            result += groupsSnapshot[i].activeCount();
        }
        return result;
    }
}

```

## 线程配置默认线程异常处理器和线程处理器

属性值

```java
public class Thread {
    // null unless explicitly set
    private volatile UncaughtExceptionHandler uncaughtExceptionHandler;

    // null unless explicitly set
    private static volatile UncaughtExceptionHandler defaultUncaughtExceptionHandler;


    /**
     * 该方法仅被JVM使用，用于分发线程中的异常
     * Dispatch an uncaught exception to the handler. This method is
     * intended to be called only by the JVM.
     */
    private void dispatchUncaughtException(Throwable e) {
        getUncaughtExceptionHandler().uncaughtException(this, e);
    }
}
```

UncaughtExceptionHandler 未捕获异常处理器 通常建议设置全局的线程处理器

不设置的话，默认使用ThreadGroup的uncaughtException方法将错误输出到System.err路径里(不便于定位问题)

## join方法的作用与实现

***wait实现***
释放cpu，释放锁 基于wait方法实现

```java
public class Thread {
    /**
     * Waits at most {@code millis} milliseconds for this thread to
     * die. A timeout of {@code 0} means to wait forever.
     *
     * <p> This implementation uses a loop of {@code this.wait} calls
     * conditioned on {@code this.isAlive}. As a thread terminates the
     * {@code this.notifyAll} method is invoked. It is recommended that
     * applications not use {@code wait}, {@code notify}, or
     * {@code notifyAll} on {@code Thread} instances.
     *
     * @param  millis
     *         the time to wait in milliseconds
     *
     * @throws IllegalArgumentException
     *          if the value of {@code millis} is negative
     *
     * @throws InterruptedException
     *          if any thread has interrupted the current thread. The
     *          <i>interrupted status</i> of the current thread is
     *          cleared when this exception is thrown.
     */
    public final synchronized void join(long millis) throws InterruptedException {
        long base = System.currentTimeMillis();
        long now = 0;

        if (millis < 0) {
            throw new IllegalArgumentException("timeout value is negative");
        }

        if (millis == 0) {
            while (isAlive()) {
                wait(0);
            }
        } else {
            while (isAlive()) {
                long delay = millis - now;
                if (delay <= 0) {
                    break;
                }
                wait(delay);
                now = System.currentTimeMillis() - base;
            }
        }
    }
}
```

## Thread使用@Contended注解处理ThreadLocalRandom中所需的三个字段的伪共享问题

```java
public class Thread {
    /** The current seed for a ThreadLocalRandom */
    @sun.misc.Contended("tlr")
    long threadLocalRandomSeed;

    /** Probe hash value; nonzero if threadLocalRandomSeed initialized */
    @sun.misc.Contended("tlr")
    int threadLocalRandomProbe;

    /** Secondary seed isolated from public ThreadLocalRandom sequence */
    @sun.misc.Contended("tlr")
    int threadLocalRandomSecondarySeed;
}
```
经典的伪共享问题， cpu缓存冲突/失效问题
需要启用参数 -XX:-RestrictContended 前后加128个byte，针对大多数cpu硬件两倍缓存行尺寸(64byte)

[Java8使用@sun.misc.Contended避免伪共享](https://www.jianshu.com/p/c3c108c3dcfd)
下面对文章中的示例做了demo
(FalseSharing源码示例)[https://github.com/chujun/javaddu/blob/master/src/main/java/com/jun/chu/java/mulitread/FalseSharing.java]


[RFR (S): JEP-142: Reduce Cache Contention on Specified Fields](http://mail.openjdk.java.net/pipermail/hotspot-dev/2012-November/007309.html)
这篇文章里详细描述了@Contended的大致内存布局(包裹作用在类上和方法上)和@Contended分组使用的内存布局

基于类的@Contended

```java

@Contended
public static class ContendedTest2 {
    private Object plainField1;
    private Object plainField2;
    private Object plainField3;
    private Object plainField4;
}
```

```
Entire class is marked contended
     @140 --- instance fields start ---
     @140 "plainField1" Ljava.lang.Object;
     @144 "plainField2" Ljava.lang.Object;
     @148 "plainField3" Ljava.lang.Object;
     @152 "plainField4" Ljava.lang.Object;
     @288 --- instance fields end ---
     @288 --- instance ends ---
```

152+4=156,156+128=284!=288????TODO:cj怎么理解

基于单个字段的@Contended

```java
public static class ContendedTest1 {
    @Contended
    private Object contendedField1;
    private Object plainField1;
    private Object plainField2;
    private Object plainField3;
    private Object plainField4;
}
```

```
@ 12 --- instance fields start ---
     @ 12 "plainField1" Ljava.lang.Object;
     @ 16 "plainField2" Ljava.lang.Object;
     @ 20 "plainField3" Ljava.lang.Object;
     @ 24 "plainField4" Ljava.lang.Object;
     @156 "contendedField1" Ljava.lang.Object; (contended, group = 0)
     @288 --- instance fields end ---
     @288 --- instance ends ---
```
24+4=28，28+128=156,
156+4=160,160+128=288

基于多个字段的@Contended
```java
public static class ContendedTest4 {
        @Contended
        private Object contendedField1;

        @Contended
        private Object contendedField2;

        private Object plainField3;
        private Object plainField4;
    }
```
```
@ 12 --- instance fields start ---
     @ 12 "plainField3" Ljava.lang.Object;
     @ 16 "plainField4" Ljava.lang.Object;
     @148 "contendedField1" Ljava.lang.Object; (contended, group = 0)
     @280 "contendedField2" Ljava.lang.Object; (contended, group = 0)
     @416 --- instance fields end ---
     @416 --- instance ends ---
```
16+4=20，20+128=148
148+4=152，152+128=280
280+4=284，284+128=412，412+4=416

基于分组的@Contended
```java
public static class ContendedTest5 {
        @Contended("updater1")
        private Object contendedField1;

        @Contended("updater1")
        private Object contendedField2;

        @Contended("updater2")
        private Object contendedField3;

        private Object plainField5;
        private Object plainField6;
    }
```
```
@ 12 --- instance fields start ---
     @ 12 "plainField5" Ljava.lang.Object;
     @ 16 "plainField6" Ljava.lang.Object;
     @148 "contendedField1" Ljava.lang.Object; (contended, group = 12)
     @152 "contendedField2" Ljava.lang.Object; (contended, group = 12)
     @284 "contendedField3" Ljava.lang.Object; (contended, group = 15)
     @416 --- instance fields end ---
     @416 --- instance ends ---
```
16+4=20，20+128=148，
152+4=156，156+128=284
284+4=288，288+128=416

### 这里面引出了另一个问题，如何计算一个java对象的内存使用情况
classmexer
[如何计算java对象内存使用情况,classmexer.jar](https://www.javamex.com/classmexer/)

# 蜻蜓点水

## isCCLOverridden方法作用

通过*SecurityManager*的checkAccess(Thread)方法安全验证

SecurityConstants 存在一系列常量

```java
public class SecurityConstants {
    public static final NetPermission GET_RESPONSECACHE_PERMISSION = new NetPermission("getResponseCache");
    public static final RuntimePermission CREATE_CLASSLOADER_PERMISSION = new RuntimePermission("createClassLoader");
    public static final RuntimePermission CHECK_MEMBER_ACCESS_PERMISSION = new RuntimePermission("accessDeclaredMembers");
    public static final RuntimePermission MODIFY_THREAD_PERMISSION = new RuntimePermission("modifyThread");
    public static final RuntimePermission MODIFY_THREADGROUP_PERMISSION = new RuntimePermission("modifyThreadGroup");
    public static final RuntimePermission GET_PD_PERMISSION = new RuntimePermission("getProtectionDomain");
    public static final RuntimePermission GET_CLASSLOADER_PERMISSION = new RuntimePermission("getClassLoader");
    public static final RuntimePermission STOP_THREAD_PERMISSION = new RuntimePermission("stopThread");
    public static final RuntimePermission GET_STACK_TRACE_PERMISSION = new RuntimePermission("getStackTrace");
}
```

# 资料

[Java8使用@sun.misc.Contended避免伪共享](https://www.jianshu.com/p/c3c108c3dcfd)
[如何计算java对象内存使用情况,classmexer.jar](https://www.javamex.com/classmexer/)

