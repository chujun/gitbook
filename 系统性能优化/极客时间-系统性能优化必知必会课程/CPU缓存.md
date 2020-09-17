# CPU多级缓存
# tag 缓存行
# CPU多级缓存架构
[CPU多级缓存架构](img/CPU多级缓存架构.jpg)
两个一级缓存(index0,index1),分别对待指令和数据
# 各个系统如何查看缓存大小
## linux
```bash
cat /sys/devices/system/cpu/cpu0/cache/index0/size
32K
cat /sys/devices/system/cpu/cpu0/cache/index1/size
32K
cat /sys/devices/system/cpu/cpu0/cache/index2/size
256K
cat /sys/devices/system/cpu/cpu0/cache/index3/size
40960K
```
![linux-cpu-cache-size](img/linux-cpu-cache-size.png)
## window
* wmic cup命令
* CPU-Z知名工具
# mac
```bash
sysctl machdep.cpu|grep 
cachemachdep.cpu.cache.linesize: 64
machdep.cpu.cache.L2_associativity: 4
machdep.cpu.cache.size: 256
```
大小计算???
64bit*4*256=8K
参考这个计算公式
[一篇对伪共享、缓存行填充和CPU缓存讲的很透彻的文章](https://blog.csdn.net/qq_27680317/article/details/78486220)

# 缓存命中率
## demo 以不同方式访问二维数组 与CPU缓存行有关系
因为二维数组内存布局特征 array 所占用的内存是连续的，比如若长度 N 的值为 2，那么内存中从前至后各元素的顺序是：
```
array[0][0]，array[0][1]，array[1][0]，array[1][1]。
```
```
int array[N][N];

for(i = 0; i < N; i+=1) { 
    for(j = 0; j < N; j+=1) { 
        array[i][j] = 0; 
    } 
}

for(j = 0; j < N; j+=1) { 
    for(n = 0; n < N; n+=1) { 
        array[j][i] = 0; 
    } 
}
```
## array[i][j]和array[j][i]遍历访问数组元组，哪一种性能更快
如果用 array[i][j]访问数组元素，则完全与上述内存中元素顺序一致，因此访问 array[0][0]时，缓存已经把紧随其后的 3 个元素也载入了，

后者此时内存是跳跃访问的，如果 N 的数值很大，那么操作 array[j][i]时，是没有办法把 array[j+1][i]也读入缓存的。

还有问题
* 为什么两者的执行时间有约 7、8 倍的差距呢？
* 载入 array[0][0]元素时，缓存一次性会载入多少元素呢？
其实这两个问题的答案都与 CPU Cache Line 相关，
它定义了缓存一次载入数据的大小，
Linux 上你可以通过 coherency_line_size 配置查看它，通常是 64 字节

再来看为什么执行时间相差 8 倍。在二维数组中，其实第一维元素存放的是地址，
第二维存放的才是目标元素。由于 64 位操作系统的地址占用 8 个字节
（32 位操作系统是 4 个字节），
因此，每批 Cache Line 最多也就能载入不到 8 个二维数组元素，
所以性能差距大约接近 8 倍。



## 提升指令缓存命中率
### demo 输出大于60岁的人员列表，并按照岁数大小排序
两种算法大列表情况下比较一种先排序条件遍历，另一种先条件遍历然后排序那种效率高?
* CPU分支预测器

当代码中出现 if、switch 等语句时，意味着此时至少可以选择跳转到两段不同的指令去执行。
如果分支预测器可以预测接下来要在哪段代码执行（比如 if 还是 else 中的指令），
就可以提前把这些指令放在缓存中，CPU 执行时就会很快。当数组中的元素完全随机时，
分支预测器无法有效工作，而当 array 数组有序时，分支预测器会动态地根据历史命中数据对未来进行预测，
命中率就会非常高。究竟有多高呢？我们还是用 Linux 上的 perf 来做个验证。
使用 -e 选项指明 branch-loads 事件和 branch-load-misses 事件，
它们分别表示分支预测的次数，以及预测失败的次数。通过 L1-icache-load-misses
 也能查看到一级缓存中指令的未命中情况。

[first](https://static001.geekbang.org/resource/image/29/72/2902b3e08edbd1015b1e9ecfe08c4472.png)
[second](https://static001.geekbang.org/resource/image/95/60/9503d2c8f7deb3647eebb8d68d317e60.png)

## 提升多核CPU缓存命中率
基本认识:虽然三级缓存面向所有核心，但一、二级缓存是每颗核心独享的
[伪共享和缓存行填充,从Java6,Java7到Java8](https://www.cnblogs.com/Binhua-Liu/p/5620339.html)
[一篇对伪共享、缓存行填充和CPU缓存讲的很透彻的文章](https://blog.csdn.net/qq_27680317/article/details/78486220)
### 缓存行在多核CPU下的伪共享问题
### 缓存行填充
### 因此，操作系统提供了将进程或者线程绑定到某一颗 CPU 上运行的能力。
如 Linux 上提供了 sched_setaffinity 方法实现这一功能
Perf 工具也提供了 cpu-migrations 事件，它可以显示进程从不同的 CPU 核心上迁移的次数。

# 资料
如果你在用 Linux 操作系统，可以通过一个名叫 Perf 的工具直观地验证缓存命中的情况
[perf工具使用案例参考](http://www.brendangregg.com/perf.html)
[geektime branch_predict perf](https://github.com/russelltao/geektime_distrib_perf/tree/master/1-cpu_cache/branch_predict)