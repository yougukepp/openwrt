#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial

gSerialName = 'COM2'
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

    print('write to: ', end = '')
    print(ser.portstr + ',', end = '')
    print(str(ser.timeout) + ',', end = '')
    print(ser.baudrate)
    print('%d:%s' % (nWrite, gSendData))

    ser.close()


