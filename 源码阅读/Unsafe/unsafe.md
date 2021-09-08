#

* sun.misc.Unsafe 是JDK内部用的工具类。
* 它通过暴露一些Java意义上说“不安全”的功能给Java层代码，
* 来让JDK能够更多的使用Java代码来实现一些原本是平台相关的、需要使用native语言（例如C或C++）才可以实现的功能。
  (例如内存分配)
* 该类不应该在JDK核心类库之外使用。(源码限制只有引导类加载器可以使用该类，但可以通过java反射机制使用该类)

# 为什么命名成"Unsafe"

这是由于Unsafe类使Java语言拥有了类似C语言指针一样操作内存空间的能力， 这无疑也增加了程序发生相关指针问题的风险。 在程序中过度、不正确使用Unsafe类会使得程序出错的概率变大，使得Java这种安全的语言变得不再“安全”。

# 功能

![Unsafe功能介绍](img/Unsafe功能介绍.png)

## 内存操作

```
//TODO:cj （复制过来的）
//分配内存, 相当于C++的malloc函数,返回base地址
public native long allocateMemory(long bytes);
//扩充内存
public native long reallocateMemory(long address, long bytes);
//释放内存
public native void freeMemory(long address);
//在给定的内存块中设置值
public native void setMemory(Object o, long offset, long bytes, byte value);
//内存拷贝
public native void copyMemory(Object srcBase, long srcOffset, Object destBase, long destOffset, long bytes);
//获取给定地址值，忽略修饰限定符的访问限制。与此类似操作还有: getInt，getDouble，getLong，getChar等
public native Object getObject(Object o, long offset);
//为给定地址设置值，忽略修饰限定符的访问限制，与此类似操作还有: putInt,putDouble，putLong，putChar等
public native void putObject(Object o, long offset, Object x);
//获取给定地址的byte类型的值（当且仅当该内存地址为allocateMemory分配时，此方法结果为确定的）
public native byte getByte(long address);
//为给定地址设置byte类型的值（当且仅当该内存地址为allocateMemory分配时，此方法结果才是确定的）
public native void putByte(long address, byte x);
```

* 通常，我们在Java中创建的对象都处于堆内内存（heap）中，堆内内存是由JVM所管控的Java进程内存，并且它们遵循JVM的内存管理机制，JVM会采用垃圾回收机制统一管理堆内存。
* 与之相对的是堆外内存，存在于JVM管控之外的内存区域，Java中对堆外内存的操作，依赖于Unsafe提供的操作堆外内存的native方法。

### 使用堆外内存的原因（初步了解下，后续再深入）

* 对垃圾回收停顿的改善。由于堆外内存是直接受操作系统管理而不是JVM，所以当我们使用堆外内存时，即可保持较小的堆内内存规模。从而在GC时减少回收停顿对于应用的影响。
* 提升程序I/O操作的性能。通常在I/O通信过程中，会存在堆内内存到堆外内存的数据拷贝操作，对于需要频繁进行内存间数据拷贝且生命周期较短的暂存数据，都建议存储到堆外内存。

### 典型应用

DirectByteBuffer是Java用于实现堆外内存的一个重要类，通常用在通信过程中做缓冲池，如在Netty、MINA等NIO框架中应用广泛。DirectByteBuffer对于堆外内存的创建、使用、销毁等逻辑均由Unsafe提供的堆外内存API来实现。

#### 那么如何通过构建垃圾回收追踪对象Cleaner实现堆外内存释放呢？

