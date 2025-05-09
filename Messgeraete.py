# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 06:41:26 2025

@author: Martin
"""

import time, serial
import pyvisa as visa
    
class connection:
    hasSerial: bool
    serialPort: str
    baud: int
    stopbits = None
    hasVISA: bool
    VISAaddress: str
    isConnected: bool=False
    prefix: str
    postfix: str
    default_sleep: float
    timeout: float
    connObj = None
    
    def __init__(self, useVISA: bool, addr: str, baud: int=115200, stopbits = serial.STOPBITS_ONE, prefix: str="", postfix: str="", defaultSleep: float=0.2, timeout: float=1):
        if useVISA:
            self.hasSerial = False
            self.hasVISA = True
            self.VISAaddress = addr
        else:
            self.hasSerial = True
            self.hasVISA = False
            self.serialPort = addr
        self.baud = baud
        self.stopbits = stopbits
        self.isConnected = False
        self.prefix = prefix
        self.postfix = postfix
        self.default_sleep = defaultSleep
        self.timeout = timeout
        self.connObj = None
    
    def checkAvailable(self):
        devlist = visa.ResourceManager().list_resources()
        if self.hasSerial:
            #if self.serialPort in devlist:
            #    return True
            #print(self.serialPort + " was not found, available devices: " + str(devlist))
            return True #TODO: needs to be fixed and properly checked!
        elif self.hasVISA:
            if self.VISAaddress in devlist:
                return True
            print(self.VISAaddress + " was not found, available devices: " + str(devlist))
        return devlist
    
    def connect(self):
        if self.isConnected is True:
            return True
        if self.checkAvailable() is True:
            if self.hasSerial:
                try:
                    self.connObj = serial.Serial(port=self.serialPort, baudrate=self.baud, stopbits=self.stopbits)
                    if self.connObj.isOpen():
                        self.isConnected = True
                        return True
                except:
                    print("There was a problem when trying to connect to " + self.serialPort)
                    self.isConnected = False
            if self.hasVISA:
                try:
                    self.connObj = visa.ResourceManager().open_resource(self.VISAaddress)
                    self.isConnected = True
                    return True
                except:
                    print("There was a problem when trying to connect to " + self.VISAaddress)
                    self.isConnected = False
        print("The device could not be connected.")
        return False
    
    def reconnect(self):
        self.disconnect()
        return self.connect()
    
    def disconnect(self):
        if self.isConnected is False:
            return True
        if self.hasSerial:
            try:
                self.connObj.close()
                self.isConnected = False
            except:
                return False
        if self.hasVISA:
            try:
                self.connObj.close()
                self.isConnected = False
            except:
                return False
        return True
    
    def padCommand(self, cmd: str):
        tempcmd = self.prefix + cmd.strip() + self.postfix
        return tempcmd
    
    def sendCommand(self, cmd: str):
        if self.connObj is None:
            print("There was an error while trying to send the command '" + cmd + "'.")
            return False
        
        tempcmd = self.padCommand(cmd)
        print("DEBUG: sending the command: '" + str(tempcmd).strip() + "'.")
        if self.hasVISA:
            self.connObj.write(tempcmd)
        else:
            self.connObj.write(tempcmd.encode())
        time.sleep(self.default_sleep)
        return True
    
    def queryCommand(self, cmd: str, expAnsw: str=None):
        if self.connObj is None:
            print("There was an error while trying to query the command '" + cmd + "'.")
            return False
        
        tempcmd = self.padCommand(cmd)
        print("DEBUG: querying the command: '" + str(tempcmd).strip() + "'.")
        tempanswer: str=None
        if self.hasVISA:
            tempanswer = self.connObj.query(tempcmd).strip()
            time.sleep(self.default_sleep)
        else:
            self.connObj.write(tempcmd)
            tempanswer = self.connObj.readline().strip()
            time.sleep(self.default_sleep)
        if expAnsw is not None:
            if tempanswer.lower() == expAnsw.lower():
                return True
            else:
                print("Expected answer: '" + expAnsw + "' actual answer: '" + tempanswer + "'.")
                return False
        return tempanswer
    
class measdevice():
    name: str
    conn: connection
    
    def __init__(self, name: str, useVISA: bool, addr: str):
        self.name = name
        self.conn = connection(useVISA, addr)
    
    def setName(self, name: str):
        tempname = self.name
        self.name = name
        return tempname
        
    def getName(self):
        return self.name
    
    def connect(self):
        return self.conn.connect()
    
    def reconnect(self):
        return self.conn.reconnect()
    
    def disconnect(self):
        return self.conn.disconnect()
    
    def sendCommand(self, cmd: str):
        return self.conn.sendCommand(cmd)
    
    def queryCommand(self, cmd: str, expAnsw: str=None):
        return self.conn.queryCommand(cmd, expAnsw)