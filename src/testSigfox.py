#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import SigfoxCom
import serial
from imu import *
from mpu6050 import mpu6050
from apresDetection4 import *
import RPi.GPIO as GPIO  
import time 
import GPS1_2
 
sigfox = SigfoxCom.Sigfox

sigfox.openUartPort(sigfox, "/dev/ttyAMA0", 115200, 2)
sleep(0.5)
sigfox.wakeUpSigfox(sigfox)
sigfox.sendData(sigfox, "Hello")
sigfox.closeUartPort(sigfox)
		
        





    





