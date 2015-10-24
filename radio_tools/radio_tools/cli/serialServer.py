#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial

gSerialName = '/dev/ttyS0'
gBaudrate = 9600
gTimeout = 0
gRequestByte = 1

if __name__ == "__main__":
    ser = serial.Serial(
            port = gSerialName,
            baudrate = gBaudrate,
            bytesize = serial.EIGHTBITS,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            timeout = gTimeout,
            xonxoff = False,
            rtscts = False,
            writeTimeout = None,
            dsrdtr = False,
            interCharTimeout = None)

    print 'wating for message...  ',
    print ser.portstr + ',',
    print str(ser.timeout) + ',',
    print ser.baudrate

    while True:
        r = ser.read(gRequestByte)
        if 0 != len(r):
            print repr(r)

    print
    ser.close()

