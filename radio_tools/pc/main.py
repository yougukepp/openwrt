#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial
import serial.tools.list_ports

from PCPinger import PCPinger
from PCConfiger import PCConfiger

if __name__=='__main__':
    configer = PCConfiger()

    print('test Serial...')
    print('all serial:')
    allSerial = serial.tools.list_ports.comports()
    for s in allSerial:
        print(s[0])
    print()

    #exit()

    print('test Ping...')

    pinger = PCPinger()
    netIP = configer.GetValue('master', 'netip')
    dhcpIPMin = configer.GetValue('master', 'dhcpipmin')
    dhcpIPMax = configer.GetValue('master', 'dhcpipmax')

    for ipLast in range(int(dhcpIPMin), int(dhcpIPMax) + 1):
        ip = netIP + '.' + str(ipLast)
        #print(ip)
        pinger.AddIp(ip)
    reachableIPs = pinger.Ping(1) # 1s超时

    for ip in reachableIPs:
        print(ip)

