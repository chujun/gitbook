# 基准测试(benchmark)
针对系统设计的一种压力测试

## 为什么需要基准测试
* 测试系统当前运行情况
* 规划未来业务增长
* 找出可能的瓶颈
* 测试不同硬件，软件和操作系统配置
* 重现系统某些异常
* 等等

## 基准测试的策略
**集成式基准测试**

针对整个系统的整体测试

*单组件式基准测试*

单独测试MySQL

### 明确测试目标
* 吞吐量:单位时间内的事务处理数

TPS(每秒事务处),TPM(每分钟事务数)

* 响应时间：测试任务所需的整体时间

平均响应时间，最小响应时间，最大响应时间，百分比响应时间(例如常说的99线)

* 并发性：正在工作中的并发操作/同时工作中的线程数，连接数

例如32/64/128个线程下测试

* 可扩展性


## 基准测试方法
常见错误
* 没有检查错误
* 忽略系统预热
* 测试时间太短

### 设计和规划基准测试

测试准备数据

测试规划
* 记录测试数据(系统性能和状态)
* 系统配置步骤
* 如何测量和分析结果
* 预热方案
* 等等

### 基准测试运行时长考量
* 系统预热时长
* 稳定运行时长应该足够长

### 获取系统性能和状态
* 测试结果(CPU使用率，磁盘I/O,网络流量统计,SHOW GLOBAL STATUS计数器等)
* 配置文件
* 测试指标
* 脚本
* 其他相关说明

### 获得准确的测试结果

### 运行基准测试并分析结果
自动化基准测试

* 装载数据
* 系统预热
* 执行测试
* 记录结果

TODO:cj to 无法跳转
[script/mysql_status.sh](script/mysql_status.sh)

[script/mysql_analyze.sh](script/mysql_analyze.sh)

```bash
chujun@chujundeMacBook-Pro  /tmp/benchmarks/mysql  ./mysql-status.sh
mysql: [Warning] Using a password on the command line interface can be insecure.
4
TS 1600765045.N 2020-09-22 16:57:25
mysql: [Warning] Using a password on the command line interface can be insecure.
mysql: [Warning] Using a password on the command line interface can be insecure.
mysql: [Warning] Using a password on the command line interface can be insecure.
5
TS 1600765050.N 2020-09-22 16:57:30
5
mysql: [Warning] Using a password on the command line interface can be insecure.
mysql: [Warning] Using a password on the command line interface can be insecure.
mysql: [Warning] Using a password on the command line interface can be insecure.
TS 1600765055.N 2020-09-22 16:57:35
mysql: [Warning] Using a password on the command line interface can be insecure.
mysql: [Warning] Using a password on the command line interface can be insecure.
mysql: [Warning] Using a password on the command line interface can be insecure.
5
```
```bash
 ./mysql-analyze.sh 5-sec-status-2020-09-22_05-status
#ts date time load QPS
1600765205 2020-09-22 17:00:05 2.1
1600765210 2020-09-22 17:00:10 2.0
1600765215 2020-09-22 17:00:15 2.0
1600765220 2020-09-22 17:00:20 2.0
1600765225 2020-09-22 17:00:25 2.0
1600765230 2020-09-22 17:00:30 2.1
1600765235 2020-09-22 17:00:35 2.1
1600765240 2020-09-22 17:00:40 2.1
1600765245 2020-09-22 17:00:45 2.1
1600765250 2020-09-22 17:00:50 2.1
1600765255 2020-09-22 17:00:55 2.0
1600765260 2020-09-22 17:01:00 2.0
1600765265 2020-09-22 17:01:05 2.0
1600765270 2020-09-22 17:01:10 1.9
1600765275 2020-09-22 17:01:15 2.5
```

### 2.3.6 绘图的重要性
可以用分析脚本输出作为gnuplot/R绘图的数据来源

`./mysql-analyze.sh 5-sec-status-2020-09-22_05-status>QPS-per-5seconds`

`gnuplot`

`plot "QPS-per-5seconds" using 4 w lines title "QPS"`


