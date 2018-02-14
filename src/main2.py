#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import GPS1_2

import SigfoxCom
a = GPS1_2.GPS
b= SigfoxCom.Sigfox
print (dir(a))
a.setDataGps(a)
a._get_lattitude(a)
a._get_longitude(a)
a._set_lattitude(a,"553520")
a._set_longitude(a,"034343")
b.openUartPort(b,"ttyAMA0",115200,2)
b.wakeUpSigfox(b)
b.sendData(b,a._get_lontgitude)
b.closeUartPort()

