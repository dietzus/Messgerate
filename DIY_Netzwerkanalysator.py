# -*- coding: utf-8 -*-
"""
Created on Fri Apr 11 17:40:45 2025

@author: Martin
"""

import sys, time
import Utility, FY6900
from dataclasses import dataclass

@dataclass
class measResult:
    freq: int
    ampl0: float = 0
    ampl1: float = 0
    ampl2: float = 0
    phase: float = 0
    diffDB: float = 0
    
    def calcDiffdB(ampl1: float, ampl2: float, impedance: float=1000000):
        return 0

if False:
    inputLin = 10
    inputLog = 40
    print(str(inputLin) + "Watt\tare\t" + str(Utility.convertW2dBm(inputLin)) + "dBm.")
    print(str(inputLog) + "dBm\tare\t" + str(Utility.convertdBm2W(inputLog)) + "W.")
    print()
    inputLin = 1
    inputLog = 120
    print(str(inputLin) + "V\t\tare\t" + str(Utility.convertV2dBuV(inputLin)) + "dBuV.")
    print(str(inputLog) + "dBuV\tare\t" + str(Utility.convertdBuV2V(inputLog)) + "V.")
    print()
    print(str(inputLin) + "A\t\tare\t" + str(Utility.convertA2dBuA(inputLin)) + "dBuA.")
    print(str(inputLog) + "dBuA\tare\t" + str(Utility.convertdBuA2A(inputLog)) + "A.")
        
    sys.exit()

#----------------------------------------- SigGen-Code Beginn --------------------
siggen = None
SiggenVolt = 1.0

def initSigGen():
    global siggen
    siggen = FY6900.FY6900("COM3")
    if siggen.connect(True):
        siggen.setVolt(SiggenVolt)
        return True
    return False

#----------------------------------------- SigGen-Code End --------------------

#----------------------------------------- Osci-Code Beginn --------------------

def initOsci():
    return False



#----------------------------------------- Osci-Code End --------------------

if initSigGen():
    print("Siggen was initialized succesfully.")
else:
    print("There was a problem while initializing the siggen, program aborted.")
    sys.exit()
    
if initOsci():
    print("Osci was initialized succesfully.")
else:
    print("There was a problem while initializing the osci, program aborted.")

freqlist = []

freqlist.extend(Utility.createFreqListLin())
freqlist.extend(Utility.createFreqListLog())

freqlist = Utility.removeDuplicatesFreqList(freqlist, 2)
print(freqlist)

siggen.setOutput(1, True)
time.sleep(1)

measpoints = []

for tempfreq in freqlist:
    tempampl1 = 0
    tempampl2 = 0
    tempphase = 0
    siggen.setFreq(1, tempfreq)
    tempmeas = measResult(tempfreq, SiggenVolt)
    time.sleep(0.5)
    
    measpoints.append(tempmeas)

time.sleep(1)
siggen.setOutput(1, False)

siggen.disconnect()

