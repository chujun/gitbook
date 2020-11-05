# 目标
## 快速
* 1分钟甚至几十秒生成千万级别以上数量测试表 
## 尽可能模拟生产环境数据
* 随机性

# 手段
## 1.编写程序批量插库(研发效率低，性能也不高,不推荐)
## 2.变成存储过程和函数执行
## 3.临时数据表方式执行(简单，快速)

## 3方式实验
```sql
CREATE TABLE `t_user` (
 `id` int(11) NOT NULL AUTO_INCREMENT,
 `c_user_id` varchar(36) NOT NULL DEFAULT '',
 `c_name` varchar(22) NOT NULL DEFAULT '',
 `c_province_id` int(11) NOT NULL,
 `c_city_id` int(11) NOT NULL,
 `create_time` datetime NOT NULL,
 PRIMARY KEY (`id`),
 KEY `idx_user_id` (`c_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 1.临时数据表tmp_table结构
```sql
CREATE TABLE tmp_table (
	id INT,
	PRIMARY KEY (id)
);
```

### 2.python/bash 生成1000w记录的数据文件()
```
python(推荐): python -c "for i in range(1, 1+1000000): print(i)" > base.txt
bash(不推荐，会比较慢): bash i=1; while [ $i -le 1000000 ]; do echo $i; let i+=1; done  > base.txt
```
### 3.导入数据到临时表tmp_table中
```sql
mysql> load data infile '/tmp/data/base.txt' replace into table tmp_table;
Query OK, 1000000 rows affected (2.55 sec)
Records: 1000000 Deleted: 0 Skipped: 0 Warnings: 0
```
千万级别数据60秒左右插入完成

#### 问题 这里可能会提示load方法执行异常
解决方案见资料2->导出数据提示–secure-file-priv选项问题的解决方法

### 4.以临时表为基础数据，插入数据到t_user
```sql
mysql> INSERT INTO t_user SELECT id,uuid(),CONCAT('userNickName', id),FLOOR(Rand() * 1000),
FLOOR(Rand() * 100),NOW() FROM tmp_table;
Query OK, 1000000 rows affected (10.37 sec)
Records: 1000000 Duplicates: 0 Warnings: 0
```
本机mac一千万数据执行差不多执行了3分钟左右

### 5.更新创建时间字段让插入的创建时间更加随机
```sql
UPDATE t_user SET create_time=date_add(create_time, interval FLOOR(1 + (RAND() * 7)) year);

Query OK, 1000000 rows affected (5.21 sec)
Rows matched: 1000000 Changed: 1000000 Warnings: 0

mysql> UPDATE t_user SET create_time=date_add(create_time, interval FLOOR(1 + (RAND() * 7)) year);


Query OK, 1000000 rows affected (4.77 sec)
Rows matched: 1000000 Changed: 1000000 Warnings: 0
```
# 资料
[MySQL如何快速的创建千万级测试数据](https://www.jb51.net/article/161712.htm)
[mysql5.5导出数据提示–secure-file-priv选项问题的解决方法](https://blog.csdn.net/jav0a0/article/details/90712089)