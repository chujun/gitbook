# 应知应会

## ThreadGroup和Thread的关系

TODO:cj Thread和ThreadGroup关系图 ThradGroup之间的关系是树的关系，而Thread与ThradGroup的关系就像元素与集合的关系。

```
├─ ThreadGroup[name=system,maxpri=10]
│  ├─Thread[Reference Handler,10,system]
│  ├─Thread[Finalizer,8,system]
│  ├─Thread[Signal Dispatcher,9,system]
│  ├─Thread[Attach Listener,5,system]
│  ├─ThreadGroup[name=main,maxpri=10]
│  │  ├─Thread[main,5,main]
│  │  ├─Thread[Monitor Ctrl-Break,5,main]
│  │  ├─Thread[Thread1,5,main]                     // 这个线程是自定义的线程
│  │  ├─ThreadGroup[name=MyThreadGroup,maxpri=10]  // 自定义线程组
│  │      └─Thread[MyThread2,5,MyThreadGroup]      // 自定义线程,添加到指定组
```
[示例-ThreadGroupTest](https://github.com/chujun/javaddu/blob/master/src/test/java/com/jun/chu/java/mulithread/ThreadGroupTest.java)

根ThreadGroup名称是"system".

```java
public class ThreadGroup {
    /**
     * Creates an empty Thread group that is not in any Thread group.
     * This method is used to create the system Thread group.
     */
    private ThreadGroup() {     // called from C code
        this.name = "system";
        this.maxPriority = Thread.MAX_PRIORITY;
        this.parent = null;
    }
}
```


## ThreadGroup的锁策略理解

可见 Thread.md#如何实时统计线程中的活跃数量

# 蜻蜓点水

# 资料

[Thread及ThreadGroup杂谈](https://www.jianshu.com/p/e682d620eba4?share_token=086a0cd6-284a-48b9-959b-69922d9d1600)
[并发编程基础 之 Thread 与ThreadGroup的介绍(api介绍)](https://blog.csdn.net/dreamhai/article/details/86611538?share_token=03bf7252-8962-4c7f-991e-4084c6ceb3ed)