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



# 列表

-XXmx -XX:+/-arg(bool值类型可以用+/-,todo猜测)
todo：大小感敏感嘛

|参数名|值类型|默认值|说明|分组|版本说明|
|---|---|---|---|---|---|
|mx|intx|todo|max，todo堆内存大小上限,单位|内存大小||
|mn|intx|todo|min,todo堆内存大小下限,单位|内存大小||
|ss|intx|todo|stock size,todo栈大小,例如128k|内存大小||
|PrintFlagsInitial|bool|false|表示打印出所有参数选项的默认值|输出|| 
|PrintFlagsFinal|bool|false|表示打印出所有参数选项在运行程序时生效的值|输出||
|PrintCommandLineFlags|bool|false|表示打印出被新值覆盖的参数列表|输出||
|UseTLAB|bool|true|是否使用TLAB(线程私有分配缓冲区，Thread Local Allocation Buffer)|内存分配|| 
|ZeroTLAB|bool|false|是否将新建的TLAB区域全部设置为零值，(todo为什么默认值是false，这是个可以探究的问题)|内存分配||
|FieldsAllocationStyle|intx|1|0:先对象引用，再基本类型，1：先基本类型(double/long,ints(int/float),short/char,byte/boolean),再对象引用，2:最终会转化为0和1|java内存布局|| 
|CompactFields|bool|true|是否允许子类中较窄的字段插入到父类字段间隙中|java内存布局|| 
|UseCompressedOops|bool|false|普通对象指针压缩|java内存布局||
|UseCompressedClassPointers|bool|false|类指针压缩,依赖UseCompressedOops，只有UseCompressedOops参数生效前提下才能生效|java内存布局||

# 资料

## book

* 深入java虚拟机第三版