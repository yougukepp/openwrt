#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial

gSerialName = '/dev/ttyUSB1'
gBaudrate = 9600
gRequestByte = 1

if __name__ == "__main__":
    ser = serial.Serial(
            port = gSerialName,
            baudrate = gBaudrate,
            bytesize = serial.EIGHTBITS,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            timeout = None,
            xonxoff = False,
            rtscts = False,
            writeTimeout = None,
            dsrdtr = False,
            interCharTimeout = None)

    print('wating for message...  ', end = '')
    print(ser.portstr + ',', end = '')
    print(str(ser.timeout) + ',', end = '')
    print(ser.baudrate)

    while True:
        r = ser.read()
        print(r)

    ser.close()

