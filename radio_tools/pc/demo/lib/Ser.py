#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial

from lib.BaseCommunication import BaseCommunication

class Ser(BaseCommunication):
    def __init__(self, comPort, bufSize, timeout):
        BaseCommunication.__init__(self)

        ser = serial.Serial(comPort[0]) # 串口名字
        ser.baudrate = comPort[1]       # 波特率
        ser.timeout = timeout / 1000

        self.mSer = ser
        self.mBufSize = bufSize

    def __del__(self):
        #print('Ser __del__')
        self.mSer.close()

    def StartRecv(self):
        self.start()
        print('开始监听 %s:%s...' % (self.mSer.port, str(self.mSer.baudrate)))

    def Recv(self):
        ser = self.mSer
        bufSize = self.mBufSize
        baudrateStr = str(ser.baudrate)

        # 接收
        recvData = ser.read(self.mBufSize)

        if 0 == len(recvData):
            return

        # 串口启动后会受到 两个连续的 0x0
        """
        for c in recvData:
            print('%s:0x%x' % (str(type(c)), c), end=',')
        print()
        """

        # 编码
        recvStr = recvData.decode(encoding="utf-8")
        self.AddLog((ser.port, baudrateStr), recvStr)

        print('recv %s from %s:%s' % (recvStr, ser.port, baudrateStr))

    def Send(self, addr, data):
        data += '\n' # 串口帧位标记

        # 编码
        byteData = data.encode(encoding="utf-8")

        # 发送数据
        ser = self.mSer
        ser.write(byteData)

        # 构造日志 及打印
        portName = ser.port
        baudrateStr = str(ser.baudrate)
        addr = (portName, baudrateStr)
        self.AddLog(addr, data)
        print('send %s to %s:%s' % (data, addr[0], str(addr[1])))

