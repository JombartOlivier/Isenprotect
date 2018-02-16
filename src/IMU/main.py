#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from imu import *
from mpu6050 import mpu6050
from time import sleep

sensor = mpu6050(0x68)

averageAccel = []
averageGyro = []

averageGryo, averageAccel = imuCalibration(sensor)
print("fin calibration")
print("acceleration : ", averageAccel)
#imu.test(sensor)
imu.waitCrash(sensor, averageAccel, averageGyro)