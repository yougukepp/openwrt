#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import struct
import array
import time
import socket
import threading

class Pinger:
    def __init__(self):
        self.mIpList = []
        self.mIndex = 0

    def AddIp(self, ip):
        ipList = self.mIpList
        ipList.append(ip)

    def __iter__(self):
        return self

    def __next__(self):
        ipList = self.mIpList
        index = self.mIndex

        size = len(self.mIpList)

        if not ipList or size == index:
            raise StopIteration
        else:
            rst = ipList[index]
            self.mIndex += 1
            return rst

    def Ping(self, timeout):
        socketIcmp = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))
        timeout = 1.0 * timeout / 1000
        socketIcmp.settimeout(timeout)
        #print('ping timeout: %d s', timeout)

        icmpRecvThread = IcmpRecvThread(socketIcmp)
        icmpRecvThread.start()

        icmpSender = IcmpSender(socketIcmp)
        data = b''                              # 用于ICMP报文的负荷字节（8bit）
        icmpSender.Send(self, data)
        reachableIPs = icmpRecvThread.Wait()    # 等待结束

        # 仅仅加入存在于mIpList中的ip
        ipList = []
        for ip in self.mIpList:
            if ip in reachableIPs:
                ipList.append(ip)

        #print(self.mIpList)
        #print(reachableIPs)
        #print(ipList)
        return tuple(ipList)

class IcmpSender:
    def __init__(self, sock):
        self.mSock = sock

    def CheckSum(self, packet):
        '''ICMP 报文效验和计算方法'''
        if len(packet) & 1:
            packet = packet + '\0'
        words = array.array('h', packet)
        sum = 0
        for word in words:
            sum += (word & 0xffff)
        sum = (sum >> 16) + (sum & 0xffff)
        sum = sum + (sum >> 16)

        return (~sum) & 0xffff

    def MakeIcmpPacket(self, data):
        '''构造 ICMP 报文'''
        idField = os.getpid()                   # 构造ICMP报文的ID字段，无实际意义

        header = struct.pack('bbHHh', 8, 0, 0, idField, 0) # TYPE、CODE、CHKSUM、ID、SEQ

        packet = header + data                  # packet without checksum
        checksum = self.CheckSum(packet)        # make checksum
        header = struct.pack('bbHHh', 8, 0, checksum, idField, 0)

        packet = header + data

        return packet

    def Send(self, ipPool, data):
        sock = self.mSock
        packet = self.MakeIcmpPacket(data)
        for ip in ipPool:  # ip 作为迭代元素
            sock.sendto(packet, (ip, 0))

class IcmpRecvThread(threading.Thread):
    '''
    接收ICMP回显报文的线程。

    参数：
        timeout -- 接收超时
        bufSize -- 接收缓冲
    '''
    def __init__(self, sock, bufSize = 1024):
        threading.Thread.__init__(self)

        self.mSock = sock
        self.mBufSize = bufSize
        self.mRunning = True
        self.mIpPool = {}

    def run(self):
        #print('Icmp Recv Thread Start...')
        while True:
            try:
                sock = self.mSock
                (recvData, addr)= sock.recvfrom(self.mBufSize)
                ip = addr[0]
                self.mIpPool[ip] = None
                #print(ip)
            except socket.timeout as err: # 超时退出
                break
        #print('Icmp Recv Thread End.')
        self.mRunning = False

    def Wait(self):
        while self.mRunning:
            time.sleep(0.1) # 休眠 100 ms
        return self.mIpPool

if __name__=='__main__':
    pass
