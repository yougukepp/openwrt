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
g_wifi_out_port = 8002

# lan interface
g_lan_in_ip = '192.168.10.1'
g_lan_in_port = 8001
g_lan_out_ip = '192.168.10.3'
g_lan_out_port = 8002

# serial interface
g_serial_name = '/dev/ttyS0'
g_baudrate = 9600

# recv bufsize
g_buf_size = 1024

def NetRouter(inSocket, outAddr):  
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
        print

    inSocket.close()
    outSocket.close()

def Serial2Wifi(ser, wifiAddr):  
    outSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

    while True: 
        recvData = ser.read(g_buf_size)
        print 'recv from:',
        print serialName,
        print baudrate,
        print 'data:',
        print recvData

        outSocket.sendto(recvData, wifiAddr)
        print 'send:',
        print recvData,
        print 'to:',
        print wifiAddr
        print
        print

    ser.close()
    outSocket.close()


def Wifi2Serial(inSocket, ser):  
    while True:
        (recvData, clientAddr) = inSocket.recvfrom(g_buf_size) 
        print 'recv from:',
        print clientAddr,
        print 'data:',
        print recvData 
        
        w = ser.write(recvData)
        print 'send to:',
        print serialName,
        print baudrate,
        print 'data:',
        print recvData

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

    # wifi to lan
    thread.start_new_thread(NetRouter, (wifiInSocket, lan_out_addr))  
    # lan to wifi
    thread.start_new_thread(NetRouter, (lanInSocket, wifi_out_addr))  
    # wifi to serial
    thread.start_new_thread(Wifi2Serial, (wifiInSocket, ser))  
    # serial to wifi
    thread.start_new_thread(Serial2Wifi, (ser, wifi_out_addr))  

    while True:
        print 'radioDaemon working'
        time.sleep(g_promtp_time)

