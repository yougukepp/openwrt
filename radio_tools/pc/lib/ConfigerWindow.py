#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUiType

gConfigerWindowUIClass = loadUiType('ui/configerwindow.ui')[0] # 0 为类 1为对应的控件类型

class ConfigerWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        # ui界面
        self.mUi = gConfigerWindowUIClass()
        self.mUi.setupUi(self)

        #print('ConfigerWindowinit:', end='')
        #print(parent)

