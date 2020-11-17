# my.cnf mysql配置文件参数项说明

slow_query_log 慢查询开启状态
slow_query_log_file 慢查询日志存放的位置（这个目录需要MySQL的运行帐号的可写权限，一般设置为MySQL的数据存放目录）
long_query_time 查询超过多少秒才记录,单位:秒，可填小数例如0.1表示超过0.1秒记录下来

`show variables like 'slow_query%';`查询mysql变量值

直接配置
```bash
set global slow_query_log='ON'; 
set global slow_query_log_file='/tmp/logs/mysql/data/slow.log';
set global long_query_time=1;
```

修改配置文件my.cnf，在[mysqld]下的下方加入
```
[mysqld]
slow_query_log = ON
slow_query_log_file = /tmp/logs/mysql/data/slow.log
long_query_time = 1`bash
```

测试 
```
select sleep(2);
```

观察slow.log日志内容
```
chujun@chujundeMacBook-Pro  /tmp/logs/mysql/data  tail -f slow.log
# User@Host: root[root] @ localhost [127.0.0.1]  Id:     8
# Query_time: 1.001018  Lock_time: 0.000000 Rows_sent: 1  Rows_examined: 1
use trade_in_center;
SET timestamp=1601025719;
select SLEEP(1);
# Time: 2020-09-25T09:22:06.689749Z
# User@Host: root[root] @ localhost [127.0.0.1]  Id:     8
# Query_time: 2.004589  Lock_time: 0.000000 Rows_sent: 1  Rows_examined: 1
SET timestamp=1601025724;
select SLEEP(2);


# Time: 2020-09-25T09:22:24.119005Z
# User@Host: root[root] @ localhost [127.0.0.1]  Id:     8
# Query_time: 2.000218  Lock_time: 0.000000 Rows_sent: 1  Rows_examined: 1
SET timestamp=1601025742;
select SLEEP(2);

```
# 解析和统计mysql慢查询日志工具 mysqldumpslow
具体查看mysqldumpslow -help说明(超级简单),常用参数-s,-a,-r,-t等
```
mysqldumpslow -s at,al /Users/chujun/logs/mysql/data/slow.log

Reading mysql slow query log from /Users/chujun/logs/mysql/data/slow.log
Count: 1  Time=0.39s (0s)  Lock=0.00s (0s)  Rows=10067.0 (10067), root[root]@localhost
  select * from t_user where c_city_id=N or c_user_id='S'

Count: 1  Time=0.28s (0s)  Lock=0.00s (0s)  Rows=1.0 (1), root[root]@localhost
  SELECT N

Count: 1  Time=11.00s (11s)  Lock=0.00s (0s)  Rows=300.0 (300), root[root]@localhost
  SELECT * FROM `trade_in_center`.`t_user_1q` ORDER BY `c_province_id` DESC LIMIT N OFFSET N

Count: 1  Time=0.25s (0s)  Lock=0.43s (0s)  Rows=6.0 (6), root[root]@localhost
  SELECT ordinal_position as ordinal_position,column_name as column_name,column_type AS data_type,character_set_name as character_set,collation_name as collation,is_nullable as is_nullable,column_default as column_default,extra as extra,column_name AS foreign_key,column_comment AS comment FROM information_schema.columns WHERE table_schema='S'AND table_name='S'

Count: 3  Time=0.34s (1s)  Lock=0.00s (0s)  Rows=10067.0 (30201), root[root]@localhost
  select * from t_user where c_city_id=N

Count: 2  Time=0.78s (1s)  Lock=0.00s (0s)  Rows=300.0 (600), root[root]@localhost
  SELECT * FROM `trade_in_center`.`t_user` ORDER BY `c_name` DESC LIMIT N OFFSET N
```

# 问题列表
## 1.mysql服务器启动后，其他配置项都正常，但是slow_query_log未为off
### 解决
一开始以为是配置问题，手动set global设置，提示文件slow.log无法创建(具体错误不记得了)
，手动创建出来后，再重启mysql服务器，slow_query_log就为on了
### mac保护机制无法创建目录和文件的原因,规避掉保护目录

## 2.如何定位my.cnf文件
```bash
mysql --verbose --help | grep my.cnf
    order of preference, my.cnf, $MYSQL_TCP_PORT,
/etc/my.cnf /etc/mysql/my.cnf /usr/local/etc/my.cnf ~/.my.cnf
```
一个个查看文件是否存在

# 资料
[MySQL慢查询（一） - 开启慢查询](https://www.cnblogs.com/luyucheng/p/6265594.html)
[关于Mac mysql my.cnf 配置文件](https://blog.csdn.net/StillCity/article/details/88558039)
[FILE TEMPLATE FOR MY.CNF](https://www.fromdual.com/mysql-configuration-file-sample)