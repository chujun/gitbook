# 常见问题
## brew update访问大概率超时
原因：github brew 和brew-core经常访问超时，导致更新失败
解决方案：设置镜像到一个国内可用镜像，例如清华镜像


## 常用命令列表

### 问题诊断用
brew doctor
brew config
brew info



## brew update 更新过程中出现问题，无法更新和使用brew
例如brew doctor出现如下情况
```shell
Warning: Some installed formulae are not readable:
  git-lfs: undefined method `cellar' for #<BottleSpecification:0x00007f97730d79f8>

  pkg-config: undefined method `cellar' for #<BottleSpecification:0x00007f977316e790>

  tree: undefined method `cellar' for #<BottleSpecification:0x00007f9773a74bc8>

  libtiff: undefined method `cellar' for #<BottleSpecification:0x00007f97730bd148>

  libtool: undefined method `cellar' for #<BottleSpecification:0x00007f9773ae5b70>

  gmp: undefined method `cellar' for #<BottleSpecification:0x00007f97731fa8a8>
```
大概率是brew-core出现问题，
### 解决方案
删除并重新更新brew-core

不使用镜像版本
```shell
rm -rf "$(brew --repo homebrew/core)"
brew tap homebrew/core
```
使用自定义镜像版本
```shell
export HOMEBREW_CORE_GIT_REMOTE="https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/homebrew-core.git"
rm -rf "$(brew --repo homebrew/core)"
brew tap --custom-remote --force-auto-update homebrew/core https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/homebrew-core.git
```

## 不重要系列
Formulae 和 casks区别
brew install 和 brew cask install 的区别

brew install:下载源码，编译(./configure && make install),处理依赖，设置好环境变量
brew cask install ：下载已经编译好的应用包，直接安装即可


brew install：适用于安装系统工具，命令行工具和第三方工具等
brew cask install：适用于安装带有界面的软件包


# 资料
[https://mirrors.tuna.tsinghua.edu.cn/help/homebrew/](https://mirrors.tuna.tsinghua.edu.cn/help/homebrew/)
## 踩过的坑
[Can't install anything with brew; I get: "undefined method 'cellar'"](https://github.com/Homebrew/discussions/discussions/2599)