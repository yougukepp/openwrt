#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lib.RecvThread import RecvThread

class SerRecvThread(RecvThread):
    def __init__(self, comPort, bufSize, timeout):
        RecvThread.__init__(self, comPort, bufSize, timeout)

        self.mComPort = comPort
        self.mBufSize = bufSize
        self.mTimeout = timeout

    def Recv(self):
        sock = self.mComPort
        bufSize = self.mBufSize
        timeout = self.mTimeout
        print('SerRecvThread Recv')

