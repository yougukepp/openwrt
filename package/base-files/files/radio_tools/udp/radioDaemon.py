#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 测试方法:
# 需要设置一台ap主 一台sta从
# 电脑WIFI 192.168.10.124  sta

# 主WIFI   192.168.10.1    ap

# 从WIFI   192.168.10.125  sta 上行口
# 从LAN    192.168.11.1        下行口

# 电脑LAN  192.168.11.124


# 主设备就是路由器 无需代码
# 从设备需要代码

import time
import socket
import thread 
import serial

g_sleep_time = 0
g_promtp_time = 10

# wifi interface
g_wifi_in_ip = '192.168.2.102'
g_wifi_in_port = 8001
g_wifi_out_ip = '192.168.2.100'
#g_wifi_out_port = 8002
g_wifi_out_port = 8001

# lan interface
g_lan_in_ip = '192.168.10.1'
g_lan_in_port = 8001
g_lan_out_ip = '192.168.10.3'
#g_lan_out_port = 8002
g_lan_out_port = 8001

# serial interface
g_serial_name = '/dev/ttyS0'
g_baudrate = 9600

# recv bufsize
g_buf_size = 1024

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

    while True: 
        recvData = ser.read(g_buf_size)
        print 'recv from:',
        print ser.portstr,
        print ser.baudrate,
        print 'data:',
        print recvData

        outSocket.sendto(recvData, wifiAddr)
        print 'send:',
        print recvData,
        print 'to:',
        print wifiAddr
        print

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
    wifi_in_addr = (g_wifi_in_ip, g_wifi_in_port)
    lan_out_addr = (g_lan_out_ip, g_lan_out_port)

    lan_in_addr = (g_lan_in_ip, g_lan_in_port)
    wifi_out_addr = (g_wifi_out_ip, g_wifi_out_port)

    lanInSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    lanInSocket.bind(lan_in_addr) 

    wifiInSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    wifiInSocket.bind(wifi_in_addr) 

    # open serial
    ser = serial.Serial(g_serial_name)
    ser.timeout = None
    ser.baudrate = g_baudrate

    time.sleep(g_sleep_time)

    # wifi to lan&serial
    thread.start_new_thread(Wifi2LanAndSerial, (wifiInSocket, lan_out_addr, ser))  

    # serial to wifi
    thread.start_new_thread(Serial2Wifi, (ser, wifi_out_addr))  

    # lan to wifi
    thread.start_new_thread(Lan2Wifi, (lanInSocket, wifi_out_addr))  

    while True:
        print 'radioDaemon working'
        time.sleep(g_promtp_time)
