#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import serial
L = [104, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100]
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
 print (x[3])
 if x[3]==82:
 	print("coucou")
 else :	
 	print("non")

 s=''.join(chr(i) for i in L)
 print (s)