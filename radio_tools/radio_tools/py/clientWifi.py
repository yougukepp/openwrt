#!/usr/bin/env python

from socket import *

recvHost = '192.168.3.3'
recvPort = 8001
recvAddr = (recvHost, recvPort)

sendData = b'0123456789abcdef'

udpSendSocket = socket(AF_INET, SOCK_DGRAM)

udpSendSocket.sendto(sendData, recvAddr)

udpSendSocket.close()

