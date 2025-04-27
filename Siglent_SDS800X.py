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
    
    def getScreenshot(filename: str, picformat: str="PNG"):                     #Prog Manual P32
        return NotImplemented
    
    def setAquireRateMode(self, acqratemode: int, check: bool=False):           #Prog Manual P35
        tempstr = ""
        if acqratemode == 0:
            tempstr = "FAST"
        elif acqratemode == 1:
            tempstr = "SLOW"
        else:
            return False
        self.sendCommand(":ACQ:AMOD " + tempstr)
        if check:
            return self.queryCommand(":ACQ:AMOD?", tempstr)
        return True
        
    def getAquireMode(self, expAcqMode: str=None):
        return self.queryCommand(":ACQ:AMOD?", expAcqMode)
    
    def clearSweep(self):
        self.conn.sendCommand(":ACQ:CSW")
        self.waitOPC()
        return True
    
    def setInterpolation(self, interpolation: bool, check: bool=False):         #Prog Manual P36
        tempstr = ""
        if interpolation:
            tempstr = "ON"
        else:
            tempstr = "OFF"
        self.sendCommand(":ACQ:INT " + tempstr)
        if check:
            return self.queryCommand(":ACQ:INT?", tempstr)
        return True    
    
    def getInterpolation(self, expInterpolation: str=None):          
        return self.queryCommand(":ACQ:AMOD?", expInterpolation)
    
    def setMemManag(self, memManag: int, check: bool=False):                    #Prog Manual P37
        tempstr = ""
        if memManag == 2:
            tempstr = "FSR"
        elif memManag == 3:
            tempstr = "FMD"
        else:
            tempstr = "AUTO"
        self.sendCommand(":ACQ:MMAN " + tempstr)
        if check:
            return self.queryCommand(":ACQ:MMAN?", tempstr)
        return True    
    
    def getMemManag(self, expInterpolation: str=None):          
        return self.queryCommand(":ACQ:MMAN?", expInterpolation)
    
    def setAcqMode(self, AcqMode: int, check: bool=False):                      #Prog Manual P38
        tempstr = ""
        if AcqMode == 2:
            tempstr = "XY"
        elif AcqMode == 3:
            tempstr = "ROLL"
        else:
            tempstr = "YT"
        self.sendCommand(":ACQ:MODE " + tempstr)
        if check:
            return self.queryCommand(":ACQ:MODE?", tempstr)
        return True    
    
    def getAcqMode(self, expAcqMode: str=None):          
        return self.queryCommand(":ACQ:MODE?", expAcqMode)
    
    def setMemDepth(self, MemDepth: float, check: bool=False):                  #Prog Manual P39
        """
        Sets the memory depth for data acquisition.
        
        Args:
            MemDepth (float): The desired memory depth in MSa.
            check (bool, optional): If True, verifies that the memory depth was correctly applied. Defaults to False.
        
        Possible Memory Depths and Ranges:
            - "10k"   : 0 < MemDepth <= 0.01
            - "100k"  : 0.01 < MemDepth <= 0.1
            - "1M"    : 0.1 < MemDepth <= 1
            - "10M"   : 1 < MemDepth <= 10
            - "50M"   : 10 < MemDepth <= 50
        
        Returns:
        bool: True if the command was sent successfully (and optionally verified), False if MemDepth is out of range.
        """
        tempstr = ""
        if MemDepth <= 0.01:
            tempstr = "10k"
        elif MemDepth <= 0.1:
            tempstr = "100k"
        elif MemDepth <= 1:
            tempstr = "1M"
        elif MemDepth <= 10:
            tempstr = "10M"
        elif MemDepth <= 25:
            tempstr = "25M"
        elif MemDepth <= 50:
            tempstr = "50M"
        else:
            return False
        
        self.sendCommand(":ACQ:MDEP " + tempstr)
        if check:
            return self.queryCommand(":ACQ:MDEP?", tempstr)
        return True
    
    def getMemDepth(self, expMemDepth: str=None):
        """
        Retrieves the current memory depth acquisition setting.
    
        Args:
            expMemDepth (str, optional): The expected memory depth value to validate against. If provided,
                the function checks if the retrieved value matches this expectation and returns True or False.
                Defaults to None.
    
        Returns:
            Union[str, bool]: 
                - If expMemDepth is not provided, returns the current memory depth setting as a string.
                - If expMemDepth is provided, returns True if the retrieved value matches expMemDepth,
                  otherwise returns False.
    
        Note:
            The possible memory depth values are "10k", "100k", "1M", "10M", "25M" and "50M".
            These correspond to specific acquisition ranges as defined in the setMemDepth method.
        """
        return self.queryCommand(":ACQ:MDEP?", expMemDepth)
    
    def getNumWavef(self):                                                      #Prog Manual P41
        return self.queryCommand(":ACQ:NUMA?")
    
    def getNumPoints(self):                                                     #Prog Manual P41
        return self.queryCommand(":ACQ:POIN?")

    def setSeq(self, Sequence: bool, check: bool=False):                        #Prog Manual P43
        tempstr = ""
        if Sequence is True:
            tempstr = "ON"
        else:
            tempstr = "OFF"
        self.sendCommand(":ACQ:SEQ " + tempstr)
        if check:
            return self.queryCommand(":ACQ:SEQ?", tempstr)
        return True    
    
    def getSeq(self, expSeqState: str=None):
        return self.queryCommand(":ACQ:SEQ?", expSeqState)

    def setSeqCount(self, count: int, check: bool=False):                       #Prog Manual P44
        if count < 1:
            return False
        
        tempstr = str(count)
        self.sendCommand(":ACQ:SEQ:COUN " + tempstr)
        if check:
            return self.queryCommand(":ACQ:SEQ:COUN?", tempstr)
        return True    
    
    def getSeqCount(self, expSeqCount: str=None):
        return self.queryCommand(":ACQ:SEQ:COUN?", expSeqCount)

    def setSampleRate(self, Samplerate: float, check: bool=False):              #Prog Manual P45
        if Samplerate <= 0:
            return False
    
        tempstr = str(Samplerate)     
        self.sendCommand(":ACQ:SRAT " + tempstr)
        if check:
            return self.queryCommand(":ACQ:SRAT?", tempstr)
        return True
    
    def getSampleRate(self, expSampleRate: str=None):          
        return self.queryCommand(":ACQ:SRAT?", expSampleRate)
    
    
    
testdevice = Siglent_SDS800X_HD('TCPIP0::192.168.0.194::inst0::INSTR')
testdevice.connect()
print(testdevice.getIDN())
if False:
    testdevice.reset()
    print(testdevice.setAquireMode(1))
    print(testdevice.setMemDepth(0.01, True))
    time.sleep(2)
    print(testdevice.setMemDepth(0.1, True))
    time.sleep(2)
    print(testdevice.setMemDepth(1, True))
    time.sleep(2)
    print(testdevice.setMemDepth(10, True))
    time.sleep(2)
    print(testdevice.setMemDepth(50, True))
    time.sleep(2)
testdevice.disconnect()