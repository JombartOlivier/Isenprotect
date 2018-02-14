#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import Sigfox/SigfoxCom
import serial

a = SigfoxCom.Sigfox
print (dir(a))
a.openUartPort(a, "/dev/ttyAMA0", 115200, 2)
a.wakeUpSigfox(a)

a.sendData(a, "Hello World")
a.closeUartPort(a)
#a.openUartPort(a, "/dev/ttyAMA0", 9600, 2)
#a.receiveData(a, 11)
#a.closeUartPort(a)
