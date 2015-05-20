#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial
import serial.tools.list_ports

import PCPing

if __name__=='__main__':
    print('test Serial...')
    print('all serial:')
    allSerial = serial.tools.list_ports.comports()
    for s in allSerial:
        print(s[0])
    print()

    exit()

    print('test Ping...')

    ipPool = PCPing.IpPool()
    ipHead = '10.33.152.'
    for ipLast in range(1, 10):
        ip = ipHead + str(ipLast)
        ipPool.AddIp(ip)
    reachableIPs = ipPool.Ping(1) # 1s超时

    for ip in reachableIPs:
        print(ip, end = ' ')

    print()
