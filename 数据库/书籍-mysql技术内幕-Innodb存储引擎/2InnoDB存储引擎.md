
# 2.1InnoDB存储引擎概述
从mysql5.5版本开始是默认的表存储引擎
OLTP应用中核心表的首选存储引擎
第一个完整支持ACID事务的mysql存储引擎

# 2.2Innodb存储引擎版本
|mysql版本|innodb版本|描述|
|---|---|---|
|mysql5.1|老版本innodb||
|mysql5.1|innodb1.0.x版本||
|mysql5.5|innodb1.1.x版本||
|mysql5.6|innodb1.2.x版本||

![2Innodb各版本功能对比](img/two/2Innodb各版本功能对比.png)

# 2.3InnoDB体系架构
innodb存储引擎体系架构图重要系列
![2InnoDB存储引擎体系架构图重要系列](img/important/2InnoDB存储引擎体系架构图重要系列.png)

后台线程的主要作用是
* 负责刷新内存池中的数据，保证缓存池汇总的内存缓存的是最近的数据。
* 将已修改的数据文件刷新到磁盘文件 
* 同时保证在数据库发生异常的情况下InnoDB能恢复到正常运行状态

## 2.3.1后台线程
InnoDB存储引擎是多线程模型,后台有不同的后台线程，负责处理不同的任务

### Master Thread
核心后台线程。2.5节会详细介绍各个版本中Master Thread的工作方式

### IO Thread
Innodb 1.0版本主要有4中IO Thread，write，read，insert buffer和log IO thread.

大量使用AIO(Async IO)来处理写IO请求,io threade主要负责浙西io请求的回调(call back)处理.可以极大提高数据库性能
查看io thread线程数信息
```
#mysql5.7
SHOW VARIables like 'innodb%thread%';
+---------------------------+-------+
| Variable_name             | Value |
+---------------------------+-------+
| innodb_purge_threads      | 1     |
| innodb_read_io_threads    | 4     |
| innodb_thread_concurrency | 0     |
| innodb_thread_sleep_delay | 10000 |
| innodb_write_io_threads   | 4     |
+---------------------------+-------+
5 rows in set
Time: 0.326s

#mysql5.8
+------------------------------+-------+
| Variable_name                | Value |
+------------------------------+-------+
| innodb_parallel_read_threads | 4     |
| innodb_purge_threads         | 4     |
| innodb_read_io_threads       | 4     |
| innodb_thread_concurrency    | 0     |
| innodb_thread_sleep_delay    | 10000 |
| innodb_write_io_threads      | 4     |
+------------------------------+-------+
```
可以通过*show engine innodb status*来观察innodb的IO Thread
```
#mysql 5.7 FILE I/O部分
--------
FILE I/O
--------
I/O thread 0 state: waiting for i/o request (insert buffer thread)
I/O thread 1 state: waiting for i/o request (log thread)
I/O thread 2 state: waiting for i/o request (read thread)
I/O thread 3 state: waiting for i/o request (read thread)
I/O thread 4 state: waiting for i/o request (read thread)
I/O thread 5 state: waiting for i/o request (read thread)
I/O thread 6 state: waiting for i/o request (write thread)
I/O thread 7 state: waiting for i/o request (write thread)
I/O thread 8 state: waiting for i/o request (write thread)
I/O thread 9 state: waiting for i/o request (write thread)
Pending normal aio reads: [0, 0, 0, 0] , aio writes: [0, 0, 0, 0] ,
 ibuf aio reads:, log i/o's:, sync i/o's:
Pending flushes (fsync) log: 0; buffer pool: 0
17132022 OS file reads, 129093260 OS file writes, 126183733 OS fsyncs
0.03 reads/s, 16384 avg bytes/read, 36.86 writes/s, 35.83 fsyncs/s
-------------------------------------
```
可以看出
* IO Thread 0为insert buffer thread
* IO Thread 1为log thread
* 之后就是4个read thread,4个write thread

### Purge Thread
事务提交后，其所使用的undolog可能不再需要，因此需要来回收已经使用并分配的undo页。
* innodb1.1版本之前，purge操作仅在InnoDB存储引擎的master thread中完成
* 从innodb1.1版本开始，purge操作在独立线程中进行
  可以减轻master thread的工作，从而提高CPU的使用率
* 从innodb1.2版本开始，innodb支持多个purge thread，为了进一步加快undo页的回收
  同时由于Purge Thread需要离散地读取undo页，可以可能更进一步利用磁盘的随机读取性能(TODO:cj 这怎么理解)
支持配置purge线程池数
```
##mysql配置文件
[mysqld]
innodb_purge_threads=4
```

### Page Cleaner Thread
innodb1.2.x版本引入，作用将之前版本中脏页的刷新操作都放入到单独的线程中来完成
目的是为了减轻原Master Thread的工作及对用户查询线程的阻塞,进一步提高innodb存储引擎的性能。

## 2.3.2内存
### 1缓冲池
*问题之假如你设计innodb系统，innodb为什么引入缓冲池？*
引入缓存也算是基于磁盘的数据库系统的通用设计思路吧

innodb基于磁盘存储，记录按照页(默认每页16KB)进行管理，属于基于磁盘的数据库系统(Disk-base Database)(了解数据库系统概述部分)

因为总所周知的计算机CPU速度和磁盘速度之间的鸿沟，基于磁盘的数据库系统通常使用缓冲池技术来提高数据库的整体性能。

