# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 17:23:33 2025

@author: Martin
"""

import math
from dataclasses import dataclass

@dataclass
class measunit:
    unit: str
    impedance: int
    
    def __init__(self, unit: str, impedance: int=1000000):
        allowedUnits = ["w", "dbm", "v", "dbuv", "a", "dbua"]
        if unit in allowedUnits:
            self.unit = unit
            self.impedance = impedance
            return True
        return None

@dataclass
class RFmeas:
    value: float
    unit: measunit
    
    # def conv2w(self):
    #     origunit = self.unit.lower()
    #     if origunit is "w":
    #         return True
    #     if origunit is "dbm":

def convertdBm2W(dBm: float, baseLog: int=10, baseLin: int=0.001):
    return baseLin * pow(10, (dBm/baseLog))

def convertW2dBm(W: float, baseLog: int=10, baseLin: int=0.001):
    if W > 0:
        return baseLog * math.log(W / baseLin, 10)
    return None

def convertdBuV2V(dBuV: float, baseLog: int=20, baseLin: int=0.000001):
    return baseLin * pow(10, (dBuV/baseLog))

def convertV2dBuV(V: float, baseLog: int=20, baseLin: int=0.000001):
    if V > 0:
        return baseLog * math.log(V / baseLin, 10)
    return None

def convertdBuA2A(dBuA: float, baseLog: int=20, baseLin: int=0.000001):
    return baseLin * pow(10, (dBuA/baseLog))

def convertA2dBuA(A: float, baseLog: int=20, baseLin: int=0.000001):
    if A > 0:
        return baseLog * math.log(A / baseLin, 10)
    return None

def getFactorFromUnit(unit: str):
    if unit.lower() == "s":
        return 1
    return False

def createFreqListLin(startf: int=10, stopf: int=100, stepf: int=10):
    if startf < 0 or stopf < 0 or stepf < 0:
        print("ERROR: all inputvalues for creating a frequencylist must be positive!")
        return []
    
    tempfreqs = [startf, stopf]
    tempfreq = startf + stepf
    while tempfreq < stopf:
        tempfreqs.append(tempfreq)
        tempfreq = int(tempfreq + stepf)
            
    print(f"\t{tempfreqs} values with lin-steps were created.")
    return tempfreqs

def createFreqListLog(startf: int=10, stopf: int=100, stepperc: int=10):
    if startf < 0 or stopf < 0 or stepperc < 0:
        print("ERROR: all inputvalues for creating a frequencylist must be positive!")
        return []
    
    tempfreqs = [startf, stopf]
    tempfreq = startf * (100 + stepperc) / 100
    while tempfreq < stopf:
        tempfreqs.append(tempfreq)
        tempfreq = int(tempfreq * ((100 + stepperc) / 100))
            
    print(f"\t{tempfreqs} values with log-steps were created.")
    return tempfreqs

def removeDuplicatesFreqList(origList: [], tolerance: int=1):
    origList.sort()
    
    lastvalue = origList[0]
    templist = [lastvalue]
    for tempvalue in origList:
        if (lastvalue + tolerance) < tempvalue:
            templist.append(tempvalue)
            lastvalue = tempvalue
    
    return templist