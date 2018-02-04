#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import SigfoxCom
import serial

a = SigfoxCom.Sigfox
print (dir(a))
a.openUartPort(a, "/dev/ttyAMA0", 9600, 2)
a.wakeUpSigfox(a)
a.closeUartPort(a)
