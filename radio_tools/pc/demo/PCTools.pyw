#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon  
from PyQt5.uic import loadUiType

from lib.MasterWindow import MasterWindow
from lib.FollowerWindow import FollowerWindow
from lib.ConfigerWindow import ConfigerWindow

# UI读取
gUIClass = loadUiType('ui/login.ui') 

class PCLoginWindow(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        # GUI初始化
        self.mUi = gUIClass[0]()
        self.mUi.setupUi(self)

        # 图标
        self.setWindowTitle('Icon')  
        self.setWindowIcon(QIcon(r'./res/wifi.png'))

        self.mRadioButtonMaster = self.mUi.radioButtonMaster
        self.mRadioButtonFollower = self.mUi.radioButtonFollower
        self.mRadioButtonConfiger = self.mUi.radioButtonConfiger
        self.mPushButton = self.mUi.pushButton

        # 默认选择主设备
        self.mRadioButtonMaster.setChecked(True)

        self.mPushButton.clicked.connect(self.EnterMainWindow) 

        self.mMainWin = None

        
    def EnterMainWindow(self):
        if self.mRadioButtonMaster.isChecked(): 
            #print('mRadioButtonMaster')
            self.mMainWin = MasterWindow()

        if self.mRadioButtonFollower.isChecked():
            #print('mRadioButtonFollower')
            self.mMainWin = FollowerWindow()

        if self.mRadioButtonConfiger.isChecked():
            #print('mRadioButtonConfiger')
            self.mMainWin = ConfigerWindow()

        self.mMainWin.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    win = PCLoginWindow()
    win.show()

    sys.exit(app.exec_())