*问题之innodb缓冲池工作机制* 
内存区域
* 在数据库进行读取页的操作，首先将从磁盘读取的页放在缓冲池中，这个过程称为将页FIX在缓冲池
* 下次读取相同页时，首先判断该页是否在缓冲池中，如在则该页命中缓冲池，直接读取该页。否则读取磁盘上的页。
* 对于数据库中页的修改操作，首先修改在缓冲池中的页(TODO:cj如果缓冲池中没有也先读到缓冲池中嘛，应该是的)，
  然后再以一定的频率刷新到磁盘上。
* 页从缓冲池刷新回磁盘操作并不是在每次页发生更新时触发，而是通过一种称为*checkpoint*的机制刷新回磁盘，为了提高数据库的整体性能

连环问题之自然想知道checkpoint是个啥，TODO:cj后面应该有介绍

#### innodb缓冲池内存结构
* 数据页
* 索引页
* undo页
* 重做日志缓冲  
* 插入缓冲(insert buffer)
* 自适应哈希索引(adaptive hash index)
* innodb存储的锁信息(lock info)
* 数据字典信息(data dictionary)
* 等等
![2innodb缓冲池内存结构数据对象图重要系列](img/important/2innodb缓冲池内存结构数据对象图重要系列.png)


配置*innodb_buffer_pool_size* 配置缓冲池大小
*innodb_buffer_pool_instances* 配置缓冲池实例数量
```
# mysql5.7 uat
SHOW VARIables like 'innodb%buffer%';
+-------------------------------------+----------------+
| Variable_name                       | Value          |
+-------------------------------------+----------------+
| innodb_buffer_pool_chunk_size       | 134217728      |
| innodb_buffer_pool_dump_at_shutdown | ON             |
| innodb_buffer_pool_dump_now         | OFF            |
| innodb_buffer_pool_dump_pct         | 25             |
| innodb_buffer_pool_filename         | ib_buffer_pool |
| innodb_buffer_pool_instances        | 1              |
| innodb_buffer_pool_load_abort       | OFF            |
| innodb_buffer_pool_load_at_startup  | ON             |
| innodb_buffer_pool_load_now         | OFF            |
| innodb_buffer_pool_size             | 3087007744     |
| innodb_change_buffer_max_size       | 25             |
| innodb_change_buffering             | all            |
| innodb_log_buffer_size              | 8388608        |
| innodb_sort_buffer_size             | 1048576        |
+-------------------------------------+----------------+
14 rows in set
Time: 0.046s
```
可以通过show engine innodb status观察buffer pool信息
![](img/two/2show%20engine%20innodb%20status观察buffer%20pool.png)



```
# mysql5.7 uat
use information_schemal;
select pool_id,pool_size,free_buffers,database_pages from innodb_buffer_pool_stats;
+---------+-----------+--------------+----------------+
| pool_id | pool_size | free_buffers | database_pages |
+---------+-----------+--------------+----------------+
| 0       | 188416    | 1024         | 177670         |
+---------+-----------+--------------+----------------+
1 row in set
Time: 0.029s
```
### 2LRU List，Free List和Flush List
*问题之innodb缓冲池怎么对内存区域进行管理的呢?*
* 采用优化过的LRU算法(latest recented used,最近最少使用)

优化点:
* LRU列表中加入了midpoint位置。新读取到的页，虽然是最新访问的页，但并不是直接
  放入到LRU列表的首部，而是放入到LRU列表的midpoint位置。（算法成为midpoint insert strategy）

*连环问题之2与朴素的LRU算法相比，midpoint insert strategy算法有什么优势?*
因为某些SQL操作(例如索引或者数据的扫描操作)可能会读取大量页数据，仅在本次查询中用到，后面就不需要了，
如果将读取到页直接放到队首，会将真正活跃的页刷出。

innodb_old_block_pct:控制该midpoint的位置，默认值为37(差不多3/8位置)
midpoint之后的列表称为old列表，之前的列表称为new列表，简单理解new列表的页面都是最为活跃的热点数据。

连环问题之3如何才能成为LRU列表new列表的热点数据
引入了*innodb_old_blocks_time*配置项,表示页读取到mid位置后需要等待多久才会被加入LRU列表的热端,默认1000ms

```
information_schema> show variables like 'innodb_old%';
+------------------------+-------+
| Variable_name          | Value |
+------------------------+-------+
| innodb_old_blocks_pct  | 37    |
| innodb_old_blocks_time | 1000  |
+------------------------+-------+
2 rows in set
Time: 0.031s
```

缓冲池页大小默认为16KB(这个数字很重要，请记住系列)

page made young:当页从LRU列表的old部分加入到new部分，这个操作
page not made young:页没有从old部分移动到new部分的操作(可能因为innodb_old_blocks_time设置原因)

#### free list

*问题之free列表作用*
数据库刚启动时，LRU列表是空的，这时页都存放在free列表中
当需要从缓冲池中分页时，首先从free列表中查找是否有可有的空闲页，如果有则将该页从free列表中删除，放入到lru列表中
如无，则根据LRU算法，淘汰LRU列表末尾的页，将该内存空间分配给新的页

参考资料网页1，里面解释地更详细



### 3重做日志缓冲

### 4额外的内存池


# 资料
## 网页
* 1.[一看就懂的MySQL的FreeList机制](http://www.likecs.com/show-120096.html)
* 1.1[印象笔记backup](https://app.yinxiang.com/shard/s23/nl/6983422/3b174bee-d40a-4be8-a178-902745cf3bb4)