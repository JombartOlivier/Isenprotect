#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import imu
from mpu6050 import mpu6050
from time import sleep

sensor = mpu6050(0x68)

averageAccel = []
averageGyro = []

averageAccel, averageGyro = imu.Calibration(sensor)
print("fin calibration")
print("acceleration : ", averageAccel)
imu.test(sensor)
imu.waitCrash(sensor, averageAccel, averageGyro)