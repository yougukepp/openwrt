#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.uic import loadUiType

from lib.Pinger import Pinger
from lib.BaseWindow import BaseWindow

gMasterWindowUIClass = loadUiType('ui/masterwindow.ui')[0] # 0 为类 1为对应的控件类型

def GetReachableIPs(netIP, minIP, maxIP, timeout=1000):
    pinger = Pinger()
    reachableIPs = None
    
    for ipLast in range(int(minIP), int(maxIP) + 1):
        ip = netIP + '.' + str(ipLast)
        #print(ip)
        pinger.AddIp(ip)
        reachableIPs = pinger.Ping(int(timeout))

    return reachableIPs

class MasterWindow(BaseWindow):
    def __init__(self, parent=None):
        BaseWindow.__init__(self, gMasterWindowUIClass(), 'master', parent)

        # 主模块 扫描从模块 
        self.mPushButtonSearch = self.mUi.pushButtonSearch
        self.mPushButtonSearch.clicked.connect(self.Search)


    def Search(self):
        print('search')

        netIP = self.mConfiger.GetValue('网络IP')
        minIP = self.mConfiger.GetValue('DHCP开始')
        maxIP = self.mConfiger.GetValue('DHCP结束')
        timeout = self.mConfiger.GetValue('PING延时')
        #print(netIP)
        #print(minIP)
        #print(maxIP)
        print(timeout)
        ips = GetReachableIPs(netIP, minIP, maxIP, timeout)

        """
        if 0 == len(ips):
            msgBox = QMessageBox();
            msgBox.setText("没有找到从设备.");
            msgBox.exec();
            self.mComboBoxMaster.setEnabled(False)
            self.mPushButtonMasterTalk.setEnabled(False)
        else: 
            self.mComboBoxMaster.clear()
            for ip in ips:
                self.mComboBoxMaster.addItem(ip)
            self.mComboBoxMaster.setEnabled(True)
            self.mPushButtonMasterTalk.setEnabled(True)
        """

