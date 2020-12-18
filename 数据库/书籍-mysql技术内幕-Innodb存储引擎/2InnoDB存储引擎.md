
# 2.1InnoDB存储引擎概述
从mysql5.5版本开始是默认的表存储引擎
第一个完整支持ACID事务的mysql存储引擎

# 2.2Innodb存储引擎版本

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

大量使用AIO(Async IO)来处理写IO请求,可以极大提高数据库性能
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
事务提交后，其所使用的undolog可能不再时序，因此需要来回收已经使用并分配的undo页。
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

### 2LRU List，Free List和Flush List

### 3重做日志缓冲

### 4额外的内存池