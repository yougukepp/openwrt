#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket

ipList = socket.gethostbyname_ex(socket.gethostname())
ipList = socket.gethostbyname(socket.gethostname())
print(ipList)

