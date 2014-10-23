# -*- coding: utf-8 -*-
"""
Created on Fri Nov 08 11:34:33 2013

This is used to create a package for handling visa devices.

@author: Brad Hermens
"""

__all__ = ['visa_devices']

import scope_comm
import awg_comm
from importlib import import_module as im

SCOPES = {}
"""A dictionary of all supported scopes connected to the system"""
AWGS = {}
"""A dictionary of all supported AWGs connected to the system"""

def GetConnectedScopes():
    scpDrvrs = scope_comm.__all__
    drivers = []
    
    for item in scpDrvrs:
        drivers.append(im(scope_comm.__name__ + "." + item))
        
    for driver in drivers:
        devs = driver.FindSupportedDevices()
        if len(devs) > 0:
            for item in devs:
                SCOPES[item.MODEL] = driver.Oscilloscope(item)
    return SCOPES
                
def GetConnectedAWGs():
    scpDrvrs = awg_comm.__all__
    drivers = []
    
    for item in scpDrvrs:
        drivers.append(im(awg_comm.__name__ + "." + item))
        
    for driver in drivers:
        devs = driver.FindSupportedDevices()
        if len(devs) > 0:
            for item in devs:
                AWGS[item.MODEL] = driver.AWG(item)
    return AWGS
    
