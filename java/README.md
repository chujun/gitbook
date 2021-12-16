# 介绍

# 安装
## mac安装jdk11和jdk8
### mac homebrew安装jdk11
#### 安装java11
##### brew search java
```shell
==> Formulae
app-engine-java            java                       java11 ✔                   javarepl                   libreadline-java
google-java-format         java-service-wrapper       javacc                     jslint4java                pdftk-java

==> Casks
charles-applejava     java-beta             java6                 eclipse-java          eclipse-javascript    oracle-jdk-javadoc

If you meant "java" specifically:
It was migrated from homebrew/cask to homebrew/core.
```
##### brew info java11
```shell
openjdk@11: stable 11.0.12 (bottled) [keg-only]
Development kit for the Java programming language
https://openjdk.java.net/
/usr/local/Cellar/openjdk@11/11.0.12 (679 files, 297.9MB)
  Poured from bottle on 2021-12-16 at 17:54:43
From: https://github.com/Homebrew/homebrew-core/blob/HEAD/Formula/openjdk@11.rb
License: GPL-2.0-only
==> Dependencies
Build: autoconf ✘
==> Caveats
For the system Java wrappers to find this JDK, symlink it with
  sudo ln -sfn /usr/local/opt/openjdk@11/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk-11.jdk

openjdk@11 is keg-only, which means it was not symlinked into /usr/local,
because this is an alternate version of another formula.

If you need to have openjdk@11 first in your PATH, run:
  echo 'export PATH="/usr/local/opt/openjdk@11/bin:$PATH"' >> ~/.zshrc

For compilers to find openjdk@11 you may need to set:
  export CPPFLAGS="-I/usr/local/opt/openjdk@11/include"

==> Analytics
install: 42,156 (30 days), 131,708 (90 days), 452,882 (365 days)
install-on-request: 20,500 (30 days), 59,275 (90 days), 196,400 (365 days)
build-error: 447 (30 days)
```
##### brew install java11
##### 查询java_home支持的版本
/usr/libexec/java_home -V
```shell
Matching Java Virtual Machines (1):
    1.8.0_211 (x86_64) "Oracle Corporation" - "Java SE 8" /Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home
/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home
```

##### 暴露java11对外命令行可使用 
一开始只有jdk8,那么如何让jdk11暴露出来呢，其实brew install java11命令中已经提示了
如果希望java wrappers找到java11，则需要在/Library/Java/JavaVirtualMachines目录建立一个链接到java11实际安装目录
```shell
sudo ln -sfn /usr/local/opt/openjdk@11/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk-11.jdk
```
此时再查看下java_home中可支持的java版本
```shell
/usr/libexec/java_home -V
Matching Java Virtual Machines (2):
    11.0.12 (x86_64) "Homebrew" - "OpenJDK 11.0.12" /usr/local/Cellar/openjdk@11/11.0.12/libexec/openjdk.jdk/Contents/Home
    1.8.0_211 (x86_64) "Oracle Corporation" - "Java SE 8" /Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home
/usr/local/Cellar/openjdk@11/11.0.12/libexec/openjdk.jdk/Contents/Home
```
java11匹配方式
```shell
/usr/libexec/java_home -v1.11
/usr/local/Cellar/openjdk@11/11.0.12/libexec/openjdk.jdk/Contents/Home
```
java8匹配方式
```shell
/usr/libexec/java_home -v1.8
/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home
```

##### 在zsh shell中的.zshrc配置文件配置java多版本
 ```shell
export JAVA_8_HOME=$(/usr/libexec/java_home -v1.8)
export JAVA_11_HOME=$(/usr/libexec/java_home -v1.11)

alias jdk8="export JAVA_HOME=$JAVA_8_HOME"
alias jdk11="export JAVA_HOME=$JAVA_11_HOME"
# default jdk8
jdk8

 ```
大工完成

### mac homebrew安装jdk8
因为jdk8 oracle不直接支持维护了,所以没有java8，而在openjdk中有维护

```shell
brew search openjdk
brew info openjdk@8
brew openjdk@8
```
后续流程与安装java11相同，就不再复述了


空空如也