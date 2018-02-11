#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import serial




class GPS:
	
	def __init__ (self) :

		self._lattitude=[]
		self._longitude=[]
		self._port=""
		#self._baudRate=0
		self._timeOut=0
		self._serialPort

	def _set_serialPort(self, serialPort):
		self._serialPort

	def _set_port(self, port):
		self._port=port

	def _set_baudRate(self, baudRate):
		self._baudRate=baudRate

	def _set_timeOut(self, timeOut):
		self._timeOut=timeOut

	def _set_lattitude(self, lattitude):
		self._lattitude=lattitude

	def _set_longitude(self, longitude):
		self._longitude=longitude

	def _get_serialPort(self):
		return self._serialPort

	def _get_port(self):
		return self._port

	def _get_baudRate(self):
		return self._baudRate

	def _get_timeOut(self):
		return self._timeOut

	def _get_lattitude (self):
		return self._lattitude

	def _get_longitude(self):
		return self._longitude
		

	def setDataGPS() :

		self.lattitude = lattitude
		self.longitude = longitude
		self.serialPort = ser
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
		 			lattitude.append(x[i])
			
		 		#EST
		 		for i in range(33,39) :
		 			if i==37 :
		 				i=38
		 			longitude.append(x[i])
		 	 	
		 		lattitudePrint=''.join(chr(j) for j in lattitude)
		 		longitudePrint=''.join(chr(k)	for k in longitude)
		 		
		 		print(lattitude)
		 		print(longitude)
		 		
		 		break
		
		
	def clearDataGps():

		del(lattitude[:])
		del(longitude[:])


	port = property(_get_port, _set_port)
	baudRate = property(_get_baudRate, _set_baudRate)
	timeOut = property(_get_timeOut, _set_timeOut)
	serialPort = property(_get_serialPort, _set_serialPort)
	longitude = property(_get_longitude, _set_longitude)
	lattitude = property(_get_lattitude, _set_lattitude)