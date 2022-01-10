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

可选参数列表详见
bash configure --help

```shell
bash configure --enable-debug --with-jvm-variants=server
```

--disable-warnings-as-errors：默认warning会导致build失败。禁止将警告当成build错误，这样子警告会输出出来，但不会影响build过程失败

本机执行情况
```shell
bash configure --with-jvm-variants=server --disable-warnings-as-errors
```


### make

在当前目录下执行make命令，即可编译生成java
默认与执行make jdk一致，也可以执行make 其他参数，详细可见build.html文档


build/macosx-x86_64-server-release/jdk $BUILD下这个目录即是生成的java home目录
全路径形式如下
~/my/project/source/java/openjdk12/jdk12-06222165c35f/build/macosx-x86_64-server-release/jdk

使用内置的java命令查询版本信息
```shell
./bin/java -version
openjdk version "12-internal" 2019-03-19
OpenJDK Runtime Environment (build 12-internal+0-adhoc.chujun.jdk12-06222165c35f)
OpenJDK 64-Bit Server VM (build 12-internal+0-adhoc.chujun.jdk12-06222165c35f, mixed mode)
```

#### make常用命令
* make print-configuration 命令打印当前configure的options输出在当前命令行中
* make clean：清理build出来的东西，不清理configure
* make dist-clean:清理build出来的东西+configure目录


# 构建失败官方建议步骤
来自官方文档
Here are a suggested list of things to try if you are having unexpected build problems. Each step requires more time than the one before, so try them in order. Most issues will be solved at step 1 or 2.

### Make sure your repository is up-to-date

Run hg pull -u to make sure you have the latest changes.

### Clean build results

The simplest way to fix incremental rebuild issues is to run make clean. This will remove all build results, but not the configuration or any build system support artifacts. In most cases, this will solve build errors resulting from incremental build mismatches.

### Completely clean the build directory.

If this does not work, the next step is to run make dist-clean, or removing the build output directory ($BUILD). This will clean all generated output, including your configuration. You will need to re-run configure after this step. A good idea is to run make print-configuration before running make dist-clean, as this will print your current configure command line. Here's a way to do this:

make print-configuration > current-configuration
make dist-clean
bash configure $(cat current-configuration)
make
### Re-clone the Mercurial repository

Sometimes the Mercurial repository gets in a state that causes the product to be un-buildable. In such a case, the simplest solution is often the "sledgehammer approach": delete the entire repository, and re-clone it. If you have local changes, save them first to a different location using hg export.


# 资料
## 官网地址
[openjdk不同版本](http://openjdk.java.net/)
## build.html
参见下载好的build/build.html文档

