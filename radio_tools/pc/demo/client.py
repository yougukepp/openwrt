#!/usr/bin/env python3

from socket import *

recvHost = '192.168.2.101'
recvPort = 8001
recvAddr = (recvHost, recvPort)

sendData = b'shoudongfasong'

udpSendSocket = socket(AF_INET, SOCK_DGRAM)

udpSendSocket.sendto(sendData, recvAddr)
print('send %s' % sendData, end = '')
print('to ', end = '')
print(recvAddr)

udpSendSocket.close()

