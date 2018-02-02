#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
class SigfoxCom(object):

    def __init__(self):
        self._port = ""
        self._baudRate = 0
        self._timeOut = 0

    def _set_port(self, port):
        self._port = port
    
    def _set_baudRate(self, baudRate):
        self._baudRate = baudRate
    
    def _set_timeOut(self, timeOut):
        self._timeOut = timeOut

    def _get_port(self):
        return self._port

    def _get_baudRate(self):
        return self._baudRate

    def _get_timeOut(self):
        return self._timeOut
    
    port = property(_get_port, _set_port)
    baudRate = property(_get_baudRate, _set_baudRate)
    timeOut = property(_get_timeOut, _set_timeOut)
    
