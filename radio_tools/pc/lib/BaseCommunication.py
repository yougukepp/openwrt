#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import threading

from lib.lib import GetNowStr

class BaseCommunication(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.mRunning = True

        # 日志及其锁
        self.mLog = ''
        self.mLogLock = threading.Lock()

    def run(self):
        #print('BaseCommunication run Begin')
        while self.mRunning:
            self.Recv()
            #print('BaseCommunication Running...')
        #print('BaseCommunication run End')

    def stop(self):
        self.mRunning = False

    def AddLog(self, addr, data):
        # 无数据 不记录
        if 0 == len(data):
            return

        name1 = addr[0]
        name2 = addr[1]
        nowStr = GetNowStr()
        log = nowStr + '\t' + str(name1) + ':' + str(name2) + '\n'
        log += data + '\n'

        # 操作日志 需要锁
        self.mLogLock.acquire()
        self.mLog += log
        self.mLogLock.release()

        #print('%s' % log)

    def GetLog(self):
        # 操作日志 需要锁
        self.mLogLock.acquire()
        log = self.mLog
        self.mLogLock.release()

        return log

    def ClearLog(self):
        # 操作日志 需要锁
        self.mLogLock.acquire()
        self.mLog = ''
        self.mLogLock.release()

if __name__ == "__main__":
    recvThread = RecvThread()
    recvThread.start()
    time.sleep(5)
    recvThread.stop()
    recvThread.join()

    exit()

