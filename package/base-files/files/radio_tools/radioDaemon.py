#!/usr/bin/env python
# -*- coding: utf-8 -*-



def HelloToWife():
    print("/etc/radioDaemon.conf 文件内容:")
    print

    # 准备解析配置文件
    f = open("../etc/radioDaemon.conf")

    for l in f:
        print l,

    # 主模式 直接退出
    # 从模式 修改配置文件后退出

if __name__ == '__main__':
    HelloToWife()


