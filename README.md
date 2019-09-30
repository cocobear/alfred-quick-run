# alfred-quick-run
## 介绍

Alfred-quick-run是一个alfred的workflow，可以使用关键词和描述来快速搜索执行命令，有点像[pet](https://github.com/knqyf263/pet), 但是它只能在本地的终端下运行，如果你连接远程的服务器就没办法使用了。

想法来源于[command-search-alfred](https://github.com/work-helper/command-search-alfred)，这是一个Go语言写的命令搜索workflow，配置文件也和它一样，感谢作者的分享。

配置文件格式为`yaml`
```yaml
---
- key: file
  remark: 文件批量操作
  values:
      - cmd: find ./ -type f -exec dos2unix {} \;
        remark: 转换当前目录下所有文件换行为unix格式
- key: yum
  remark: yum包管理
  values:
      - cmd: yum install --downloadonly --downloaddir=/root/python python36u python36u-pip
        remark: yum下载指定的包到指定目录不安装
```

你可以搜索命令的关键词，比如 ：

`yum install`

或者也可以搜索命令的描述，比如：

`yum下载`

然后回车，命令就自动粘贴在了终端：

![](https://github.com/cocobear/alfred-quick-run/blob/master/alfred-quick-run-demo.gif)


## 配置

配置文件默认是安装目录下面，你可以通过alfred-quick-run的环境变量来设置它的路径

![](https://github.com/cocobear/alfred-quick-run/blob/master/config.gif)

## 依赖

文本搜索使用的是`rg`，所以需要先安装，建议使用`brew install rg`来安装