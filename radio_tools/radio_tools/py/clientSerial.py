#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial

gSerialName = '/dev/ttyS0'
gBaudrate = 9600
gRequestByte = 1
gSendData = b'0123456789abcdef\r\n'

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

    nWrite = ser.write(gSendData)

    print 'write to: ',
    print ser.portstr + ',',
    print str(ser.timeout) + ',',
    print ser.baudrate,
    print ':%s' % gSendData

    ser.close()


