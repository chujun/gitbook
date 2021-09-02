#

#     

# 应知应会

## 如何实时统计线程中的活跃数量
***探究activeCount方法实现*** ***标签二***

并不严格是某一时刻的真实存活数量，而是大致的预估值，通过线程的ThreadGroup大致统计

统计线程组实时存活数量通过线程组的快照方式，加锁策略生成线程组快照数组方式
(基于ThreadGroup组数结构的某一层加锁，而非全局ThreadGroup数加锁，减少锁粒度)统计

```java
public class Thread{
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
     * @return  an estimate of the number of active threads in the current
     *          thread's thread group and in any other thread group that
     *          has the current thread's thread group as an ancestor
     */
    public static int activeCount() {
        return currentThread().getThreadGroup().activeCount();
    }
}

public class ThreadGroup{
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
     * @return  an estimate of the number of active threads in this thread
     *          group and in any other thread group that has this thread
     *          group as an ancestor
     *
     * @since   JDK1.0
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
        for (int i = 0 ; i < ngroupsSnapshot ; i++) {
            //同步块外再统计累加子ThreadGroup活跃线程数量
            result += groupsSnapshot[i].activeCount();
        }
        return result;
    }
}

```
##     

线程异常处理有默认线程异常处理器和线程处理器 uncaughtExceptionHandler defaultUncaughtExceptionHandler

## join方法的作用与实现

释放cpu，释放锁 基于wait方法实现

```java
public class Thread {
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

经典的伪共享问题， cpu缓存冲突/失效问题
[Java8使用@sun.misc.Contended避免伪共享](https://www.jianshu.com/p/c3c108c3dcfd)

# 蜻蜓点水

## isCCLOverridden方法作用

# 资料

[Java8使用@sun.misc.Contended避免伪共享](https://www.jianshu.com/p/c3c108c3dcfd)

