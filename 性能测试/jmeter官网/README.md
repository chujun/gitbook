# 介绍
Apache出品，纯java开发的开源
压测工具

## 特性
* 支持多种多样的协议,除了最常见的http,https协议之外，官网还例举了SOAP,FTP,Database vis JDBC,TCP等等
* 测试集成套件:测试计划录制，构建和调试
* 支持命令行模型
* 完成的动态html测试报告输出
* 100%纯java开发，从而具备java应用的天生特性
* 多线程架构允许通过多个线程发出并发的请求和通过单独的线程组向不同功能发出并发的请求。
* 缓存和离线分析/重放测试结果
* 高可扩展性内核:
  Pluggable Samplers allow unlimited testing capabilities.
  Scriptable Samplers (JSR223-compatible languages like Groovy and BeanShell)
  Several load statistics may be chosen with pluggable timers.
  Data analysis and visualization plugins allow great extensibility as well as personalization.
  Functions can be used to provide dynamic input to a test or provide data manipulation.
  Easy Continuous Integration through 3rd party Open Source libraries for Maven, Gradle and Jenkins.

# JMeter不是一个浏览器
不能执行js脚本，不能渲染html页面

# download
[下载链接](https://jmeter.apache.org/download_jmeter.cgi)

```shell
wget https://mirrors.tuna.tsinghua.edu.cn/apache//jmeter/binaries/apache-jmeter-5.4.1.tgz
```

# 链接
[jmeter官方链接](https://jmeter.apache.org/)
[jmeter源码](https://github.com/apache/jmeter)
