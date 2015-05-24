#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon

from lib.BaseWindow import BaseWindow
from lib.Net import Net
from lib.lib import ComOrNet
from lib.lib import GetReachableIPs

gMasterWindowUIClass = loadUiType('ui/masterwindow.ui')[0] # 0 为类 1为对应的控件类型

class MasterWindow(BaseWindow):
    def __init__(self, parent=None):
        BaseWindow.__init__(self, gMasterWindowUIClass(), '主设备', parent)

        # 设置图标
        self.setWindowTitle('Icon')
        self.setWindowIcon(QIcon(r'./res/wifim.png'))

        # 主模块 扫描从模块
        self.mPushButtonSearch = self.mUi.pushButtonSearch
        self.mPushButtonSearch.clicked.connect(self.Search)

    def Search(self):
        #print('search')

        netIP = self.mConfiger.GetValue('网络IP')
        minIP = self.mConfiger.GetValue('DHCP开始')
        maxIP = self.mConfiger.GetValue('DHCP结束')
        timeout = self.mConfiger.GetValue('PING延时')
        #print(netIP)
        #print(minIP)
        #print(maxIP)
        #print(timeout)
        ips = GetReachableIPs(netIP, minIP, maxIP, timeout)
        #print(ips)

        if 0 == len(ips):
            msgBox = QMessageBox();
            msgBox.setText("没有找到从设备.");
            msgBox.exec();
        else:
            self.UpdateComboBoxList(ips)

    def WidgetToTalking(self):
        BaseWindow.WidgetToTalking(self)
        self.mPushButtonSearch.setEnabled(False)
        #print('MasterWindow WidgetToTalking')

    def WidgetToUnTalking(self):
        BaseWindow.WidgetToUnTalking(self)
        self.mPushButtonSearch.setEnabled(True)
        #print('MasterWindow WidgetToUnTalking')

    def StartTalking(self):
        #print('MasterWindow StartTalking')

        # 构造接收套接字
        ipAddr = self.GetAndCheckLocalIP('网络IP', '主设备IP')
        port = int(self.mConfiger.GetValue('主设备Port'))
        addr = (ipAddr, port)
        #print(addr)

        BaseWindow.StartTalking(self, addr, Net)

    def StopTalking(self):
        #print('MasterWindow StopTalking')
        BaseWindow.StopTalking(self)

    def Send(self):
        #print('MasterWindow Send')
        ipAddr = self.GetComboBoxCurrentText()
        port = int(self.mConfiger.GetValue('从模块Port'))
        addr = (ipAddr, port)

        BaseWindow.Send(self, addr)

