#
纯粹的mybatis spring boot项目

mybatis的操作主要分为两大阶段

* 1.mybatis初始化阶段,用来完成mybatis运行环境的准备工作，只在mybatis启动时运行一次
* 2.数据读写阶段。该阶段由业务系统数据读写操作触发，完成CRUD等数据库操作

# 3.1初始化阶段追踪