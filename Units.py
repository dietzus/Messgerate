# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 17:26:08 2025

@author: Martin
"""

from dataclasses import dataclass

units = []

@dataclass
class Timebase:
    name: str
    factor: float

@dataclass
class Measunits:
    name: str
    log: bool
    