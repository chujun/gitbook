#



# 名句
* Java与C++之间有一堵由内存动态分配和垃圾收集技术所围成的高墙，墙外面的人想进去，墙里面的人却想出来。

# 小实验
## 自己编译openjdk
这儿以openjdk12为例
### 源码地址
[openjdk12](https://hg.openjdk.java.net/jdk/jdk12)
* 源码zip包下载（比较大，几百兆，几万个文件）,解压缩
* 建立github仓库，推送上去

```shell
git init .
git add .
git commit -m "init project"
git remote add origin git@github.com:cj-fork-git/openjdk12-copy.git
git push --set-upstream origin master
```

### mac环境准备
* 1.安装最新版本xcode
* 2.安装最新版本Xcode Command Line Tools [官网文档](https://mac.install.guide/commandlinetools/3.html)
* 3.需要依赖（n-1）上一个大版本的jdk11（称为Bootstrap JDK，用来编译openjdk中的java代码）

这1和2两个SDK提供了OpenJDK所需的CLang编译器以及Makefile中用到的其他外部命令
```shell
xcode-select -p
/Applications/Xcode.app/Contents/Developer
```
表示安装完成

### linux环境准备
略去，见书籍

### 编译命令
bash configure [options]

```shell
bash configure --enable-debug --with-jvm-variants=server
```

--disable-warnings-as-errors：禁止将警告当成build错误，这样子警告不会影响build过程失败

bash configure --with-jvm-variants=server --disable-warnings-as-errors

make print-configuration打印当前configure的options输出在当前命令行中






# 本书面向读者
初级程序员 xxx
中高级程序员 get


# 书籍信息
* 深入理解Java虚拟机：JVM高级特性与最佳实践（第3版）
* 周志明
* 出版社：机械工业出版社
* 出版时间：2019-11
* ISBN：9787111641247

# 资料
## 官网地址
[openjdk不同版本](http://openjdk.java.net/)
## 源码地址
[华章图书网站](http://www.hzbook.com/)

## 官网贵方
* java虚拟机规范
* java语言规范

## 书籍
* 《垃圾回收算法手册：自动内存管理的艺术》专业性极强
* 《Virtual Machines：Versatile Platforms for Systems and Processes》虚拟化技术的百科全书
* 《Java性能优化权威指南》从操作系统到基于Java的上层程序性能度量和调优进行全面介绍。其中涉及Java虚拟机的内容具备一定深度和很好的可实践性

## 网站资源
* [高级语言虚拟机圈子](http://hllvm.group.iteye.com/)


# 待梳理部分
##  Running Make
When running make without any arguments, the default target is used, which is the same as running make default or make jdk

The output of the exploded image resides in $BUILD/jdk. You can test the newly built JDK like this: $BUILD/jdk/bin/java -version.
# Problems with the Build Environment
By default, the JDK has a strict approach where warnings from the compiler is considered errors which fail the build. For very new or very old compiler versions, this can trigger new classes of warnings, which thus fails the build. Run configure with --disable-warnings-as-errors to turn of this behavior. (The warnings will still show, but not make the build fail.)
## 构建失败建议步骤
Here are a suggested list of things to try if you are having unexpected build problems. Each step requires more time than the one before, so try them in order. Most issues will be solved at step 1 or 2.

Make sure your repository is up-to-date

Run hg pull -u to make sure you have the latest changes.

Clean build results

The simplest way to fix incremental rebuild issues is to run make clean. This will remove all build results, but not the configuration or any build system support artifacts. In most cases, this will solve build errors resulting from incremental build mismatches.

Completely clean the build directory.

If this does not work, the next step is to run make dist-clean, or removing the build output directory ($BUILD). This will clean all generated output, including your configuration. You will need to re-run configure after this step. A good idea is to run make print-configuration before running make dist-clean, as this will print your current configure command line. Here's a way to do this:

make print-configuration > current-configuration
make dist-clean
bash configure $(cat current-configuration)
make
Re-clone the Mercurial repository

Sometimes the Mercurial repository gets in a state that causes the product to be un-buildable. In such a case, the simplest solution is often the "sledgehammer approach": delete the entire repository, and re-clone it. If you have local changes, save them first to a different location using hg export.

