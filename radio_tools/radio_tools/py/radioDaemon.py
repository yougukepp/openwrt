#!/usr/bin/env python
# -*- coding: utf-8 -*-

# master moduler is router, code is not needed
# this is follower moduler code

import os
import re
import time
import socket
import thread
import serial

g_get_ip_sleep_time = 3
g_sleep_time = 0
g_promtp_time = 5

# all port is 8001
# wifi interface
# master device unchanged 192.168.3.3
# follower moduler changed( becasue of dhcp)
g_wifi_in_ip = '192.168.3.2' # inited ip to 192.168.3.2(revesed ip)
g_wifi_in_port = 8001
g_wifi_out_ip = '192.168.3.3'
g_wifi_out_port = 8001

# wired interface unchanged
# follower moduler unchanged 192.168.10.1
# follower device unchanged  192.168.10.3
g_lan_in_ip = '192.168.10.1'
g_lan_in_port = 8001
g_lan_out_ip = '192.168.10.3'
g_lan_out_port = 8001

# serial interface
g_serial_name = '/dev/ttyS0'
g_baudrate = 9600

# recv bufsize
g_buf_size = 1024
g_serial_buf_size = 1

def GetLocalWifiIP():
    cmd = 'ifconfig ' # remove sudo
    interfaceName = 'wlan0'
    cmdStr = cmd + interfaceName

    while True:
        rstStrList = os.popen(cmdStr).readlines()
        ipLine = rstStrList[1]

        # find ip line
        m = re.search(r'inet addr:(.*)\s+Bcast', ipLine)
        #print ipLine

        ip = ''
        if m:
            ip = m.group(1)
            break
        else:
            # sleep goto next loop
            print "wifi is not ready, wait %s and goto check wifi ip again." % g_get_ip_sleep_time
            time.sleep(g_get_ip_sleep_time)
    print ip

    return ip

def Wifi2LanAndSerial(inSocket, outAddr, outSerial):
    outSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        (recvData, clientAddr) = inSocket.recvfrom(g_buf_size)
        print 'recv from:',
        print clientAddr,
        print 'data:',
        print recvData

        outSocket.sendto(recvData, outAddr)
        print 'send:',
        print recvData,
        print 'to:',
        print outAddr

        outSerial.write(recvData)
        print 'send to:',
        print ser.portstr,
        print ser.baudrate,
        print 'data:',
        print recvData
        print

def Serial2Wifi(ser, wifiAddr):
    outSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    buf = ''
    while True:
        recvData = ser.read(g_serial_buf_size)
        print 'recv from:',
        print ser.portstr,
        print ser.baudrate,
        print 'data:',
        print recvData

        if '\n' != recvData: # a serial frame end with '\n'
            buf += recvData
        else:
            outSocket.sendto(buf, wifiAddr)
            print 'send:',
            print recvData,
            print 'to:',
            print wifiAddr
            print
            buf = ''

def Lan2Wifi(inSocket, outAddr):
    outSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        (recvData, clientAddr) = inSocket.recvfrom(g_buf_size)
        print 'recv from:',
        print clientAddr,
        print 'data:',
        print recvData

        outSocket.sendto(recvData, outAddr)
        print 'send:',
        print recvData,
        print 'to:',
        print outAddr
        print

if __name__ == '__main__':
    # get wifi in ip
    # global g_wifi_in_ip
    g_wifi_in_ip = GetLocalWifiIP()

    wifi_in_addr = (g_wifi_in_ip, g_wifi_in_port)
    lan_out_addr = (g_lan_out_ip, g_lan_out_port)

    lan_in_addr = (g_lan_in_ip, g_lan_in_port)
    wifi_out_addr = (g_wifi_out_ip, g_wifi_out_port)

    # open serial
    ser = serial.Serial(g_serial_name)
    ser.timeout = None
    ser.baudrate = g_baudrate

    print 'wait system startup'
    time.sleep(g_sleep_time)

    lanInSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    lanInSocket.bind(lan_in_addr)
    wifiInSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    wifiInSocket.bind(wifi_in_addr)

    print 'begin listen port:'
    print 'listen by',
    print wifi_in_addr

    print 'listen by',
    print lan_in_addr

    print 'listen by',
    print str(ser.portstr) + ' ' + str(ser.baudrate)

    # wifi to lan&serial
    thread.start_new_thread(Wifi2LanAndSerial, (wifiInSocket, lan_out_addr, ser))

    # serial to wifi
    thread.start_new_thread(Serial2Wifi, (ser, wifi_out_addr))

    # lan to wifi
    thread.start_new_thread(Lan2Wifi, (lanInSocket, wifi_out_addr))

    while True:
        print 'radioDaemon working'
        time.sleep(g_promtp_time)

