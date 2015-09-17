#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUiType

gConfigerWindowUIClass = loadUiType('ui/configerwindow.ui')[0] # 0 为类 1为对应的控件类型

class ConfigerWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        # ui界面
        self.mUi = gConfigerWindowUIClass()
        self.mUi.setupUi(self)

        # 设置图标
        self.setWindowTitle('Icon')
        self.setWindowIcon(QIcon(r'./res/config.ico'))

        # 整个窗体除能
        self.mCentralWidget = self.centralWidget()
        self.mCentralWidget.setEnabled(False)

        #print('ConfigerWindowinit:', end='')
        #print(parent)

