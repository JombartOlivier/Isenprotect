#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import serial




class GPS:
	
	def __init__ (self) :

		self._lattitude=""
		self._longitude=""

	def _set_lattitude(self, lattitude):
		self.lattitude=lattitude
		print(self.lattitude)

	def _set_longitude(self, longitude):
		self.longitude=longitude
		print(self.longitude)

	def _get_lattitude(self):
		print(self.lattitude)
		return self.lattitude

	def _get_longitude(self):
		print(self.longitude)
		return self.longitude
		

	def setDataGps(self) :

		lattitudePrint=[]
		longitudePrint=[]
		
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
		 			lattitudePrint.append(x[i])
			
		 		#EST
		 		for j in range(33,39) :
		 			if j==37 :
		 				j=38
		 			longitudePrint.append(x[j])
		 	 	
		 		lattitudePrint2=''.join(chr(j) for j in lattitudePrint)
		 		longitudePrint2=''.join(chr(k) for k in longitudePrint)
		 		self.lattitude=lattitudePrint2
		 		self.longitude=longitudePrint2
		 		#print(self.lattitude)
		 		#print(self.longitude)
		 		ser.close()
		 		break
		
		
	def clearDataGps(self):

		self.longitude=""
		self.lattitude=""
  



	
	longitude = property(_get_longitude, _set_longitude)
	lattitude = property(_get_lattitude, _set_lattitude)