```
 ./mysql-analyze.sh 5-sec-status-2020-09-22_05-status>QPS-per-5seconds
 chujun@chujundeMacBook-Pro  /tmp/benchmarks/mysql  ls
5-sec-status-2020-09-21_05-innodbstatus 5-sec-status-2020-09-22_10-innodbstatus
5-sec-status-2020-09-21_05-processlist  5-sec-status-2020-09-22_10-processlist
5-sec-status-2020-09-21_05-status       5-sec-status-2020-09-22_10-status
5-sec-status-2020-09-22_04-innodbstatus QPS-per-5seconds
5-sec-status-2020-09-22_04-processlist  mysql-analyze.sh
5-sec-status-2020-09-22_04-status       mysql-status.sh
5-sec-status-2020-09-22_05-innodbstatus mysql-variables
5-sec-status-2020-09-22_05-processlist  running
5-sec-status-2020-09-22_05-status
 chujun@chujundeMacBook-Pro  /tmp/benchmarks/mysql  gnuplot

	G N U P L O T
	Version 5.4 patchlevel 0    last modified 2020-07-13

	Copyright (C) 1986-1993, 1998, 2004, 2007-2020
	Thomas Williams, Colin Kelley and many others

	gnuplot home:     http://www.gnuplot.info
	faq, bugs, etc:   type "help FAQ"
	immediate help:   type "help"  (plot window: hit 'h')

Terminal type is now 'qt'

gnuplot> plot "QPS-per-5seconds" using 4 w lines title "QPS"

Warning: slow font initializationqt.qpa.fonts: Populating font family aliases took 1095 ms. Replace uses of missing font family "Sans" with one that exists to avoid this cost.

gnuplot>
```
![gnuplot绘制图效果截图](img/gnuplot绘制图效果截图.png)

## 2.4基准测试工具
### 2.4.1集成式测试工具
* ab：Apache HTTP服务器基准测试工具。测试HTTP服务器每秒罪过处理多少请求，
只能针对单个URL进行压力测试

* http_load

