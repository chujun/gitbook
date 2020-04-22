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



# 使用

