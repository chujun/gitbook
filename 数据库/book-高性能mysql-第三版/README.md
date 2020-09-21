# book-高性能mysql-第三版

## 第一章概念梳理
* 并发问题
并发问题--->锁--->锁类型(读锁，写锁)--->锁粒度---->锁策略(表锁，行锁)

* 事务
事务 -> ACID(原子性，一致性，隔离性，持久性)
->隔离级别(未提交读，提交读，可重复读,可串行化)
->脏读，不可重复读，幻读
-->多版本并发控制(MVCC,Multiversion Concurrency Control)

* 死锁
死锁 ->死锁检测/死锁超时机制->死锁回滚算法

* 事务日志
追加(顺序IO快于随机IO)->预写式日志(Write-Ahead Logging)

* 事务提交

* MVCC
MVCC实现->innodb通过记录额外列实现(创建行和删除行)

* 存储引擎
innodb
MVCC->可重复读->间隙锁解决幻读
MyISAM(了解即可)


聚簇索引


# 资料
[高性能mysql书籍代码样例](http://www.highperfmysql.com/)
[msql official dococument](https://dev.mysql.com/doc)