* JMeter
### 2.4.2单组件式测试工具
* mysqlslap
[mysqlslap](http://dev.mysql.com/doc/refman/8.0/en/mysqlslap.html)

* MySQL Benchmark Suite(sql-bench)

* Super Smack
[Super Smack访问不了](http://vegan.net/tony/supersmack/)

* Database Test Suite
[SourceForge](http://sourceforge.net/projects/osdldbt/)
dbt2:免费的TPC-C OLTP测试工具

* Percona's TPCC-MySQL Tool(good)
作者自研的，专门为MySQL测试开发的
简单测试会用sysbench替代
[项目源码](https://launchpad.net/perconatools)
[github最新地址](https://github.com/Percona-Lab/tpcc-mysql)

* sysbench(good)
[sysbench](https://launchpad.net/sysbench)
[github最新地址](https://github.com/akopytov/sysbench)

# 2.5基准测试案例
## 2.5.1http_load
urls.txt
```
http://www.mysqlperformanceblog.com/
http://www.mysqlperformanceblog.com/page/2/
http://www.mysqlperformanceblog.com/mysql-patches/
http://www.mysqlperformanceblog.com/mysql-performance-presentations/
http://www.mysqlperformanceblog.com/2006/09/06/slow-query-log-analyzes-tools/
```

```bash
http_load -parallel 1 -seconds 10 urls.txt
```

执行结果

一个线程跑10秒
```bash
chujun@chujundeMacBook-Pro  /tmp/benchmarks/http_load  cat urls.txt
http://www.mysqlperformanceblog.com/
http://www.mysqlperformanceblog.com/page/2/
http://www.mysqlperformanceblog.com/mysql-patches/
http://www.mysqlperformanceblog.com/mysql-performance-presentations/
http://www.mysqlperformanceblog.com/2006/09/06/slow-query-log-analyzes-tools/
 chujun@chujundeMacBook-Pro  /tmp/benchmarks/http_load  http_load -parallel 1 -seconds 10 urls.txt
19 fetches, 1 max parallel, 3549 bytes, in 10 seconds
186.789 mean bytes/connection
1.9 fetches/sec, 354.9 bytes/sec
msecs/connect: 233.618 mean, 308.646 max, 195.255 min
msecs/first-response: 272.966 mean, 390.396 max, 211.834 min
HTTP response codes:
  code 302 -- 19
```

5个并发线程跑10秒
```bash
60 fetches, 5 max parallel, 9662 bytes, in 10.0006 seconds
161.033 mean bytes/connection
5.99966 fetches/sec, 966.146 bytes/sec
msecs/connect: 559.017 mean, 4285.79 max, 194.143 min
msecs/first-response: 258.62 mean, 476.163 max, 197.998 min
HTTP response codes:
  code 302 -- 60
```

根据访问速率做测试(例如每秒5次)
```bash
chujun@chujundeMacBook-Pro  /tmp/benchmarks/http_load  http_load -rate 5 -seconds 10 urls.txt
47 fetches, 3 max parallel, 7897 bytes, in 10 seconds
168.021 mean bytes/connection
4.69999 fetches/sec, 789.698 bytes/sec
msecs/connect: 208.598 mean, 272.19 max, 196.752 min
msecs/first-response: 213.182 mean, 269.172 max, 201.517 min
HTTP response codes:
  code 302 -- 47
```

根据访问速率做测试(例如每秒20次)
```bash
 chujun@chujundeMacBook-Pro  /tmp/benchmarks/http_load  http_load -rate 20 -seconds 10 urls.txt
191 fetches, 19 max parallel, 31671 bytes, in 10.0009 seconds
165.817 mean bytes/connection
19.0982 fetches/sec, 3166.81 bytes/sec
msecs/connect: 222.823 mean, 1232.14 max, 194.791 min
msecs/first-response: 219.753 mean, 708.067 max, 198.145 min
HTTP response codes:
  code 302 -- 191
```

## 2.5.2 MySQL基准测试套件
sql-bench mysql5.8这个安装目录没有找到

## 2.5.3 sysbench
sysbench不仅设计用来测试数据库性能，也可以测试运行数据库服务器性能

mac 安装sysbench
```bash
brew install sysbench
```

### sysbench的CPU基准测试
测试计算素数知道某个数所需要的时间
`sysbench --test=cpu --cpu-max-prime=20000 run`


```bash
chujun@chujundeMacBook-Pro  /tmp/benchmarks/sysbench  sysbench --test=cpu --cpu-max-prime=20000 run
WARNING: the --test option is deprecated. You can pass a script name or path on the command line without any options.
sysbench 1.0.20 (using bundled LuaJIT 2.1.0-beta2)

Running the test with following options:
Number of threads: 1
Initializing random number generator from current time


Prime numbers limit: 20000

Initializing worker threads...

Threads started!

CPU speed:
    events per second:   424.86

General statistics:
    total time:                          10.0020s
    total number of events:              4250

Latency (ms):
         min:                                    2.32
         avg:                                    2.35
         max:                                    4.05
         95th percentile:                        2.43
         sum:                                 9999.65

Threads fairness:
    events (avg/stddev):           4250.0000/0.00
```

### sysbench的文件I/O基准测试
测试系统在不同I/O负载下的性能

* 第一步：准备阶段，准备测试数据文件，生成的数据文件至少比内存大，
否则操作系统会缓存大部分数据，导致测试结果无法体现I/O密集型的工作负载.
(数据一上来就是150G,没这么多磁盘空间，搞不起)
`sysbench --test=fileio --file-total-size=20G prepare`

```bash
 chujun@chujundeMacBook-Pro  /tmp/benchmarks/sysbench  sysbench --test=fileio --file-total-size=20G prepare
WARNING: the --test option is deprecated. You can pass a script name or path on the command line without any options.
sysbench 1.0.20 (using bundled LuaJIT 2.1.0-beta2)

128 files, 163840Kb each, 20480Mb total
Creating files for the test...
Extra file open flags: (none)
Creating file test_file.0
Creating file test_file.1
Creating file test_file.2
...
Creating file test_file.125
Creating file test_file.126
Creating file test_file.127
21474836480 bytes written in 27.78 seconds (737.16 MiB/sec).
```

* 第二步：运行阶段

|IO类型测试选项|描述|
|---|---|
|seqwr|顺序写入|
|seqrewr|顺序重写|
|seqrd|顺序读取|
|rndrd|随机读取|
|rndwr|随机写入|
|rndrw|混合随机读/写|

运行文件I/O混合随机读/写基准测试
60秒混合随机读/写
`sysbench --test=fileio --file-total-size=20G --file-test-mode=rndrw --max-time=60 --max-requests=0 run`

```bash
chujun@chujundeMacBook-Pro  /tmp/benchmarks/sysbench  sysbench --test=fileio --file-total-size=20G --file-test-mode=rndrw --max-time=60 --max-requests=0 run
WARNING: the --test option is deprecated. You can pass a script name or path on the command line without any options.
WARNING: --max-time is deprecated, use --time instead
sysbench 1.0.20 (using bundled LuaJIT 2.1.0-beta2)

Running the test with following options:
Number of threads: 1
Initializing random number generator from current time


Extra file open flags: (none)
128 files, 160MiB each
20GiB total file size
Block size 16KiB
Number of IO requests: 0
Read/Write ratio for combined random IO test: 1.50
Periodic FSYNC enabled, calling fsync() each 100 requests.
Calling fsync() at the end of test, Enabled.
Using synchronous I/O mode
Doing random r/w test
Initializing worker threads...

Threads started!


File operations:
    reads/s:                      4191.56
    writes/s:                     2794.37
    fsyncs/s:                     8942.31

Throughput:
    read, MiB/s:                  65.49
    written, MiB/s:               43.66

General statistics:
    total time:                          60.0047s
    total number of events:              955667

Latency (ms):
         min:                                    0.00
         avg:                                    0.06
         max:                                   44.06
         95th percentile:                        0.18
         sum:                                59170.15

Threads fairness:
    events (avg/stddev):           955667.0000/0.00
    execution time (avg/stddev):   59.1702/0.00
```
sysbench --test=fileio --file-total-size=20G --file-test-mode=rndrw --init-rng=on --max-time=300 --max-requests=0 run

* 第三步,清除阶段，清除第一步生成的测试文件
`sysbench --test=fileio --file-total-size=20G cleanup`

```bash
 chujun@chujundeMacBook-Pro  /tmp/benchmarks/sysbench  ls
test_file.0   test_file.108 test_file.118 test_file.13  test_file.23  test_file.33  test_file.43  test_file.53  test_file.63  test_file.73  test_file.83  test_file.93
test_file.1   test_file.109 test_file.119 test_file.14  test_file.24  test_file.34  test_file.44  test_file.54  test_file.64  test_file.74  test_file.84  test_file.94
test_file.10  test_file.11  test_file.12  test_file.15  test_file.25  test_file.35  test_file.45  test_file.55  test_file.65  test_file.75  test_file.85  test_file.95
test_file.100 test_file.110 test_file.120 test_file.16  test_file.26  test_file.36  test_file.46  test_file.56  test_file.66  test_file.76  test_file.86  test_file.96
test_file.101 test_file.111 test_file.121 test_file.17  test_file.27  test_file.37  test_file.47  test_file.57  test_file.67  test_file.77  test_file.87  test_file.97
test_file.102 test_file.112 test_file.122 test_file.18  test_file.28  test_file.38  test_file.48  test_file.58  test_file.68  test_file.78  test_file.88  test_file.98
test_file.103 test_file.113 test_file.123 test_file.19  test_file.29  test_file.39  test_file.49  test_file.59  test_file.69  test_file.79  test_file.89  test_file.99
test_file.104 test_file.114 test_file.124 test_file.2   test_file.3   test_file.4   test_file.5   test_file.6   test_file.7   test_file.8   test_file.9
test_file.105 test_file.115 test_file.125 test_file.20  test_file.30  test_file.40  test_file.50  test_file.60  test_file.70  test_file.80  test_file.90
test_file.106 test_file.116 test_file.126 test_file.21  test_file.31  test_file.41  test_file.51  test_file.61  test_file.71  test_file.81  test_file.91
test_file.107 test_file.117 test_file.127 test_file.22  test_file.32  test_file.42  test_file.52  test_file.62  test_file.72  test_file.82  test_file.92
 chujun@chujundeMacBook-Pro  /tmp/benchmarks/sysbench  sysbench --test=fileio --file-total-size=20G cleanup
WARNING: the --test option is deprecated. You can pass a script name or path on the command line without any options.
sysbench 1.0.20 (using bundled LuaJIT 2.1.0-beta2)

Removing test files...
```

### sysbench的OLTP基准测试(On-Line Transaction Processing联机事务处理过程)
#### 生成测试表，超过1百万数据



```bash
sysbench --test=oltp --olpt-table-size=1000000 --mysql-db=trade_in_center --mysql-user=root prepare
WARNING: the --test option is deprecated. You can pass a script name or path on the command line without any options.
sysbench 1.0.20 (using bundled LuaJIT 2.1.0-beta2)

FATAL: Cannot find benchmark 'oltp': no such built-in test, file or module
```

执行失败,查看sysbench的文档找原因(mac地址/usr/local/Cellar/sysbench/1.0.20/READE.md)
```bash
chujun@chujundeMacBook-Pro  ~  which sysbench
/usr/local/bin/sysbench
 chujun@chujundeMacBook-Pro  ~  ll /usr/local/bin/ |grep sysbench
lrwxr-xr-x   1 chujun  admin    38B  9 23 10:49 sysbench -> ../Cellar/sysbench/1.0.20/bin/sysbench
 chujun@chujundeMacBook-Pro  ~  cd /usr/local/Cellar/sysbench/1.0.20
 chujun@chujundeMacBook-Pro  /usr/local/Cellar/sysbench/1.0.20  ls
COPYING              INSTALL_RECEIPT.json bin
ChangeLog            README.md            share
```

## 2.5.4数据库测试套件中dbt2 TPC-C测试
数据库测试套件(Database Test Suite) dbt2是一款TPC-C测试工具
TPC-C是专门针对联机交易处理系统（OLTP系统）的测试规范,用于模拟测试复杂的在线事务处理系统
测试结果包括每分钟事务数(tpmC)，以及每事务成本(Price/tmpC)
*了解*

### 2.5.5 Percona的TPCC-MySQL测试工具
相比dbt2有一些不足之处，本书作者新开发这个工具
[github最新地址](https://github.com/Percona-Lab/tpcc-mysql)

# 资料
[TPC-C](http://www.tpc.org/)
[ab](http://httpd.apache.org/docs/2.0/programs/ab.html)
[http_load](http://www.acme.com/software/http_load/)
[jmeter](http://jmeter.apache.org/)
[tpcc-mysql](https://code.launchpad.net/~percona-dev/perconatools/tpcc-mysql)