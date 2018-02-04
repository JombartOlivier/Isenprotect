#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import serial

class Sigfox:

    def __init__(self):
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

    def _get_serialPort(self):
        return self._serialPort

    def _get_port(self):
        return self._port

    def _get_baudRate(self):
        return self._baudRate

    def _get_timeOut(self):
        return self._timeOut

    port = property(_get_port, _set_port)
    baudRate = property(_get_baudRate, _set_baudRate)
    timeOut = property(_get_timeOut, _set_timeOut)
    serialPort = property(_get_serialPort, _set_serialPort)

    
    def openUartPort(self, port, baudRate, timeout):

        self.port = port
        self.baudRate = baudRate
        self.timeOut = timeout

        
        print("Parametre de la liaison Uart :")
        print("Port       : ", self.port)
        print("Baude rate : ", self.baudRate)
        print("timeout    : " , self.timeOut)

        self.serialPort = serial.Serial(self.port, self.baudRate, timeout = self.timeOut)

    def closeUartPort(self):
        self.serialPort.close()

    def wakeUpSigfox(self):

        charToSend = ['A','T','$','S','F','=']
        charToByte = list()
        i = 0

        while i < len(charToSend):

            print("start : ", i, charToSend[i])
            temp1 = charToSend[i]
            temp1 = temp1.encode()
            charToByte.append(temp1)
            print("else", temp1)

            i = i+1     

        print("char To Send : ", charToSend)
        print("char To Byte : ", charToByte )
        print("taille", len(charToByte))

        #temp2 = "ÿ".encode()
        temp2 = str(255).encode()

        self.serialPort.write(temp2)
        self.serialPort.write(temp2)
        self.serialPort.write(temp2)
        self.serialPort.write(temp2)
        self.serialPort.write(temp2)
        self.serialPort.write(charToByte[0])
        self.serialPort.write(charToByte[1])
        self.serialPort.write(charToByte[2])
        self.serialPort.write(charToByte[3])
        self.serialPort.write(charToByte[4])
        self.serialPort.write(charToByte[5])

    def sendData(self, message):
        temp = message.encode()
        print("message : ", temp)
        temp2 = str(44).encode()
        temp3 = str(48).encode()
        temp4 = str(13).encode()
        self.serialPort.write(temp)
        self.serialPort.write(temp2)
        self.serialPort.write(temp3)
        self.serialPort.write(temp4)

    
    def receiveData(self, size):
        temp = self.serialPort.read(size)
        print("message reçu raw : ", temp)
        message = temp.decode()
        print("message reçu : ", message)


       
     

    



    
