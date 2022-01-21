# jvm虚拟机参数大梳理



# 输出
```shell
#vm args
-XX:+PrintFlagsInitial -XX:+PrintFlagsFinal
```



# 列表
-XXmx
-XX:+/-arg(bool值类型可以用+/-,todo猜测)
todo：大小感敏感嘛

|参数名|值类型|默认值|说明|分组|版本说明|
|---|---|---|---|---|---|
|mx|intx||todo堆内存大小上限,单位|内存大小||
|mn|intx||todo堆内存大小下限,单位|内存大小||
|ss|intx||todo栈大小,例如128k|内存大小||
|PrintFlagsInitial|bool|false|表示打印出所有参数选项的默认值|输出||
|PrintFlagsFinal|bool|false|表示打印出所有参数选项在运行程序时生效的值|输出||
|UseTLAB|bool|true|是否使用TLAB(线程私有分配缓冲区，Thread Local Allocation Buffer)|内存分配||
|ZeroTLAB|bool|false|是否将新建的TLAB区域全部设置为零值，(todo为什么默认值是false，这是个可以探究的问题)|内存分配||



# 资料
## book
* 深入java虚拟机第三版