#    

# FutureTask相关接口和类

* Callable
* Future
* RunnableFuture

RunnableAdapter

# 基本概念

## 4种状态流

状态和状态流 终态(NORMAL,EXCEPTIONAL,CANCELLED,INTERRUPTED)
TODO:cj

# 应知应会

## 关于validate state的设计
而outcome无需是volatile修饰

```java
public class FutureTask {
    private volatile int state;
}
```

```java
public class FutureTask {
    private static final int INTERRUPTED = 6;

    /** The underlying callable; nulled out after running */
    private Callable<V> callable;
    /** The result to return or exception to throw from get() */
    private Object outcome; // non-volatile, protected by state reads/writes
    /** The thread running the callable; CASed during run() */
    private volatile Thread runner;
    /** Treiber stack of waiting threads */
    private volatile WaitNode waiters;
}
```

##    

源码里多次提到的 TODO:cj

###

# 蜻蜓点水

## runAndReset方法可重复执行调用

## FutureTask的UNSAFE

源码 TODO:cj 这其实是个大头，但是目前还啃不动

# 设计小挑战

## Treiber Stack 无锁并发栈

小挑战,自己模拟实现下该数据结构，并需通过设计良好的单元自测

## 自己实现下FutureTask源码

# 资料