#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.uic import loadUiType

from lib.BaseWindow import BaseWindow

gFollowerWindowUIClass = loadUiType('ui/followerwindow.ui')[0] # 0 为类 1为对应的控件类型

class FollowerWindow(BaseWindow):
    def __init__(self, parent=None):
        BaseWindow.__init__(self, gFollowerWindowUIClass(), 'follower', parent)

        #print('FollowerWindow init:', end='')
        #print(parent)
