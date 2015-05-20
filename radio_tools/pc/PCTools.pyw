#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import ctypes
import socket
import threading

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QTimer
from PyQt5.uic import loadUiType,loadUi

from PCPinger import PCPinger
from PCConfiger import PCConfiger

# UI读取
gUIClass = loadUiType('PCTools.ui') 

# 主模块 对话日志
gMasterTalkLog = ''
gMasterTalkLogLock = threading.Lock()

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.mConfiger = PCConfiger()

        # GUI初始化
        self.mUi = gUIClass[0]()
        self.mUi.setupUi(self)

        # 控件
        # 核心tabWidget控件
        self.mTabWidget = self.mUi.tabWidget 

        # 配置页面除能
        self.mTabConfig = self.mUi.tabConfig
        self.mTabConfig.setEnabled(False)

        # 主模块 除pushButtonMasterScan外 全部除能
        self.mPushButtonMasterScan = self.mUi.pushButtonMasterScan

        self.mComboBoxMaster = self.mUi.comboBoxMaster
        self.mComboBoxMaster.setEnabled(False)
        self.mPushButtonMasterTalk = self.mUi.pushButtonMasterTalk
        self.mPushButtonMasterTalk.setEnabled(False)
        self.mPlainTextEditMaster = self.mUi.plainTextEditMaster
        self.mPlainTextEditMaster.setReadOnly(True)
        self.mPlainTextEditMaster.setCenterOnScroll(True)
        self.mLineEditMaster = self.mUi.lineEditMaster
        self.mLineEditMaster.setEnabled(False)
        self.mPushButtonMasterSend =self.mUi.pushButtonMasterSend
        self.mPushButtonMasterSend.setEnabled(False)

        # 主模块 扫描从模块 
        self.mPushButtonMasterScan.clicked.connect(self.MasterScan)
        # 主模块 对话 非对话 模式切换
        self.mMasterTalking = False   # 标记主模块是否处于对话中
        self.mPushButtonMasterTalk.clicked.connect(self.MasterTalk)
        # 主模块 发送消息
        self.mPushButtonMasterSend.clicked.connect(self.MasterSend)
        # 主模块 接收消息使用独立线程
        self.mMasterRecvThread = None

        # 主模块定时器 更新 mPlainTextEditMaster
        self.mPlainTextEditMasterTimer = QTimer()
        self.mPlainTextEditMasterTimer.timeout.connect(self.UpdatePlainTextEditMaster)

    # 重绘
    def paintEvent(self, event): 
        QMainWindow.paintEvent(self, event)

    # 退出
    def closeEvent(self, event):
        # 接收退出
        self.mMasterRecvThread.stop()
        self.mMasterRecvThread.join()

    # 以下工具函数移动入独立的文件
    def MasterScan(self): 
        ips = self.GetAddrListByMaster()
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

    def UpdatePlainTextEditMaster(self):
        """
        研究算法 加速更新速度
        """
        if not self.mMasterTalking: # 回话状态才更新
            return

        #print('UpdatePlainTextEditMaster')
        self.mPlainTextEditMaster.clear()

        gMasterTalkLogLock.acquire() # 操作日志 需要锁
        self.mPlainTextEditMaster.setPlainText(gMasterTalkLog)
        gMasterTalkLogLock.release() # 操作日志 需要锁


    def MasterTalk(self):
        # 切换状态
        self.mMasterTalking = not self.mMasterTalking

        # 依据新状态 更新控件状态
        if self.mMasterTalking: # 对话状态
            # 创建 & 启动接收线程 
            ips = self.GetLocalIpList()                          # 主设备 本机ip
            if 1 != len(ips):                                     # 有且仅有一个ip
                print(ips)
                msgBox = QMessageBox();
                msgBox.setText("本机ip设置有误.");
                msgBox.exec();
                return
            ip = ips[0]
            port = int(self.mConfiger.GetValue('master', 'port')) # 主设备 监听端口
            bufSize = int(self.mConfiger.GetValue('master', 'bufsize')) # 主设备 监听buf大小
            addr = (ip, port) 
            self.mMasterRecvThread = RecvThread(addr, bufSize)

            # 设置控件
            self.mPushButtonMasterScan.setEnabled(False) 
            self.mComboBoxMaster.setEnabled(False)
            self.mPushButtonMasterTalk.setText('停止对话')
            self.mPushButtonMasterTalk.setEnabled(True)
            self.mLineEditMaster.setEnabled(True)
            self.mPushButtonMasterSend.setEnabled(True)
            #print('对话状态')


            self.mMasterRecvThread.start() 
            self.mPlainTextEditMasterTimer.start(1000) # 使用配置项
        else: 
            #print('非对话状态')
            # 关闭接收线程
            self.mMasterRecvThread.stop()
            self.mMasterRecvThread.join()
            self.mPlainTextEditMasterTimer.stop()

            # 设置控件
            self.mLineEditMaster.setEnabled(False)
            self.mPushButtonMasterSend.setEnabled(False)
            self.mPushButtonMasterTalk.setEnabled(False)
            self.mPushButtonMasterTalk.setText('开始对话')
            self.mLineEditMaster.clear()
            self.mComboBoxMaster.clear()
            self.mComboBoxMaster.setEnabled(True)
            self.mPushButtonMasterScan.setEnabled(True) 


    def MasterSend(self):
        ip = self.mComboBoxMaster.currentText()
        port = int(self.mConfiger.GetValue('fllower', 'port')) # 主模块发往从模块的监听端口
        data = self.mLineEditMaster.text()

        byteData = data.encode(encoding="utf-8")
        # print(data)
        # print(byteData)
        self.UdpSend(ip, port, byteData)

        # 加入到日志
        log = GetLogTitle(ip, port) + '\n'
        log += data + '\n\n'
        print(log)
        gMasterTalkLogLock.acquire() # 操作日志 需要锁
        global gMasterTalkLog
        gMasterTalkLog += log
        gMasterTalkLogLock.release() # 操作日志 需要锁

        self.mLineEditMaster.clear()

    def GetAddrListByFllower(self):
        pass

    def GetAddrListByMaster(self):
        """
        通过连接的ip查询模块
        """ 
        pinger = PCPinger()
        netIP = self.mConfiger.GetValue('master', 'netip')
        dhcpIPMin = self.mConfiger.GetValue('master', 'dhcpipmin')
        dhcpIPMax = self.mConfiger.GetValue('master', 'dhcpipmax') 
        
        for ipLast in range(int(dhcpIPMin), int(dhcpIPMax) + 1):
            ip = netIP + '.' + str(ipLast)
            #print(ip)
            pinger.AddIp(ip)
        reachableIPs = pinger.Ping(1) # 1s超时

        return reachableIPs

    def GetLocalIpList(self): 
        ipInfo = socket.gethostbyname_ex(socket.gethostname())
        ipList = ipInfo[2]
        return ipList

    def UdpSend(self, ip, port, data): 
        addr = (ip, port)
        udpSendSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #print(addr)
        #print(data)
        udpSendSocket.sendto(data, addr)
        print('send %s' % data, end = '')
        print('to ', end = '')
        print(addr)
        udpSendSocket.close()

