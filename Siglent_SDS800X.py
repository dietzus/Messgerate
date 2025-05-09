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
    NrChannels: int
    bandwidth: int
    
    def __init__(self, addr: str, name: str="SDS800X_HD", NrChannels: int=4, bandwidth: int=70):
        """
        Initialize a Siglent SDS 800X HD oscilloscope instance.
        
        Parameters:
            addr (str): The address of the oscilloscope, typically a VISA resource string.
            name (str, optional): Name identifier for the instrument. Defaults to "SDS800X_HD".
            NrChannels (int, optional): Number of channels on the oscilloscope. Defaults to 4.
            bandwidth (int, optional): Maximum bandwidth in megahertz (MHz). Defaults to 70.
        
        This method establishes a connection to the oscilloscope using the provided address and initializes
        its configuration with the specified parameters, including channel count and bandwidth settings.
        """

        self.name = name
        self.conn = Messgeraete.connection(useVISA=True, addr=addr)
        if NrChannels == 2 or NrChannels == 4:
            self.NrChannels = NrChannels
        else:
            return None
        if bandwidth > 200:
            return None
        elif bandwidth > 100:
            self.bandwidth = 200    	#TODO: is this smart?
        elif bandwidth > 70:
            self.bandwidth = 100
        else:
            self.bandwidth = 70

    def getIDN(self):
        """
        Queries the oscilloscope for its identification information using the *IDN? command.
    
        Returns:
            str: The identification string of the device, containing manufacturer details and model number. This value is also stored in the instance variable `self.IDN`.
        """

        self.IDN = self.conn.queryCommand("*IDN?").strip()
        return self.IDN

    def waitOPC(self):
        """
        Sends an SCPI query to the oscilloscope to check if all previous operations have completed.
        
        The function issues the '*OPC?' command, which queries the instrument to confirm whether it has finished processing 
        all preceding commands. This ensures synchronization between the software and hardware operations.
        
        Note: This function does not verify the actual completion of operations on the oscilloscope; instead, it confirms that 
        the query was successfully sent. If any errors occur during the query, they will be raised as exceptions by the underlying 
        `queryCommand` method.
        
        Returns:
            bool: True, indicating that the query was initiated successfully.
        """
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
        self.sendCommand(f":ACQ:AMOD {tempstr}")
        if check:
            return self.getAquireMode(tempstr)
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
        self.sendCommand(f":ACQ:INT {tempstr}")
        if check:
            return self.getInterpolation(tempstr)
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
            return self.getMemManag(tempstr)
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
            return self.getAcqMode(tempstr)
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
            return self.getMemDepth(tempstr)
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
    
    def getNumWavef(self, expNumWavef: int=None):                                                      #Prog Manual P41
        return self.queryCommand(":ACQ:NUMA?", expNumWavef)
    
    def getNumPoints(self, expNumPoints: int=None):                                                     #Prog Manual P41
        return self.queryCommand(":ACQ:POIN?", expNumPoints)

    def setSeq(self, Sequence: bool, check: bool=False):                        #Prog Manual P43
        tempstr = ""
        if Sequence is True:
            tempstr = "ON"
        else:
            tempstr = "OFF"
        self.sendCommand(":ACQ:SEQ " + tempstr)
        if check:
            return self.getSeq(tempstr)
        return True    
    
    def getSeq(self, expSeqState: str=None):
        return self.queryCommand(":ACQ:SEQ?", expSeqState)

    def setSeqCount(self, count: int, check: bool=False):                       #Prog Manual P44
        if count < 1:
            return False
        
        tempstr = str(count)
        self.sendCommand(":ACQ:SEQ:COUN " + tempstr)
        if check:
            return self.getSeqCount(tempstr)
        return True    
    
    def getSeqCount(self, expSeqCount: str=None):
        return self.queryCommand(":ACQ:SEQ:COUN?", expSeqCount)

    def setSampleRate(self, Samplerate: float, check: bool=False):              #Prog Manual P45
        if Samplerate <= 0:
            return False
    
        tempstr = str(Samplerate)     
        self.sendCommand(":ACQ:SRAT " + tempstr)
        if check:
            return self.getSampleRate(tempstr)
        return True
    
    def getSampleRate(self, expSampleRate: str=None):          
        return self.queryCommand(":ACQ:SRAT?", expSampleRate)
    
    def setAcquireType(self, Type: int, check: bool=False, times: int=None, bits: int=None):             #Prog Manual P46
        tempstr = ""
        if Type == 1:
            tempstr = "NORM"
        elif Type == 2:
            tempstr = "PEAK"
        elif Type == 3:
            print("Average Mode is not available for the SDS800X HD-Model.")
            return False
        elif Type == 4:
            print("ERES Mode is not available as an aquire-option for te SDS800X HD-Model.")
            print("Hint: you can use ERES as a math-function on a channel basis.")
            return False
        else:
            print("Please choose either 1 for Normal-Mode or 2 for Peak-Mode.")
            return False
        
        self.sendCommand(":ACQ:TYPE " + tempstr)
        if check:
            return self.getAcquireType(tempstr)
        return True
    
    def getAcquireType(self, expType: str=None):          
        return self.queryCommand(":ACQ:TYPE?", expType)
    
    def setChannelReference(self, Type: int, check: bool=False):             #Prog Manual P48
        tempstr = ""
        if Type == 1:
            tempstr = "OFF"
        elif Type == 2:
            tempstr = "POS"
        else:
            print("Please choose either 1 for Offset-Mode or 2 for Position-Mode.")
            return False
        
        self.sendCommand(":CHAN:REF " + tempstr)
        if check:
            return self.getChannelReference(tempstr)
        return True
    
    def getChannelReference(self, expType: str=None):          
        return self.queryCommand(":ACQ:REF?", expType)
    
    def checkChannel(self, channel: int):
        if channel > 0 and channel <= self.NrChannels:
            return True
        print(f"Invalid channel, allowed values are integers in the range of 1 to {self.NrChannels}.")
        return False
    
    def setBWLimit(self, channel: int, Limit: int, check: bool=False):             #Prog Manual P49
        if not self.checkChannel(channel):
            return False
    
        tempstr = ""
        if Limit <= 0:
            tempstr = "FULL"
        elif Limit <= 20:
            tempstr = "20M"
        elif Limit <= 200:
            print("The SDS800X HD-model only supports 20M BW-limit -> setting the Limit to FULL instead.")
            tempstr = "FULL"
        else:
            print("Please choose a valid BW-limit, the SDS800X HD offers either 0 for FULL or 20 for 20MHz.")
            return False
        
        self.sendCommand(f":CHAN{channel}:BWL {tempstr}")
        if check:
            return self.getBWLimit(channel, tempstr)
        return True
    
    def getBWLimit(self, channel: int, expLimit: str=None):
        if not self.checkChannel(channel):
            return False
        return self.queryCommand(f":CHAN{channel}:BWL?", expLimit)
    
    def setCoupling(self, channel: int, coupling: int, check: bool=False):      #Prog Manual P50
        if not self.checkChannel(channel):
            return False
        
        tempstr = ""
        if coupling == 1:
            tempstr = "DC"
        elif coupling == 2:
            tempstr = "AC"
        elif coupling == 3:
            tempstr = "GND"
        else:
            print("Please choose either 1 for DC-Coupling, 2 for AC-Coupling or 3 for Ground-Coupling.")
            return False
        
        self.sendCommand(f":CHAN{channel}:COUP {tempstr}")
        if check:
            return self.getCoupling(channel, tempstr)
        return True
    
    def getCoupling(self, channel: int, expCoupling: str=None):
        if not self.checkChannel(channel):
            return False
        return self.queryCommand(f":CHAN{channel}:COUP?", expCoupling)
    
    def setImpedance(self, channel: int, impedance: int=0, check: bool=False):  #Prog Manual P51
        return NotImplemented
    
    def getImpedance(self, channel: int, expImpedance: str=None):
        return NotImplemented
    
    def setInvert(self, channel: int, invert: bool=False, check: bool=False):   #Prog Manual P52
        return NotImplemented
    
    def getInvert(self, channel: int, expInvert: str=None):
        return NotImplemented
    
    def setLabelOnOff(self, channel: int, OnOff: bool, check: bool=False):      #Prog Manual P53
        return NotImplemented
    
    def getLabelOnOff(self, channel: int, exp: str=None):
        return NotImplemented
    
    def setLabelText(self, channel: int, text: str, check: bool=False):         #Prog Manual P54
        return NotImplemented
    
    def getLabelText(self, channel: int, expText: str=None):
        return NotImplemented
    
    def setOffset(self, channel: int, offset: float, check: bool=False):        #Prog Manual P55
        return NotImplemented
    
    def getOffset(self, channel: int, expOffset: float=None):
        return NotImplemented
    
    def setProbeAttenuation(self, channel: int, attenuation: float, check: bool=False):        #Prog Manual P56
        return NotImplemented
    
    def getProbeAttenuation(self, channel: int, expAttenuation: float=None):
        return NotImplemented
    
    def setScale(self, channel: int, attenuation: float, check: bool=False):        #Prog Manual P57
        return NotImplemented
    
    def getScale(self, channel: int, expScale: float=None):
        return NotImplemented
    
    def setSkew(self, channel: int, scale: float, check: bool=False):        #Prog Manual P58
        return NotImplemented
    
    def getSkew(self, channel: int, expScale: float=None):
        return NotImplemented
    
    def setChannelOnOff(self, channel: int, OnOff: bool, check: bool=False):        #Prog Manual P59
        return NotImplemented
    
    def getChannelOnOff(self, channel: int, expOnOff: str=None):
        return NotImplemented
    
    def setUnit(self, channel: int, unit: int, check: bool=False):        #Prog Manual P60
        return NotImplemented
    
    def getUnit(self, channel: int, expUnit: str=None):
        return NotImplemented
    
    def setVisible(self, channel: int, visible: bool, check: bool=False):        #Prog Manual P61
        return NotImplemented
    
    def getVisible(self, channel: int, expVisible: str=None):
        return NotImplemented
    
    # ------------------------- Counter Section of the Prog Manual P62-P73 skipped
    
    def setCursorOnOff(self, CursorOnOff: bool, check: bool=False):        #Prog Manual P75
        return NotImplemented
    
    def getCursorOnOff(self, expCursorOnOff: str=None):
        return NotImplemented
    
    def setCursorTagstyle(self, CursorTagstyle: int, check: bool=False):        #Prog Manual P76
        return NotImplemented
    
    def getCursorTagstyle(self, expCursorTagstyle: str=None):
        return NotImplemented
        
    def getCursorIXDelta(self, expIXDelta: str=None):             #Prog Manual P77
        return self.queryCommand(":CURS:IXD?", expIXDelta)
    
    def setCursorMItem(self, Mtype: int, source1: int, source2: int=None, check: bool=False):        #Prog Manual P78
        return NotImplemented
    
    def getCursorMItem(self, expMItem: str=None):
        return NotImplemented
    
    def setCursorMode(self, Mtype: int, MMode: int=None, check: bool=False):        #Prog Manual P79
        return NotImplemented
    
    def getCursorMode(self, expCursorMode: str=None):
        return NotImplemented
    
    def setCursorSource(self, source1o2: int, source: int, subsource: int, check: bool=False):        #Prog Manual P80-81
        return NotImplemented
    
    def getCursorSource(self, expCursorSource: str=None):
        return NotImplemented
    
    def setCursorXY1XY2(self, xy: int, cursor: int, value: float, check: bool=False):        #Prog Manual P82-83, 86-87
        return NotImplemented
    
    def getCursorXY1XY2(self, xy: int, cursor: int, expCurserValue: float=None):
        return NotImplemented
    
    def getCursorX1X2Delta(self, expCurserDelta: float=None):                        #Prog Manual P84
        return self.queryCommand(":CURS:XDEL?", expCurserDelta)
    
    def setCursorXYRef(self, xy: int, CType: int, check: bool=False):        #Prog Manual P85, 89
        return NotImplemented
    
    def getCursorXYRef(self, xy: int, expXRef: str=None):
        return NotImplemented
    
    def getCursorY1Y2Delta(self, expCurserDelta: float=None):                        #Prog Manual P88
        return self.queryCommand(":CURS:XDEL?", expCurserDelta)
    
    # ------------------------- Decode Section of the Prog Manual P90-P191 skipped
    
    # ------------------------- Digital Commands Section of the Prog Manual P192-P207 skipped
    
    def setAxisLabelsOnOff(self, OnOff: bool, check: bool=False):        #Prog Manual P209
        return NotImplemented
    
    def getAxisLabelsOnOff(self, expAxisLabelOnOff: str=None):
        return self.queryCommand(":DISP:AXIS?", expAxisLabelOnOff)
    
    def setAxisLabelMode(self, Mode: int, check: bool=False):        #Prog Manual P210
        return NotImplemented
    
    def getAxisLabelMode(self, expAxisMode: str=None):
        return self.queryCommand(":DISP:AXIS:MODE?", expAxisMode)
    
    def setDisplayBacklight(self, brightness: int, check: bool=False):        #Prog Manual P211
        return NotImplemented
    
    def getDisplayBacklight(self, expDisplayBrightness: str=None):
        return self.queryCommand(":DISP:BACK?", expDisplayBrightness)
    
    def clearWaveforms(self):                                               #Prog Manual P212
        self.sendCommand(":DISP:CLE")
        return True
    
    def setDisplayColorOnOff(self, ColorOnOff: bool, check: bool=False):
        return NotImplemented
    
    def getDisplayColorOnOff(self, expDisplayColorOnOff: str=None):
        return self.queryCommand(":DISP:COL?", expDisplayColorOnOff)
    
    def setDisplayGraticule(self, graticule: int, check: bool=False):       #Prog Manual P213
        return NotImplemented
    
    def getDisplayGraticule(self, expDisplayCraticule: int=None):
        return self.queryCommand(":DISP:GRAT?", expDisplayCraticule)
    
    def setDisplayGridstyle(self, gridstyle: int, check: bool=False):       #Prog Manual P214
        return NotImplemented
    
    def getDisplayGridstyle(self, expGridstyle: str=None):
        return self.queryCommand(":DISP:GRID?", expGridstyle)
    
    def setDisplayIntensity(self, intensity: int, check: bool=False):       #Prog Manual P215
        return NotImplemented
    
    def getDisplayIntensity(self, expIntensity: int=None):
        return self.queryCommand(":DISP:INT?", expIntensity)
    
    def setMenuStyle(self, style: int, check: bool=False):       #Prog Manual P216
        return NotImplemented
    
    def getMenuStyle(self, expMenuStyle: int=None):
        return self.queryCommand(":DISP:MENU?", expMenuStyle)
    
    def setMenuHidetime(self, hidetime: int, check: bool=False):       #Prog Manual P217
        return NotImplemented
    
    def getMenuHidetime(self, expHidetime: str=None):
        return self.queryCommand(":DISP:MENU:HIDE?", expHidetime)
    
    def setDisplayPersistence(self, persistence: int, check: bool=False):       #Prog Manual P218
        return NotImplemented
    
    def getDisplayPersistence(self, expPersistence: int=None):
        return self.queryCommand(":DISP:PERS?", expPersistence)
    
    def setDisplayTransparency(self, transparency: int, check: bool=False):       #Prog Manual P219
        return NotImplemented
    
    def getDisplayTransparency(self, expTransparency: int=None):
        return self.queryCommand(":DISP:TRAN?", expTransparency)
    
    def setDisplayType(self, DisplayType: int, check: bool=False):       #Prog Manual P220
        return NotImplemented
    
    def getDisplayType(self, expDisplayType: str=None):
        return self.queryCommand(":DISP:TYPE?", expDisplayType)
    
    # ------------------------- DVM Section of the Prog Manual P221-P228 skipped
    
    def setFFTDisplay(self, DisplayType: int, check: bool=False):       #Prog Manual P231
        return NotImplemented
    
    def getFFTDisplay(self, expDisplayType: str=None):
        return self.queryCommand(":FUNC:FFTD?", expDisplayType)
    
    def setGatethreshold(self, valueA: float, valueB: float, check: bool=False):       #Prog Manual P232
        return NotImplemented
    
    def getGatethreshold(self, expValueA: float=None, expValueB: float=None):
        return NotImplemented 
    
testdevice = Siglent_SDS800X_HD('TCPIP0::192.168.0.194::inst0::INSTR')
if testdevice is not None and testdevice.connect() is True: 
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

# --------------------------------------- pyTest Start --------------------------------------- #

def test_checkChannel():
    tempdevice = Siglent_SDS800X_HD("demo")
    assert tempdevice.checkChannel(1) is True
    assert tempdevice.checkChannel(2) is True
    assert tempdevice.checkChannel(3) is True
    assert tempdevice.checkChannel(4) is True
    assert tempdevice.checkChannel(0) is False
    assert tempdevice.checkChannel(5) is False

# ---------------------------------------- pyTest End ---------------------------------------- #