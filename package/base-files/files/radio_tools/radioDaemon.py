#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 需要设置一台ap主 一台sta从
# 电脑WIFI 192.168.10.124  sta
# 主WIFI   192.168.10.1    ap
# 从WIFI   192.168.10.125  sta
# 从LAN    192.168.11.1
# 电脑LAN  192.168.11.124

import time
import socket

g_sleep_time = 300

g_in_ip = '192.168.10.1'
g_in_port = 8001
g_in_addr = (g_in_ip, g_in_port)
g_udp_in_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
g_udp_in_socket.bind(g_in_addr)

g_out_ip = '192.168.2.100'
g_out_port = 8001
g_out_addr = (g_out_ip, g_out_port)
g_udp_out_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

g_buf_size = 1024

def router(): 
    (recvData, clientAddr) = g_udp_in_socket.recvfrom(g_buf_size) 
    print 'recv from:',
    print clientAddr,
    print 'data:',
    print recvData

    g_udp_out_socket.sendto(recvData, g_out_addr)
    print 'send:',
    print recvData,
    print 'to:',
    print g_out_addr

if __name__ == '__main__':
    print 'begin'
    #time.sleep(g_sleep_time)
    router()
    print 'end'

