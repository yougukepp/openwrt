#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser

gIniFileName = 'PCTools.ini'

class PCConfiger:
    def __init__(self):
        self.mConfiger = configparser.ConfigParser()
        self.mConfiger.read(gIniFileName)
    
    def GetValue(self, section, attributeName):
        value = self.mConfiger[section][attributeName]
        return value

if __name__ == '__main__': 
    configer = PCConfiger()
    value = configer.GetValue('master', 'lanip')
    print('master.lanip')
    print(value)


