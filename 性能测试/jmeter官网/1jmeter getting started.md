# 执行大致步骤
## 1.测试计划构建
可以使用GUI模式
## 2.加载测试运行
不要使用GUI模式
## 3.加载测试分析
HTML报告


# 系统要求
* java环境，java8以上
## 可选的
* JDK8以上


# 1.3安装
下载后直接解压缩即可，需要有java环境
目录结构如下
```
 ✘ chujun@chujundeMacBook-Pro  ~/my/mysoftware/apache-jmeter-5.4.1  tree -L 1
.
├── LICENSE
├── NOTICE
├── README.md
├── bin
├── docs
├── extras
├── lib
├── licenses
└── printable_docs
```

# 1.4运行jmeter
## GUI模式
用于创建测试脚本，录制脚本,调试脚本
启动起来有点慢，需要耐心等一小会,差不多10秒左右吧才会弹出慢吞吞的弹出jmeter窗口来
```shell
cd ~/my/mysoftware/apache-jmeter-5.4.1/bin
./jmeter
```
## CLI模式
用于执行测试脚本
