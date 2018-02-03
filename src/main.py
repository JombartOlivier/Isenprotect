#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import SigfoxCom.py
import serial

a = SigfoxCom
a.baudRate = 9600
baud = a.baudRate
print "baude rate", baud, "\n"
a.port = "/dev/ttyAMA0"
print "port", a.port, "\n"
a.timeOut = 2
print "time out", a.timeOut, "\n"
a.openUartPort(a.port, a.baudRate, a.timeOut)

