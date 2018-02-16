#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import SigfoxCom
import serial
from imu import *
from mpu6050 import mpu6050
from apresDectection4 import *
import RPi.GPIO as GPIO  
import time 
import GPS1_2
 
sigfox = SigfoxCom.Sigfox

sigfox.openUartPort(sigfox, "/dev/ttyAMA0", 115200, 2)
sigfox.closeUartPort(sigfox)

gps = GPS1_2.GPS
#a.openUartPort(a, "/dev/ttyAMA0", 9600, 2)
#a.receiveData(a, 11)
#a.closeUartPort(a)

ledGpioNumber = 18
boutonNumber = 25

tempAttentes = 20
# Imu declaration
imuAddr = 0x68
averageAcceleration = []
averageGyroscope = []
imu = mpu6050(imuAddr)

global state = 0

averageGyroscope, averageAcceleration = imuCalibration(imu) 

# Define a threaded callback function to run in another thread when events are detected  
def my_callback(cha):  
    state=3
    

#detection changement d'état et appel de la fonction callback
GPIO.add_event_detect(25, GPIO.RISING, callback=my_callback)
finProgramme = True

while finProgramme == True:
    print("etat : " state)
    if state == 0:
        state = isCrash(imu, averageAcceleration, averageGyroscope)
        GPIO.output(GpioNumber,GPIO.LOW)
        temp = time.time()

    elif state == 1:
        GPIO.output(GpioNumber,GPIO.HIGH)
        play_music(state)
        print("temps d'attente", time.time() - temp)
        if time.time() - temp => tempAttentes:
            state = 2
        else:
            state = 3
        
    elif state = 2:
        GPIO.output(GpioNumber,GPIO.LOW)
        play_music(state)
        
        gps.setDataGps(gps)
        lattitude = gps.lattitude
        longitude = gps.longitude
        # close port

        sigfox.wakeUpSigfox(sigfox)
        sigfox.sendData(sigfox, lattitude)
        sleep(0.5)
        sigfox.sendData(sigfox, longitude)

        state = 3
        finProgramme = False

    elif state = 3:
        GPIO.output(GpioNumber,GPIO.LOW)
        play_music(state)
        state = 0
        





    





