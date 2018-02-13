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
 	liste.append(x[20])
 	liste.append(x[21])
 	liste.append(x[22])
 	liste.append(x[23])

 	liste.append(x[25])
 	liste.append(x[26])
 	
 	#EST
 	liste.append(x[33])
 	liste.append(x[34])
 	liste.append(x[35])
 	liste.append(x[36])
 	
 	liste.append(x[38])
 	liste.append(x[39])
 	 	
 	l=''.join(chr(i) for i in liste)
 	print(l)
 	print(len(l))
 	break



