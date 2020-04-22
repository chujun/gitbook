# http_load
# 官网
[官网](http://www.acme.com/software/http_load/)

# 说明
一款多线程http测试web服务器性能工具，可以测试服务器的吞吐量



# 安装

```css
tar xzvfhttp_load-12mar2006.tar.gz
make
make install
```

%accordion%http_load安装%accordion%

![http_load安装过程](img/http_load安装过程.png)

%/accordion%

## 验证安装成功，执行http_load命令
```bash
usage:  http_load [-checksum] [-throttle] [-proxy host:port] [-verbose] [-timeout secs] [-sip sip_file]
            -parallel N | -rate N [-jitter]
            -fetches N | -seconds N
            url_file
One start specifier, either -parallel or -rate, is required.
One end specifier, either -fetches or -seconds, is required.
```
 
## 常见错误
### 当man失败是不影响功能使用
```
m -f /usr/local/bin/http_load
cp http_load /usr/local/bin
rm -f /usr/local/man/man1/http_load.1
cp http_load.1 /usr/local/man/man1
cp: /usr/local/man/man1: No such file or directory
make: *** [install] Error 1
```

# 常见使用
## 常见参数
```
-parallel 简写-p ：含义是并发的用户进程数。
-rate 简写-r ：含义是每秒的访问频率

-fetches 简写-f ：含义是总计的访问次数
-seconds 简写-s ：含义是总计的访问时间
```

## 使用示例
```
http_load -r 10 -s 5 first.txt
49 fetches, 1 max parallel, 686147 bytes, in 5.00346 seconds
14003 mean bytes/connection
9.79323 fetches/sec, 137135 bytes/sec
msecs/connect: 0.438143 mean, 0.647 max, 0.225 min
msecs/first-response: 1.69065 mean, 11.311 max, 0.977 min
HTTP response codes:
  code 200 -- 49
```

## 结果分析
```
1. 49 fetches, 1 max parallel, 686147 bytes, in 5.00346 seconds 
  本次测试共发起了49个请求，最大并发数为1,总传输字节数686147字节，总运行时间为5.00346秒

2. 14003 mean bytes/connection
  每一个连接的传输字节数 686147/49=14003 bytes
3. 9.79323 fetches/sec, 137135 bytes/sec
  每秒请求数9.79323，每秒字节数137135
4. msecs/connect: 0.438143 mean, 0.647 max, 0.225 min
  每个连接的平均响应时间:0.438143,最大响应时间为0.647，最小响应时间为0.225 
5. msecs/first-response: 1.69065 mean, 11.311 max, 0.977 min

6. HTTP response codes:
      code 200 -- 49
   http响应code为200的数量为49，和总请求数一致   
```
特殊说明：这里，我们一般会关注到的指标是fetches/sec、msecs/connect
他们分别对应的常用性能指标参数
Qpt-每秒响应用户数和response time，每连接响应用户时间。

### 准备url文件，可以包含多个url

```bash
$ cat first.txt
http://localhost:4000/
```

### 1.基于并发数
http_load -parallel 10 -seconds 5  first.txt
```
$ http_load -p 10 -s 5  first.txt
14863 fetches, 10 max parallel, 2.08127e+08 bytes, in 5.00013 seconds
14003 mean bytes/connection
2972.52 fetches/sec, 4.16242e+07 bytes/sec
msecs/connect: 0.16341 mean, 24.721 max, 0.036 min
msecs/first-response: 3.08797 mean, 36.806 max, 0.816 min
HTTP response codes:
  code 200 -- 14863
```

### 2.基于每秒速率
http_load -rate 10 -seconds 5  first.txt
```
$ http_load -r 10 -s 5 first.txt
49 fetches, 1 max parallel, 686147 bytes, in 5.00141 seconds
14003 mean bytes/connection
9.79724 fetches/sec, 137191 bytes/sec
msecs/connect: 0.441245 mean, 0.906 max, 0.26 min
msecs/first-response: 0.983673 mean, 1.656 max, 0.574 min
HTTP response codes:
  code 200 -- 49
```

# 实际应用场景


# TODO
* 能测试get请求，post请求还不知道怎么配置


# 参考资料
[http_load使用详解](https://www.cnblogs.com/shijingjing07/p/6539179.html)