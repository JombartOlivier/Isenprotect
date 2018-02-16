#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import SigfoxCom
import serial
from imu import *
from mpu6050 import mpu6050
 
a = SigfoxCom.Sigfox
print (dir(a))
a.openUartPort(a, "/dev/ttyAMA0", 115200, 2)
a.wakeUpSigfox(a)

a.sendData(a, "Hello World")
a.closeUartPort(a)
#a.openUartPort(a, "/dev/ttyAMA0", 9600, 2)
#a.receiveData(a, 11)
#a.closeUartPort(a)

# Imu declaration
imuAddr = 0x68
averageAcceleration = []
averageGyroscope = []
imu = mpu6050(imuAddr)

state = 0

averageGyroscope, averageAcceleration = imuCalibration(imu) 

while True:
    if state == 0:
        state = isCrash(imu, averageAcceleration, averageGyroscope)
    elif state == 1:

    





