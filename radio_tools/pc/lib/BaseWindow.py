#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QTimer

from lib.Configer import Configer
from lib.lib import GetLocalIpList

class BaseWindow(QMainWindow):
    def __init__(self, ui, iniSection, parent=None):
        QMainWindow.__init__(self, parent)

        # ui界面
        self.mUi = ui
        self.mUi.setupUi(self)

        # 配置
        self.mConfiger = Configer(iniSection)

        # 通用UI 全部除能
        self.mComboBox = self.mUi.comboBox
        self.mPushButtonTalk = self.mUi.pushButtonTalk
        self.mPlainTextEdit = self.mUi.plainTextEdit
        self.mLineEdit = self.mUi.lineEdit
        self.mPushButtonSend = self.mUi.pushButtonSend
        self.mComboBox.setEnabled(False)
        self.mPushButtonTalk.setEnabled(False)
        self.mPlainTextEdit.setEnabled(False)
        self.mLineEdit.setEnabled(False)
        self.mPushButtonSend.setEnabled(False)

        # 接收线程
        self.mComPort = None

        # 对话 非对话 模式切换
        self.mTalking = False   # 标记主模块是否处于对话中
        self.mPushButtonTalk.clicked.connect(self.ModeChange)
        # 定时器 更新 mPlainTextEdit
        self.mPlainTextEditTimer = QTimer()
        self.mPlainTextEditTimer.timeout.connect(self.UpdatePlainTextEdit)

        # 主模块 发送消息
        self.mPushButtonSend.clicked.connect(self.Send)

        #print('BaseWindow init:', end='')
        #print(parent)

    def UpdatePlainTextEdit(self):
        log = self.mComPort.GetLog()
        # 无日志 不记录
        if 0 == len(log):
            return

        self.mPlainTextEdit.appendPlainText(log)
        self.mComPort.ClearLog()

    def UpdateComboBoxList(self, strs):
        self.mComboBox.clear()
        for s in strs:
            self.mComboBox.addItem(s)
        self.mComboBox.setEnabled(True)
        self.mPushButtonTalk.setEnabled(True)

    def ModeChange(self):
        # 切换状态
        self.mTalking = not self.mTalking

        if self.mTalking: # 对话状态
            self.WidgetToTalking()
            self.StartTalking()
        else:
            self.WidgetToUnTalking()
            self.StopTalking()

    def StartTalking(self, comPort, CommunicationClass):
        #print('BaseWindow StartTalking')
        #print(CommunicationClass)

        bufSize = int(self.mConfiger.GetValue('缓存大小'))
        timeOut = int(self.mConfiger.GetValue('接收超时值'))
        # print(comPort)
        # print(bufSize)
        # print(timeOut)

        self.mComPort = CommunicationClass(comPort, bufSize, timeOut)
        self.mComPort.StartRecv()

        flushPeriod = int(self.mConfiger.GetValue('刷新频率'))
        self.mPlainTextEditTimer.start(flushPeriod) # 使用配置项

    def GetComboBoxCurrentText(self):
        return self.mComboBox.currentText()

    def SetComboBoxCurrentText(self, text):
        self.mComboBox.addItem(text)

    def StopTalking(self):
        if self.mComPort:
            self.mComPort.stop()
            self.mComPort.join()
        self.mPlainTextEditTimer.stop()

        # 为下一次打开准备
        del self.mComPort
        self.mComPort = None

        #print('BaseWindow StopTalking')

    def WidgetToTalking(self):
        self.mComboBox.setEnabled(False)
        self.mPlainTextEdit.setEnabled(True)
        self.mLineEdit.setEnabled(True)
        self.mPushButtonSend.setEnabled(True)
        self.mPushButtonTalk.setText('停止对话')
        #self.mPushButtonTalk.setEnabled(True)
        #print('BaseWindow WidgetToTalking')

    def WidgetToUnTalking(self):
        self.mComboBox.setEnabled(True)
        self.mPlainTextEdit.setEnabled(False)
        self.mLineEdit.setEnabled(False)
        self.mPushButtonSend.setEnabled(False)
        self.mPushButtonTalk.setText('开始对话')
        #self.mPushButtonTalk.setEnabled(True)
        #print('BaseWindow WidgetToUnTalking')

    def Send(self, addr):
        #print('BaseWindow Send')
        # 获取 待发送的字节流
        data = self.mLineEdit.text()
        if 0 == len(data): # 避免零长发送回车
            return

        # 发送数据
        self.mComPort.Send(addr, data)

        # 清空 lineEdit
        self.mLineEdit.clear()

    # 退出 清理线程
    def closeEvent(self, event):
        self.StopTalking()

        # TODO: 实现将plainTextEdit内容记录到文件

    def GetAndCheckLocalIP(self, netIPInIni, deviceIPInIni):
        # 获取本机IP列表
        localAddrList = GetLocalIpList()

        # 获取INI中IP
        localAddrFromIni = self.mConfiger.GetValue(netIPInIni)
        localAddrFromIni += '.'
        localAddrFromIni += self.mConfiger.GetValue(deviceIPInIni)

        # IP检查
        rightIPFlag = False
        for ip in localAddrList:
            if localAddrFromIni == ip:
                rightIPFlag = True
                break

        if not rightIPFlag:
            msgBox = QMessageBox();
            msg = '本机ip列表:' + str(localAddrList) + '\n'
            msg += '主设备ip:' + str(localAddrFromIni)
            msgBox.setText(msg)
            msgBox.exec();
            return None
        else:
            return localAddrFromIni

