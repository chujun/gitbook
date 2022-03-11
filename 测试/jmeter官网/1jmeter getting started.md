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

./jmeter

```
-n
This specifies JMeter is to run in cli mode(nongui)
-t
[name of JMX file that contains the Test Plan].
-l
[name of JTL file to log sample results to].
-j
[name of JMeter run log file].
-r
Run the test in the servers specified by the JMeter property "remote_hosts"
-R
[list of remote servers] Run the test in the specified remote servers
-g
[path to CSV file] generate report dashboard only
-e
generate report dashboard after load test
-o
output folder where to generate the report dashboard after load test. Folder must not exist or be empty
The script also lets you specify the optional firewall/proxy server information:

-H
[proxy server hostname or ip address]
-P
[proxy server port]

```

## 服务器模式启动
```shell
jmeter-server -H my.proxy.server -P 8000
```

示例
```shell
jmeter -n -t my_test.jmx -l log.jtl -H my.proxy.server -P 8000
```

## 1.4.1JMeter Classpath
自定义扩展jmeter的类库，jmeter会自动从下面的路径加载库
```
JMETER_HOME/lib
    used for utility jars
JMETER_HOME/lib/ext
    used for JMeter components and plugins
```

## 1.4.2从模板里创建测试计划
GUI方式

## 1.4.6不同类型的属性定义
-D[prop_name]=[value]
defines a java system property value.
-J[prop_name]=[value]
defines a local JMeter property.
-G[prop_name]=[value]
defines a JMeter property to be sent to all remote servers.
-G[propertyfile]
defines a file containing JMeter properties to be sent to all remote servers.
-L[category]=[priority]
overrides a logging setting, setting a particular category to the given priority level.

1.4.8 jmeter命令行完整参数选项
```
--?
        print command line options and exit
    -h, --help
        print usage information and exit
    -v, --version
        print the version information and exit
    -p, --propfile <argument>
        the jmeter property file to use
    -q, --addprop <argument>
        additional JMeter property file(s)
    -t, --testfile <argument>
        the jmeter test(.jmx) file to run
    -l, --logfile <argument>
        the file to log samples to
    -i, --jmeterlogconf <argument>
        jmeter logging configuration file (log4j2.xml)
    -j, --jmeterlogfile <argument>
        jmeter run log file (jmeter.log)
    -n, --nongui
        run JMeter in nongui mode
    -s, --server
        run the JMeter server
    -H, --proxyHost <argument>
        Set a proxy server for JMeter to use
    -P, --proxyPort <argument>
        Set proxy server port for JMeter to use
    -N, --nonProxyHosts <argument>
        Set nonproxy host list (e.g. *.apache.org|localhost)
    -u, --username <argument>
        Set username for proxy server that JMeter is to use
    -a, --password <argument>
        Set password for proxy server that JMeter is to use
    -J, --jmeterproperty <argument>=<value>
        Define additional JMeter properties
    -G, --globalproperty <argument>=<value>
        Define Global properties (sent to servers)
        e.g. -Gport=123
         or -Gglobal.properties
    -D, --systemproperty <argument>=<value>
        Define additional system properties
    -S, --systemPropertyFile <argument>
        additional system property file(s)
    -f, --forceDeleteResultFile
        force delete existing results files and web report folder if present before starting the test
    -L, --loglevel <argument>=<value>
        [category=]level e.g. jorphan=INFO, jmeter.util=DEBUG or com.example.foo=WARN
    -r, --runremote
        Start remote servers (as defined in remote_hosts)
    -R, --remotestart <argument>
        Start these remote servers (overrides remote_hosts)
    -d, --homedir <argument>
        the jmeter home directory to use
    -X, --remoteexit
        Exit the remote servers at end of test (CLI mode)
    -g, --reportonly <argument>
        generate report dashboard only, from a test results file
    -e, --reportatendofloadtests
        generate report dashboard after load test
    -o, --reportoutputfolder <argument>
        output folder for report dashboard
```

# 1.5配置jmeter
0.在JMETER_HOME/bin/system.properties中配置系统属性
1.在JMETER_HOME/bin/user.properties中配置属性
2.在jmeter命令中指定-p jmeter.properties属性文件配置属性

## 各种属性加载顺序
* 1.-p propfile
* 2.jmeter.properties (or the file from the -p option) is then loaded
* 3.-j logfile
* 4.Logging is initialised
* 5.user.properties is loaded
* 6.system.properties is loaded
* 7.all other command-line options are processed
