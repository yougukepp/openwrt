#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMainWindow

from lib.Configer import Configer

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

        # 对话 非对话 模式切换
        self.mTalking = False   # 标记主模块是否处于对话中
        self.mPushButtonTalk.clicked.connect(self.ModeChange)
        # 主模块 发送消息
        self.mPushButtonSend.clicked.connect(self.Send)

        #print('BaseWindow init:', end='')
        #print(parent)

    def ModeChange(self):
        pass

    def Send(self):
        pass


