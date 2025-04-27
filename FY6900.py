# -*- coding: utf-8 -*-
"""
Created on Sat Apr 12 14:51:45 2025

@author: Martin
"""

import serial, sys
import Messgeraete

class FY6900(Messgeraete.measdevice):
    name: str
    conn: Messgeraete.connection
    
    def __init__(self, port: str, name: str="FY6900"):
        self.name = name
        self.conn = Messgeraete.connection(useVISA=False, addr=port, postfix="\n" , stopbits=serial.STOPBITS_TWO)
    
    def initSine(self, cha: int=1, volt: float=1.0, offs: float=0.0, freq: float=10.0):
        if cha==0 or cha > 2:
            return False
        initcmds = [["WMW0", "WMF" + str(freq), "WMA" + str(int(volt*10000)/10000), "WMO" + str(int(offs*1000)/1000)]]
        initcmds.append(["WFW0", "WFF" + str(freq), "WFA" + str(int(volt*10000)/10000), "WFO" + str(int(offs*1000)/1000)])
        for tempcmd in initcmds[cha-1]:
            tempsuccess = self.sendCommand(tempcmd)
            if tempsuccess is False:
                return False
        return True
    
    def setVolt(self, volt: float=1.0, cha: int=1):
        if cha==0 or cha > 2:
            return False
        tempcommand = ["WMA", "WFA"]
        tempsuccess = self.sendCommand(tempcommand[cha-1] + str(int(volt*10000)/10000))
        return tempsuccess
    
    def setOffs(self, offs: float=1.0, cha: int=1):
        if cha==0 or cha > 2:
            return False
        tempcommand = ["WMO", "WFO"]
        tempsuccess = self.sendCommand(tempcommand[cha-1] + str(int(offs*1000)/1000))
        return tempsuccess
    
    def setFreq(self, freq: float=1.0, cha: int=1):
        if cha==0 or cha > 2:
            return False
        tempcommand = ["WMF", "WFF"]
        tempsuccess = self.sendCommand(tempcommand[cha-1] + str(freq))
        return tempsuccess
    
    def setOutput(self, onoff: bool=False, cha: int=1):
        if cha==0 or cha > 2:
            return False
        tempcommand = ["WMN", "WFN"]
        tempsuccess = False
        if onoff is False:
            tempsuccess = self.sendCommand(tempcommand[cha-1] + "0")
        else:
            tempsuccess = self.sendCommand(tempcommand[cha-1] + "1")
        return tempsuccess
    
testdevice = FY6900("COM3")
if not testdevice.connect():
    sys.exit()
testdevice.initSine()
testdevice.setFreq(10)
testdevice.setVolt(2)
testdevice.setOutput(True)
testdevice.setFreq(100)
testdevice.setFreq(1000)
testdevice.initSine(2)
testdevice.setFreq(100, 2)
testdevice.setOutput(True, 2)
testdevice.setOutput(False)
testdevice.setOutput(False, 2)
testdevice.disconnect()