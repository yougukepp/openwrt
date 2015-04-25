#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial

gSerialName = '/dev/ttyUSB1'
sendData = b'0123456789abcdef'

def test(timeOut, recvBufSize, baudrate):
    ser = serial.Serial(gSerialName)
    ser.timeout = timeOut
    ser.baudrate = baudrate 
    
    print('wating for message...', end = '') 
    print(ser.portstr + ',', end = '')
    print(ser.baudrate)

    r = ser.read(recvBufSize)
    print(r)

    #ser.close()

if __name__ == "__main__":
    recvBufSize = 1024
    timeOut = None
    baudrate = 9600
    test(timeOut, recvBufSize, baudrate)

