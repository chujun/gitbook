# jvm虚拟机参数大梳理



# 输出
## 引申:一个简单问题:如何判断一个jvm参数默认值和实际生效值
利用两个jvm参数可以看出来

```shell
#vm args
-XX:+PrintFlagsInitial -XX:+PrintFlagsFinal -XX:+PrintCommandLineFlags
```

## 对输出结果说明

```shell
-XX:+PrintFlagsFinal -XX:FieldsAllocationStyle=0 -XX:-UseCompressedOops -XX:-UseCompressedClassPointers -XX:+CompactFields -XX:-ZeroTLAB
```

* 第三列有":"表示设置了该jvm参数，而非标识和默认值不一样（jdk8 CompactFields默认值也是true）

```shell
bool CompactFields                            := true                                {product}
intx CompilationPolicyChoice                   = 3                                   {product}
```

![jvmPrint.md](out/jvmPrint.md)

# 关于参数设置的一些说明
## HotSpot虚拟机两类参数类型
Java HotSpot VM的官方文档

|参数类型|类型|描述|格式|
|---|---|---|---|
|-X|非标准参数|不是虚拟机规范规定的,不是所有其他虚拟机都支持这些参数|-Xms20m|
|-XX|稳定参数|是虚拟机规范规定的|-XX:+PrintFlagsInitial,-XX:FieldsAllocationStyle=0|
严格区分大小写，不合法的jvm参数，运行时会直接报错，无法识别该jvm参数
todo:cj 前者小写后者大写？（目前看起来的demo是这样子的）

## 
HotSpot虚拟机针对-XX类型参数
boolean类型:-XX:+/-arg,+表示开启，-表示关闭

# 如果输出一个正在运行的java应用配置的jvm参数
使用jvm工具jinfo -flags
```shell
#例如测试环境我们的服务tic，28是jps后得到的进程id
jinfo -flags 28
```
输出如下
```shell
Attaching to process ID 28, please wait...
Debugger attached successfully.
Server compiler detected.
JVM version is 25.91-b14
Non-default VM flags: -XX:CICompilerCount=4 -XX:CMSInitiatingOccupancyFraction=75 -XX:+DisableExplicitGC -XX:HeapDumpPath=null -XX:InitialHeapSize=2147483648 -XX:MaxHeapSize=2147483648 -XX:MaxNewSize=697892864 -XX:MaxTenuringThreshold=6 -XX:MinHeapDeltaBytes=196608 -XX:NewSize=697892864 -XX:OldPLABSize=16 -XX:OldSize=1449590784 -XX:-OmitStackTraceInFastThrow -XX:+PrintGC -XX:+PrintGCDateStamps -XX:+PrintGCDetails -XX:+PrintGCTimeStamps -XX:+PrintHeapAtGC -XX:+UseCMSInitiatingOccupancyOnly -XX:+UseCompressedClassPointers -XX:+UseCompressedOops -XX:+UseConcMarkSweepGC -XX:+UseParNewGC
Command line:  -Xmx2048M -Xms2048M -XX:-OmitStackTraceInFastThrow -XX:+UseConcMarkSweepGC -XX:CMSInitiatingOccupancyFraction=75 -XX:+UseCMSInitiatingOccupancyOnly -XX:+PrintHeapAtGC -XX:+PrintGC -XX:+PrintGCDetails -XX:+PrintGCTimeStamps -XX:+PrintGCDateStamps -Xloggc:/data/log/trade-in-center-service-gc.txt -XX:+DisableExplicitGC -XX:HeapDumpPath=/data/log/trade-in-center-service.dump -javaagent:/usr/src/myapp/aihuishou-agent.jar -javaagent:/usr/src/myapp/skywalking-agent/skywalking-agent.jar -javaagent:/usr/src/myapp/transmittable-thread-local-2.10.2.jar -javaagent:/usr/src/myapp/jmx_prometheus_javaagent-0.3.1.jar=18080:/usr/src/myapp/config.yaml
```
[参考官方文档jvm options说明](https://www.oracle.com/java/technologies/javase/vmoptions-jsp.html)
# 列表
## verbose
|参数名|值类型|默认值|说明|分组|版本说明|
|---|---|---|---|---|---|
|-verbose:class|||监控类的加载和卸载|类加载卸载||
|–verbose:gc|||输出gc时的信息，todo|gc日志||

## 普通
|参数名|值类型|默认值|说明|分组|版本说明|
|---|---|---|---|---|---|
|mx|intx|todo|max，todo堆内存大小上限,单位|内存大小||
|mn|intx|todo|min,todo堆内存大小下限,单位|内存大小||
|ss|intx|todo|stock size,todo java方法栈容量大小,例如128k|内存大小||
|PrintFlagsInitial|bool|false|表示打印出所有参数选项的默认值|输出|| 
|PrintFlagsFinal|bool|false|表示打印出所有参数选项在运行程序时生效的值|输出||
|PrintCommandLineFlags|bool|false|表示打印出被新值覆盖的参数列表|输出||
|UseTLAB|bool|true|是否使用TLAB(线程私有分配缓冲区，Thread Local Allocation Buffer)|内存分配|| 
|ZeroTLAB|bool|false|是否将新建的TLAB区域全部设置为零值，(todo为什么默认值是false，这是个可以探究的问题)|内存分配||
|FieldsAllocationStyle|intx|1|0:先对象引用，再基本类型，1：先基本类型(double/long,ints(int/float),short/char,byte/boolean),再对象引用，2:最终会转化为0和1|java内存布局|| 
|CompactFields|bool|true|是否允许子类中较窄的字段插入到父类字段间隙中|java内存布局|| 
|UseCompressedOops|bool|false|普通对象指针压缩|java内存布局||
|UseCompressedClassPointers|bool|false|类指针压缩,依赖UseCompressedOops，只有UseCompressedOops参数生效前提下才能生效|java内存布局||
|HeapDumpOnOutOfMemoryError|bool|false|OOM异常时是否存储堆栈转储文件|OOM异常||
|MetaspaceSize|intx|todo|元空间初始gc阈值(而非元空间的初始大小),达到改值时触发垃圾回收期进行gc(类型卸载),同时会动态调整该值大小|元空间|jdk8+|
|MaxMetaspaceSize|uintx|todo|,元空间大小上限-1表示不限制大小，只受限于内存大小|元空间|jdk8+|
|MinMetaspaceFreeRatio|uintx|40|todo|元空间|jdk8+|
|MaxMetaspaceFreeRatio|uinx|70|todo|元空间|jdk8+|
|MaxDirectMemorySize|uinx|0|直接内存大小，默认不限制和Java堆最大值一致|直接内存||
|TraceClassLoading|bool|false|跟踪类的加载，与-verbose:class相比，少了类的卸载信息|类加载卸载||
|TraceClassUnLoading|bool|false|跟踪类的卸载，与-verbose:class相比，少了类的加载信息|类加载卸载||
# 资料

## book

* 深入java虚拟机第三版