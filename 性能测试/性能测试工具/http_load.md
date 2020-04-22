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

准备url文件

```bash
$ cat first.txt
http://localhost:4000/
```

## 1.基于并发数
```
$ http_load -parallel 10 -seconds 5  first.txt
14863 fetches, 10 max parallel, 2.08127e+08 bytes, in 5.00013 seconds
14003 mean bytes/connection
2972.52 fetches/sec, 4.16242e+07 bytes/sec
msecs/connect: 0.16341 mean, 24.721 max, 0.036 min
msecs/first-response: 3.08797 mean, 36.806 max, 0.816 min
HTTP response codes:
  code 200 -- 14863
```

## 2.基于每秒速率
```
$ http_load -rate 10 -seconds 5  first.txt
49 fetches, 1 max parallel, 686147 bytes, in 5.00141 seconds
14003 mean bytes/connection
9.79724 fetches/sec, 137191 bytes/sec
msecs/connect: 0.441245 mean, 0.906 max, 0.26 min
msecs/first-response: 0.983673 mean, 1.656 max, 0.574 min
HTTP response codes:
  code 200 -- 49
```

# 实际应用场景


# 参考资料