class RecvThread(threading.Thread):  
    def __init__(self, addr, bufSize):
        threading.Thread.__init__(self)
        self.mAddr = addr
        self.mBufSize = bufSize
        self.mRunning = True

    def run(self):  
        udpRecvSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udpRecvSocket.settimeout(1) # 不阻塞 避免无法join线程
        udpRecvSocket.bind(self.mAddr)
        print('开始监听 ', end = '')
        print(self.mAddr, end = '')
        print('... ')

        while self.mRunning: 
            try:
                (recvData, clientAddr) = udpRecvSocket.recvfrom(self.mBufSize)

                recvStr = recvData.decode(encoding="utf-8")
                ip = clientAddr[0]
                port = clientAddr[1]
                log = GetLogTitle(ip, port)  + '\n'
                log += recvStr + '\n\n'
                
                gMasterTalkLogLock.acquire() # 操作日志 需要锁
                global gMasterTalkLog
                gMasterTalkLog += log
                gMasterTalkLogLock.release() # 操作日志 需要锁 
                
                print('recv %s ' % recvStr, end = '')
                print('from ', end = '')
                print(clientAddr)

                #print('running')
            except socket.timeout as e: # 为了避免阻塞这里使用超时
                continue
            except Exception as e:
                print(e)
                break
            
        udpRecvSocket.close()
        print('结束监听 ', end = '')
        print(self.mAddr, end = '')
        print('... ')

    def stop(self):
        self.mRunning = False

def GetLogTitle(ip, port):
    t = time.localtime()
    nowStr = '%4d-%02d-%02d %02d:%02d:%02d' % (t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec) 
    title = str(ip) + ':' + str(port) + '\t' + nowStr

    return title

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    win = MainWindow()
    win.show()

    sys.exit(app.exec_())

