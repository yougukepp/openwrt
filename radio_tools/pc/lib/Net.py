#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket

from lib.BaseCommunication import BaseCommunication

class Net(BaseCommunication):
    def __init__(self, addr, bufSize, timeout):
        BaseCommunication.__init__(self)

        recvSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        recvSock.bind(addr)
        recvSock.settimeout(timeout/1000) # 不阻塞 避免无法join线程

        self.mAddr = addr
        self.mRecvSock = recvSock
        self.mBufSize = bufSize

    # 接收线程 启动 循环调用Recv
    def StartRecv(self):
        self.start()
        print('开始监听 %s:%s...' % (self.mAddr[0], str(self.mAddr[1])))

    def Recv(self):
        sock = self.mRecvSock
        bufSize = self.mBufSize

        # 为了避免阻塞这里使用超时 来非阻塞
        try :
            # 接收消息
            (recvData, clientAddr) = sock.recvfrom(bufSize)

            # 编码
            recvStr = recvData.decode(encoding="utf-8")

            '''
            # 记录日志
            ip = clientAddr[0]
            port = clientAddr[1]
            log = GetLogTitle(ip, port)  + '\n'
            log += recvStr + '\n\n'
            gMasterTalkLogLock.acquire() # 操作日志 需要锁
            global gMasterTalkLog
            gMasterTalkLog += log
            gMasterTalkLogLock.release() # 操作日志 需要锁
            '''
            self.AddLog(clientAddr, recvStr)
            print('recv %s from %s:%s' % (recvStr, clientAddr[0], str(clientAddr[1])))

        except socket.timeout as e:
            pass
        except Exception as e:
            print(e)
            exit()

    def Send(self, addr, data):
        # 编码
        byteData = data.encode(encoding="utf-8")

        sendSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sendSock.sendto(byteData, addr)

        self.AddLog(addr, data)
        print('send %s to %s:%s' % (data, addr[0], str(addr[1])))

