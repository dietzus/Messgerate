# -*- coding: utf-8 -*-
"""
Created on Sat May 10 11:03:46 2025

@author: Martin
"""

import time
import Messgeraete

class Owon_DGE1060(Messgeraete.measdevice):
    name: str
    conn: Messgeraete.connection
    IDN: str=""
    NrChannels: int
    maxFreq: int
    
    def __init__(self, addr: str, name: str="SDS800X_HD", NrChannels: int=1, maxFreq: int=60000000):
        self.name = name
        self.conn = Messgeraete.connection(useVISA=True, addr=addr)
        if NrChannels == 1 or NrChannels == 2:
            self.NrChannels = NrChannels
        else:
            return None
        if maxFreq > 70000000:
            return None
        elif maxFreq > 60000000:
            self.maxFreq = 70000000
        elif maxFreq > 35000000:
            self.maxFreq = 60000000
        else:
            self.maxFreq = 35000000  
    
    def getIDN(self):
        return self.conn.queryCommand("*IDN?")
    
    def reset(self):
        #return NotImplemented #The device also resets the USB mode -> after a reset there is usb connection via VISA possible anymore
        self.setAmplitude(1)
        self.setChannelOnOff(False)
        self.setOffset(0)
        self.setModOnOff(False)
        self.setFrequency(1)
        
        time.sleep(1)
        return True
    
    def setImpedance(self, impedance: int, channel: int=1, check: bool=False):          #Prog Manual P10
        if not self.checkChannel(channel) or impedance < 1:
            return False
        
        tempstr = ""
        if impedance == 1:
            tempstr = "MIN"
        elif impedance == 10000:
            tempstr = "MAX"
        elif impedance > 10000:
            tempstr = "INF"
            impedance = 9.9E+37
        else:
            tempstr = str(impedance) + "OHMS"
        self.sendCommand(f"OUTP{channel}:IMP {tempstr}")
        if check:
            return self.getImpedance(channel, str(impedance))
        return True
        
    def getImpedance(self, channel: int=1, expImpedance: str=None):
        if not self.checkChannel(channel):
            return False
        return self.queryCommand(f"OUTP{channel}:IMP?", expImpedance)
        
    
    def setChannelOnOff(self, onOff: bool, channel: int=1, check: bool=False):
        if not self.checkChannel(channel):
            return False
        
        tempstr = ""
        if onOff:
            tempstr = "1"
        else:
            tempstr = "0"
        self.sendCommand(f"OUTP{channel}:STAT {tempstr}")
        if check:
            return self.getChannelOnOff(channel, tempstr)
        return True
        
    def getChannelOnOff(self, channel: int=1, expStateOnOff: str=None):
        if not self.checkChannel(channel):
            return False
        return self.queryCommand(f"OUTP{channel}:STAT?", expStateOnOff)
    
    def setFrequency(self, freq: float, unit: str="Hz", channel: int=1, check: bool=False):
        if not self.checkChannel(channel) or freq <= 0:
            return False
        
        unitlower = unit.lower()
        tempfreq = 0
        if unitlower == "hz":
            tempfreq = freq
        elif unitlower == "khz":
            tempfreq = freq * 1000
        elif unitlower == "mhz":
            tempfreq = freq * 1000000
        else:
            return False
        
        if tempfreq > self.maxFreq:
            return False
        
        self.sendCommand(f"SOUR{channel}:FREQ:FIX {tempfreq}Hz")
        if check:
            return self.getFrequency(channel, tempfreq)
        return True
    
    def getFrequency(self, channel: int=1, expFreq: int=None):                  #Prog Manual P24
        if not self.checkChannel(channel):
            return False
        tempanswer = self.queryCommand(f"SOUR{channel}:FREQ:FIX?")
        try:
            tempfreq = float(tempanswer)
        except:
            print("The answer could not be parsed to a valid frequency.")
            return 0
        if expFreq is not None:
            return expFreq == tempfreq
        return tempfreq
    
    def getMinFrequency(self, channel: int=1, expFreq: str=None):
        if not self.checkChannel(channel):
            return False
        return self.queryCommand(f"SOUR{channel}:FREQ:FIX? MIN", expFreq)
    
    def getMaxFrequency(self, channel: int=1, expFreq: str=None):
        if not self.checkChannel(channel):
            return False
        return self.queryCommand(f"SOUR{channel}:FREQ:FIX? MAX", expFreq)
    
    def setModOnOff(self, onOff: bool, channel: int=1, check: bool=False):      #Prog Manual P32
        if not self.checkChannel(channel):
            return False
        
        tempstr = ""
        if onOff:
            tempstr = "1"
        else:
            tempstr = "0"
        self.sendCommand(f"SOUR{channel}:MOD:STAT {tempstr}")
        if check:
            return self.getModOnOff(channel, tempstr)
        return True
        
    def getModOnOff(self, channel: int=1, expStateOnOff: str=None):
        if not self.checkChannel(channel):
            return False
        return self.queryCommand(f"SOUR{channel}:MOD:STAT?", expStateOnOff)
    
    def setAmplitude(self, amplitude: float, unit: str="V", channel: int=1, check: bool=False): #Prog Manual P46-47
        if not self.checkChannel(channel):
            return False
        
        unitlower = unit.lower()
        tempampl = 0.0
        if unitlower == "v":
            tempampl = amplitude * 1000
        elif unitlower == "mv":
            tempampl = amplitude
        else:
            return False
        
        self.sendCommand(f"SOUR{channel}:VOLT:LEV:IMM:AMPL {tempampl}mVpp")
        if check:
            return self.getAmplitude(channel, tempampl)
        return True
        
    def getAmplitude(self, channel: int=1, expVolt: int=None):
        if not self.checkChannel(channel):
            return False
        tempanswer = self.queryCommand(f"SOUR{channel}:VOLT:LEV:IMM:AMPL?")
        try:
            tempampl = float(tempanswer)
        except:
            print("The answer could not be parsed to a valid frequency.")
            return 0
        if expVolt is not None:
            return expVolt == tempampl
        return tempampl
    
    def setOffset(self, offset: float, unit: str="V", channel: int=1, check: bool=False):   #Prog Manual P46
        if not self.checkChannel(channel):
            return False
        
        unitlower = unit.lower()
        tempoffs = 0.0
        if unitlower == "v":
            tempoffs = offset * 1000
        elif unitlower == "mv":
            tempoffs = offset
        else:
            return False
        
        self.sendCommand(f"SOUR{channel}:VOLT:LEV:IMM:OFFS {tempoffs}mV")
        if check:
            return self.getAmplitude(channel, tempoffs)
        return True
        
    def getOffset(self, channel: int=1, expOffs: int=None):
        if not self.checkChannel(channel):
            return False
        tempanswer = self.queryCommand(f"SOUR{channel}:VOLT:LEV:IMM:OFFS?")
        try:
            tempoffs = float(tempanswer)
        except:
            print("The answer could not be parsed to a valid frequency.")
            return 0
        if expOffs is not None:
            return expOffs == tempoffs
        return tempoffs
    
    def getErrorMessages(self):                                                             #Prog Manual P48
        temperrors = self.queryCommand("SYST:ERR:NEXT?")
        temperror = self.queryCommand("SYST:ERR:NEXT?")
        counter = 0
        while not temperror.startswith("0") and counter < 10:
            temperrors += "\n" + temperror
            temperror = self.queryCommand("SYST:ERR:NEXT?")
            counter += 1
        return temperrors
    
