#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import serial

liste=[]

#UART BAUDRATE 9600
ser = serial.Serial(
 port='/dev/ttyAMA0',
 baudrate = 9600,
 parity=serial.PARITY_NONE,
 stopbits=serial.STOPBITS_ONE,
 bytesize=serial.EIGHTBITS,
 timeout=1
)
counter=0


while 1:
 x=ser.readline()
 if x[3]==82:
 	 	
 	#NORD
 	for i in range(20,26) :
 		
 		if i==24 :
 			i=25
 		liste.append(x[i])
	
 	#EST
 	for i in range(33,39) :
 		if i==37 :
 			i=38
 		liste.append(x[i])
 	 	
 	l=''.join(chr(i) for i in liste)
 	print(l)
 	print(len(l))
 	break



