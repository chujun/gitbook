#!/usr/bin/env bash
# 这个命令每秒捕获一次show global status数据,awk输出每秒查询数，线程连接数，正在执行查询的线程数
# mysqladmin extended-status(因为没有"歧义"，所以可以使用ext代替)
mysqladmin -uroot -proot ext -i1|awk '
	/Queries/{q=$4-qp;qp=$4}
	/Threads_connected/{tc=$4}
	/Threads_running/{printf "%5d %5d %5d\n",q,tc,$4}
'