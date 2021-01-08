# 命令概述 
该命令展示的不是当前状态，而是过去某个时间范围内innodb存储引擎的状态，例如
`Per second averages calculated from the last 35 seconds`
表示信息为过去35秒的数据库状态

# BUFFER POOL AND MEMORY 部分
## LRU列表以及Free列表
![](img/attach1/attach1-解析之buffer%20pool%20LRU%20page.png)
解析内容
buffer pool size表示缓冲池总页数,*16KB就是缓冲池的大小
free buffer：表示当前列表页的数量
database pages表示LRU列表中页的数量
一般 free buffer+database pages<buffer pool size
![](img/attach1/attach1-内容之buffer%20pool%20LRU%20page.png)
说明见2InnoDB存储引擎.md的2.3.2内存
