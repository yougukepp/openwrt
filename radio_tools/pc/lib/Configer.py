#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser

gIniFileName = 'Config.ini'

class Configer:
    def __init__(self, section):
        self.mConfiger = configparser.ConfigParser()
        self.mConfiger.read(gIniFileName, encoding='utf8')
        self.mSection = section

    def GetValue(self, attributeName):
        hasValidSection = False
        section = self.mSection

        #print('in Configer.GetValue:', end='')
        #print(section + ' ', end = '')
        #print(attributeName)

        # 在ini文件中查找section是否有效
        for k in self.mConfiger:
            if k == section:
                hasValidSection = True
                break

        value = None
        if hasValidSection: # section无效则返回None
            value = self.mConfiger[section][attributeName]

        return value

if __name__ == '__main__':
    configer = Configer()
    configer.GetValue('lanip')


