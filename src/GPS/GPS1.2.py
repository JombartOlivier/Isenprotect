#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import serial




class GPS:
	
	def __init__ (self) :

		self.lattitude=[]
		self.longitude=[]
		self._port = ""
        	self._baudRate = 0
       	self._timeOut = 0
        	self._serialPort
		
     def _set_serialPort(self, serialPort):
          self._serialPort

     def _set_port(self, port):
          self._port = port
    
     def _set_baudRate(self, baudRate):
          self._baudRate = baudRate
    
     def _set_timeOut(self, timeOut):
          self._timeOut = timeOut

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
		


     port = property(_get_port, _set_port)
    	baudRate = property(_get_baudRate, _set_baudRate)
   	timeOut = property(_get_timeOut, _set_timeOut)
    	serialPort = property(_get_serialPort, _set_serialPort)
    	longitude = property(_get_longitude, _set_longitude)
    	lattitude = property(_get_lattitude, _set_lattitude)

    	def openUartPort(self, port, baudRate, timeout):

        self.port = port
        self.baudRate = baudRate
        self.timeOut = timeout

        
        print("Parametre de la liaison Uart :")
        print("Port       : ", self.port)
        print("Baude rate : ", self.baudRate)
        print("timeout   : " , self.timeOut)

        self.serialPort = serial.Serial(self.port, self.baudRate, timeout = self.timeOut)

    	def closeUartPort(self):
       self.serialPort.close()

	def setDataGPS() :

		self.lattitude = lattitude
		self.longitude = longitude
		self.serialPort = ser

		liste=[]
		while 1:
		 x=ser.readline()
		 if x[3]==82: #on veut la valeur du GPRMC
		 	#GPRMC
		 	liste.append(x[0])
		 	liste.append(x[1])
		 	liste.append(x[2])
		 	liste.append(x[3])
		 	liste.append(x[4])
		 	liste.append(x[5])
		 	
		 	#lattitude
		 	lattitude.append(x[20])
		 	lattitude.append(x[21])
		 	lattitude.append(x[22])
		 	lattitude.append(x[23])

		 	lattitude.append(x[25])
		 	lattitude.append(x[26])
		 	lattitude.append(x[27])
		 	lattitude.append(x[28])
		 	#longitude
		 	longitude.append(x[33])
		 	longitude.append(x[34])
		 	longitude.append(x[35])
		 	longitude.append(x[36])
		 	
		 	longitude.append(x[38])
		 	longitude.append(x[39])
		 	longitude.append(x[40])
		 	longitude.append(x[41])
		 	
		 	l=''.join(chr(i) for i in liste)
		 	lattitudePrint=''.join(chr(j) for j in lattitude)
		 	longitudePrint=''.join(chr(k)	for k in longitude)
		 	print(l)
		 	print(lattitude)
		 	print(longitude)
		 	del(l[:])
		 	break
		
	def clearDataGps():

	del(lattitude[:])
	del(longitude[:])


