#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial.tools.list_ports

from PyQt5.uic import loadUiType

from lib.BaseWindow import BaseWindow
from lib.Ser import Ser
from lib.Net import Net

gFollowerWindowUIClass = loadUiType('ui/followerwindow.ui')[0] # 0 为类 1为对应的控件类型

class FollowerWindow(BaseWindow):
    def __init__(self, parent=None):
        BaseWindow.__init__(self, gFollowerWindowUIClass(), '从设备', parent)

        # UI设置
        self.mRadioButtonSerial = self.mUi.radioButtonSerial
        self.mRadioButtonNet = self.mUi.radioButtonNet

        self.mRadioButtonSerial.toggled.connect(self.MethodChange)
        # 两个radio互斥 连接一个即可
        #self.mRadioButtonNet.toggled.connect(self.MethodChange)

        # 默认选择串口
        self.mRadioButtonSerial.setChecked(True)

        #print('FollowerWindow init:', end='')
        #print(paren)

    def SerialUsed(self):
        if self.mRadioButtonSerial.isChecked():
            return True
        else:
            return False

    def MethodChange(self):
        addrs = []

        if self.SerialUsed(): # 串口通信
            allSerial = serial.tools.list_ports.comports()
            for aSerial in allSerial:
                addrs.append(aSerial[0])
        else: # 网口通信
            ipAddr = self.GetLocalIP()
            addrs.append(ipAddr)

        self.UpdateComboBoxList(addrs)

    def WidgetToTalking(self):
        BaseWindow.WidgetToTalking(self)
        self.mRadioButtonSerial.setEnabled(False)
        self.mRadioButtonNet.setEnabled(False)
        #print('FollowerWindow WidgetToTalking')

    def StartTalking(self):
        #print('FollowerWindow StartTalking')
        (addr, communicationClass) = self.GetTalkPara()
        BaseWindow.StartTalking(self, addr, communicationClass)

    def WidgetToUnTalking(self):
        BaseWindow.WidgetToUnTalking(self)
        self.mRadioButtonSerial.setEnabled(True)
        self.mRadioButtonNet.setEnabled(True)
        #print('FollowerWindow WidgetToUnTalking')

    def StopTalking(self):
        #print('FollowerWindow StopTalking')
        BaseWindow.StopTalking(self)

    def Send(self):
        #print('FollowerWindow Send')
        ipAddr = self.mConfiger.GetValue('网络IP')
        ipAddr += '.'
        ipAddr += self.mConfiger.GetValue('从模块IP')
        port = int(self.mConfiger.GetValue('从模块Port'))
        addr = (ipAddr, port)

        BaseWindow.Send(self, addr)

    def GetTalkPara(self):
        addr = None
        communicationClass = None

        if self.SerialUsed(): # 串口通信
            portName = self.GetComboBoxCurrentText()
            baudRate = int(self.mConfiger.GetValue('波特率'))
            addr = (portName, baudRate)
            communicationClass = Ser
        else: # 网口通信
            ipAddr = self.GetLocalIP()
            port = int(self.mConfiger.GetValue('从设备Port'))
            addr = (ipAddr, port)
            communicationClass = Net

        return (addr, communicationClass)

    def GetLocalIP(self):
        ipAddr = self.GetAndCheckLocalIP('网络IP', '从设备IP')
        return ipAddr