[Java魔法类：Unsafe应用解析](https://tech.meituan.com/2019/02/14/talk-about-java-magic-class-unsafe.html)
TODO:cj 了解，后续再深入研究

* Cleaner
* PhantomReference
* ReferenceQueue
* Reference Handler 守护线程（后台线程并且具有最高优先级10）
* Deallocator

## CAS相关

```
/**
	*  CAS
  * @param o         包含要修改field的对象
  * @param offset    对象中某field的偏移量
  * @param expected  期望值
  * @param update    更新值
  * @return          true | false
  */
public final native boolean compareAndSwapObject(Object o, long offset,  Object expected, Object update);

public final native boolean compareAndSwapInt(Object o, long offset, int expected,int update);
  
public final native boolean compareAndSwapLong(Object o, long offset, long expected, long update);
```

什么是CAS? 即比较并替换，实现并发算法时常用到的一种技术。

CAS操作包含三个操作数——内存位置、预期原值及新值。执行CAS操作的时候，将内存位置的值与预期原值比较，如果相匹配，那么处理器会自动将该位置值更新为新值，否则，处理器不做任何操作。

我们都知道，CAS是一条CPU的原子指令（*cmpxchg*指令），不会造成所谓的数据不一致问题，Unsafe提供的CAS方法（如compareAndSwapXXX）底层实现即为CPU指令cmpxchg。

### 典型应用

CAS在java.util.concurrent.atomic相关类、Java AQS、CurrentHashMap等实现上有非常广泛的应用

AtomicInteger的实现中，

* 静态字段valueOffset即为字段value的内存偏移地址(类中的所有对象该字段偏移值都相同，所以可以用静态static修饰符)，
* valueOffset的值在AtomicInteger初始化时，在静态代码块中通过Unsafe的objectFieldOffset方法获取。
* 在AtomicInteger中提供的线程安全方法中，通过字段valueOffset的值可以定位到AtomicInteger对象中value的内存地址
* (对象的baseAddress+字段的valueOffset=value的内存地址）， 从而可以根据CAS实现对value字段的原子操作。

下图为某个AtomicInteger对象自增操作前后的内存示意图，对象的基地址baseAddress=“0x110000”，

通过baseAddress+valueOffset得到value的内存地址valueAddress=“0x11000c”；

然后通过CAS进行原子性的更新操作，成功则返回，否则继续重试，直到更新成功为止。
![Unsafe计算对象的内存地址+CAS方式](img/Unsafe计算对象的内存地址+CAS方式.png)

```java
public class AtomicInteger extends Number implements java.io.Serializable {
    private static final long serialVersionUID = 6214790243416807050L;

    // setup to use Unsafe.compareAndSwapInt for updates
    private static final Unsafe unsafe = Unsafe.getUnsafe();
    //该类中的所有对象的value字段的偏移地址都相同,所以可以用static修饰
    private static final long valueOffset;

    static {
        try {
            valueOffset = unsafe.objectFieldOffset
                (AtomicInteger.class.getDeclaredField("value"));
        } catch (Exception ex) {
            throw new Error(ex);
        }
    }
}
```

##  

TODO:cj to be done

# 应用

## java源码中的应用，系统

例如FutureTask类中的CAS，无锁并发栈

## 自己研发过程中如何使用呢

Unsafe的限制 仅在引导类加载器`BootstrapClassLoader`加载时才合法

```java
public class Unsafe {
    @CallerSensitive
    public static Unsafe getUnsafe() {
        Class<?> caller = Reflection.getCallerClass();
        // 仅在引导类加载器`BootstrapClassLoader`加载时才合法
        if (!VM.isSystemDomainLoader(caller.getClassLoader()))
            throw new SecurityException("Unsafe");
        return theUnsafe;
    }
}
```

### 方法一：

从getUnsafe方法的使用限制条件出发，通过Java命令行命令

-Xbootclasspath/a

把调用Unsafe相关方法的类A所在jar包路径追加到默认的bootstrap路径中，使得A被引导类加载器加载， 从而通过Unsafe.getUnsafe方法安全的获取Unsafe实例。

```shell
java -Xbootclasspath/a: ${path}   // 其中path为调用Unsafe相关方法的类所在jar包路径
```

### 方法二：通过反射获取单例对象theUnsafe。

```java
public class Temp {
    private static Unsafe reflectGetUnsafe() {
        try {
            Field field = Unsafe.class.getDeclaredField("theUnsafe");
            field.setAccessible(true);
            return (Unsafe) field.get(null);
        } catch (Exception e) {
            log.error(e.getMessage(), e);
            return null;
        }
    }
}
```

## netty中nio使用

# 小挑战
## 自己实现个 AtomicInteger
TODO：cj
# 资料

[Unsafe jdk8u源码](https://github.com/cj-fork-git/jdk8u/blob/master/jdk/src/share/classes/sun/misc/Unsafe.java
https://tech.meituan.com/2019/02/14/talk-about-java-magic-class-unsafe.html)
[Java魔法类：Unsafe应用解析](https://tech.meituan.com/2019/02/14/talk-about-java-magic-class-unsafe.html)