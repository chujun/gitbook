# 常见脚本命令

## Linux系统查看当前Tcp/ip连接状态和对应个数

```
 ✘ chujun@MacBook-Pro-4  ~  netstat -na | awk '/^tcp/ {++s[$NF]} END {for(a in s) print a,s[a]}'
LISTEN 36
FIN_WAIT_2 1
LAST_ACK 1
CLOSE_WAIT 4
CLOSED 1
TIME_WAIT 1
ESTABLISHED 60
```
