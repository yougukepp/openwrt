#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import ctypes
import threading

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QTimer
from PyQt5.uic import loadUiType,loadUi

import PCPing

# UI读取
gUIClass = loadUiType('PCTools.ui')

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.mMasterAddr = None             # master 自身地址 ip
        self.mFllowerAddr = None            # fllower 自身地址 ip or serial
        self.mAddrListByMaster = None       # 主模块中查到的从模块IP
        self.mAddrListByFllower = None      # 从模块中查到的可能通信口 ip or serial

        # GUI初始化
        self.mUi = gUIClass[0]()
        self.mUi.setupUi(self)

        # 控件
        # 核心tabWidget控件
        self.mTabWidget = self.mUi.tabWidget 

        # 主模块地址下拉框
        self.mMasterAddrComboBox = self.mUi.comboBoxMaster
        # 从模块地址下拉框
        #self.mMasterAddrComboBox = self.mUi.comboBoxMaster

        # 自动刷新定时器
        self.mFlushTimer = QTimer()
        self.mFlushTimer.timeout.connect(self.Flush)
        self.mFlushTimer.start(1000)

    def paintEvent(self, event):
        QMainWindow.paintEvent(self, event)

    def Flush(self): 
        self.mAddrListByMaster = self.GetAddrListByMaster()
        self.mAddrListByFllower = self.GetAddrListByFllower()
        print(self.mAddrListByMaster)

    # 以下工具函数移动入独立的文件
    def GetAddrListByFllower(self):
        pass

    def GetAddrListByMaster(self):
        """
        通过连接的ip查询模块
        """ 
        ipPool = PCPing.IpPool()
        ipHead = '10.33.152.'
        for ipLast in range(1, 10):
            ip = ipHead + str(ipLast)
            ipPool.AddIp(ip)
            
        reachableIPs = ipPool.Ping(1) # 1s超时
        return reachableIPs

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    win = MainWindow()
    win.show()

    sys.exit(app.exec_())

