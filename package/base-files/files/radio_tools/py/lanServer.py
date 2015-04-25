#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from socket import *

host = '192.168.10.3'
port = 8001
bufSize = 1024

addr = (host, port)

udpSerSock = socket(AF_INET, SOCK_DGRAM)
udpSerSock.bind(addr)

os.system('sudo ifconfig eth0 192.168.10.3')

print('wating for message...', end = '')
print(addr)

while True:
    (recvData, clientAddr) = udpSerSock.recvfrom(bufSize)
    print(recvData)
    print(clientAddr)

udpSerSock.close()