testdevice = Owon_DGE1060('USB0::0x5345::0x1235::24500387::INSTR')
if testdevice is not None and testdevice.connect() is True: 
    print(testdevice.getIDN())
    testdevice.reset()
    print("Min Freq: " + testdevice.getMinFrequency())
    print("Max Freq: " + testdevice.getMaxFrequency())
    if False:
        time.sleep(2)
        print(testdevice.setImpedance(1, 1, True))
        time.sleep(1)
        print(testdevice.setImpedance(50, 1, True))
        time.sleep(1)
        print(testdevice.setImpedance(10000, 1, True))
        time.sleep(1)
        print(testdevice.setImpedance(10001, 1, True))
        time.sleep(1)
        print(testdevice.setChannelOnOff(True, 1, True))
        time.sleep(1)
        print(testdevice.setChannelOnOff(False, 1, True))
        
        print(testdevice.setFrequency(1, "Hz"))
        print(testdevice.getFrequency())
        print(testdevice.setFrequency(0.000001, "Hz"))
        print(testdevice.getFrequency())
        print(testdevice.setFrequency(60000000, "Hz"))
        print(testdevice.getFrequency())
        print(testdevice.setFrequency(0.001, "Hz"))
        print(testdevice.getFrequency())
        print(testdevice.setFrequency(1, "kHz"))
        print(testdevice.getFrequency())
        print(testdevice.setFrequency(60, "MHz"))
        print(testdevice.getFrequency())
    
        print(testdevice.setAmplitude(0.001))
        print(testdevice.getAmplitude())
        print(testdevice.setOffset(15))
        print(testdevice.getOffset())
        print(testdevice.setAmplitude(1))
        print(testdevice.getAmplitude())
        print(testdevice.setOffset(5))
        print(testdevice.getOffset())
        print(testdevice.setAmplitude(20))
        print(testdevice.getAmplitude())
        print(testdevice.setAmplitude(100))
        print(testdevice.getAmplitude())
    
        print(testdevice.getErrorMessages())
    
    testdevice.reset()
    testdevice.disconnect()

# --------------------------------------- pyTest Start --------------------------------------- #