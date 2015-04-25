#!/usr/bin/env python3

from socket import *

recvHost = '192.168.10.1'
recvPort = 8001
recvAddr = (recvHost, recvPort)

sendData = b'0123456789abcdef'

udpSendSocket = socket(AF_INET, SOCK_DGRAM)

udpSendSocket.sendto(sendData, recvAddr)

udpSendSocket.close()

