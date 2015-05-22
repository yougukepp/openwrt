#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import time

def ComOrNet(portName):
    '''
    依据 民族判断是串口还是网络
    '''

    return 'Net'

def GetLocalIpList():
    ipInfo = socket.gethostbyname_ex(socket.gethostname())
    #print(ipInfo)
    ipList = ipInfo[2]

    return ipList

def GetNowStr():
    t = time.localtime()
    nowStr = '%4d-%02d-%02d %02d:%02d:%02d' % (t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)

    return nowStr


