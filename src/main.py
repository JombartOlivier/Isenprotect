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
gps = GPS1_2.GPS

ledGpioNumber = 26
boutonNumber = 25

#setting GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(ledGpioNumber,GPIO.OUT) 							   #LED du bouton
GPIO.setup(boutonNumber, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#setting Multiplexeur
GPIOenableMultiplexeur = 17
GPIO.setup(GPIOenableMultiplexeur, GPIO.OUT)



tempAttente = 20
# Imu declaration
imuAddr = 0x68
averageAcceleration = []
averageGyroscope = []
imu = mpu6050(imuAddr)


state = 0

averageGyroscope, averageAcceleration = imuCalibration(imu) 

# Define a threaded callback function to run in another thread when events are detected  
def my_callback(cha): 
	global state
	state=3
	
    

#detection changement d'état et appel de la fonction callback
GPIO.add_event_detect(boutonNumber, GPIO.RISING, callback=my_callback)
finProgramme = True
print("etat : ",state)
while finProgramme == True:
	#print("etat : ", state)	
	#etat de detection d'accident via l'IMU
	if state == 0:
		state = isCrash(imu, averageAcceleration, averageGyroscope)
		GPIO.output(ledGpioNumber,GPIO.LOW)
		temp = time.time()
	elif state == 1:
		print("etat : ",state)
		GPIO.output(ledGpioNumber,GPIO.HIGH)
		play_music(state)
		x= int(time.time() - temp)
		print("temps d'attente :", x)
		if (time.time() - temp) > tempAttente:
			state = 2
        
    #etat si l'utilisateur n'a pas appuyé sur le bouton   
	elif state == 2:
		print("etat : ",state)
		GPIO.output(GPIOenableMultiplexeur, GPIO.LOW)
		GPIO.output(ledGpioNumber, GPIO.LOW)
		play_music(state)
		gps.setDataGps(gps)
		lattitude = gps.lattitude
		longitude = gps.longitude
		coordonnees = lattitude + longitude
		# close port
		print("lattitude : ", lattitude)
		print("longitude : ", longitude)
		sleep(0.5)
		GPIO.output(ledGpioNumber, GPIO.HIGH)
		sigfox.openUartPort(sigfox, "/dev/ttyAMA0", 115200, 2)
		sleep(0.5)
		sigfox.wakeUpSigfox(sigfox)
		sigfox.sendData(sigfox, coordonnees)
		sigfox.closeUartPort(sigfox)
		finProgramme = False
	#etat si l'utilisateur a appuyé sur le bouton
	elif state == 3:
		print("etat : ",state)
		GPIO.output(ledGpioNumber,GPIO.LOW)
		play_music(state)
		state = 0 #on revient à l'état 1
		print("etat : ",state)

        





    





