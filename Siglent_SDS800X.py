# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 17:15:01 2025

@author: Martin
"""

import time
import Messgeraete

class Siglent_SDS800X_HD(Messgeraete.measdevice):
    name: str
    conn: Messgeraete.connection
    IDN: str=""
    
    def __init__(self, addr: str, name: str="SDS800X_HD"):
        self.name = name
        self.conn = Messgeraete.connection(useVISA=True, addr=addr)

    def getIDN(self):
        self.IDN = self.conn.queryCommand("*IDN?").strip()
        return self.IDN

    def waitOPC(self):
        self.conn.queryCommand("*OPC?")
        return True
    
    def reset(self):
        self.conn.sendCommand("*RST")
        time.sleep(5)
        self.waitOPC()
        return True
    
    def getScreenshot(filename: str, picformat: str="PNG"):
        return NotImplemented
    
    def setAquireMode(self, acqmode: int):
        tempstr = ""
        if acqmode == 0:
            tempstr = "FAST"
        elif acqmode == 1:
            tempstr = "SLOW"
        else:
            return False
        self.sendCommand(":ACQ:AMOD " + tempstr)
        return self.queryCommand(":ACQ:AMOD?", tempstr)
        
    def getAquireMode(self, expAcqMode: str=None):
        return self.queryCommand(":ACQ:AMOD?", expAcqMode)
    
    def setTimebase(self, newTimebase: int, newUnit: str):
        curTimebase = self.getTimebase()
        return curTimebase
    
    def getTimebase(self):
        return 0
    
    def setDvisions(self, newDivisions: int, newUnit: str):
        curDivisons = self.getDivisions()
        return curDivisons
        
    def getDivisions(self):
        return 0
    
testdevice = Siglent_SDS800X_HD('TCPIP0::192.168.0.194::inst0::INSTR')
testdevice.connect()
print(testdevice.getIDN())
#testdevice.reset()
print(testdevice.setAquireMode(1))
testdevice.disconnect()