# -*- coding: utf-8 -*-
"""
Created on Sat Nov 02 11:21:40 2013

@author: Brad Hermens

This module is for communication with Tektronix scopes.
"""
SUPPORTED_DEVICES = ['TDS 2014B', 'TDS 1012B', 'TDS 2012B']

from .. import visa_devices as vd

def FindSupportedDevices():
    """
    Uses VISA to look for scopes attached to the system. 
    
    @return: A list of VisaDevice objects that are supported by this module.
    """
    scopes = []
    devices = vd.GetDevices()
    for device in devices:
        if device.MODEL in SUPPORTED_DEVICES:
            scopes.append(device)
    
    return scopes
    
class Oscilloscope(vd.VisaDevice):
    def __init__(self, vd):
        super(Oscilloscope, self).__init__(vd.resource_name)
        del(vd)
    
    def Identity(self):
        """
        Grabs the Identity string form the specified scope.
        
        @return: Device identitiy string.
        """
        return self.ask("*IDN?")
        
    def HeaderOn(self, yn):
        """
        Turns the return header from the scope on or off.
        
        @param yn: True for headers on, false for no headers.
        @type yn: Boolean
        """
        if yn:
            self.write("header on")
        else:
            self.write("header off")
            
    def ClearQueue(self):
        """
        Clears the scope buffer.
        
        @return: Bytes cleared from buffer?
        """
        return self.ask("*esr?")
        
    def Lock(self, yn): 
        """
        Lock the scope from local input.
                
        @param yn: True for lock, false for unlocked.
        @type yn: Boolean    
        """        
        if yn:
            self.write("lock all")
        else:
            self.write("unlock all")
            
    def SetDataChannel(self, channel):
        """
        Set the channel from which data will be returned if asked.
        
        @param channel: The scope channel number.
        @type channel: int
        """
        self.write("data:source ch{}".format(channel))
        
    def ChannelOn(self, channel, yn):
        """
        Turns the selected channel on or off.
        
        @param channel: The channel you want to turn on or off.
        @type channel: int
        
        @param yn: True for channel on, false for channel off.
        @type yn: Boolean
        """
        
        if yn:
            self.write("select:ch{} 1".format(channel))
        else:
            self.write("select:ch{} 0".format(channel))
            
    def ProbeVoltage(self, channel, multiplier):
        """
        Sets the probe voltage multiplyer for the specified channel.
        
        @param channel: The channel on which you would like to change the voltage
        multiplier.
        @type channel: int
        
        @param multiplier: The value to multiply the voltage by. Valid values are:
        1, 10, 20, 50, 100, 500, 1000
        @param multiplier: int
        """
        self.write("ch{}:probe {}".format(channel, multiplier))
        
    def Coupling(self, channel, type):
        """
        Sets the coupling state for the specified channel.
        
        @param channel: The channle on which you would like to set the coupling.
        @type channel: int
        
        @param type: The coupling type. Valid values are: ac, dc
        @type type: string
        """
        self.write("ch{}:coupling {}".format(channel, type))
        
    def BandwidthLimiting(self, channel, yn): 
        """
        Turns bandwith limiting on or off for the selected scope.
        
        @param channel: The channel number to set limiting.
        @type channel: int
        
        @param yn: True for limiting on, false for off.
        @type yn: Boolean
        """
        if yn:
            self.write("ch{}:bandwidth on".format(channel))
        else:
            self.write("ch{}:bandwidth off".format(channel))
            
    def VoltageScale(self, channel, scale):
        """
        Sets the voltage scale on the specified channel.
        
        @param channel: The channel on which to change the voltage scale.
        @type channe: int
        
        @param scale: The voltage range per division.
        @type scale: float
        """
        self.write("ch{}:scale {}".format(channel, scale)) 
        
    def VerticalPosition(self, channel, pos):
        """
        Sets the vertical center position of the specified channel.
        
        @param channel: The channel on which to change the vertical position.
        @type channe: int
        
        @param pos: The center position in grid units.
        @type pos: float
        """
        self.write("ch{}:position {}".format(channel, pos))
        
    def TimeScale(self, scale):
        """
        Sets the time scale on the specified scope.
        
        @param scale: The number of seconds per division.
        @type scale: float
        """
        self.write("horizontal:scale {}".format(scale))
        
    def TriggerMode(self, mode):
        """
        Sets the trigger mode for the specified scope.
        
        @param mode: The trigger mode. Either auto or normal
        @type mode: string
        """
        self.write("trigger:main:mode {}".format(mode))
        
        
    def TriggerType(self, type):
        
        """
        Sets the type of signal the specified scope will trigger on.
        
        @param type: The type of input to be used as a trigger. Valid values
        are: edge, video, or pulse
        @type type: string
        """
        self.write("trigger:mode:type {}".format(type))
        
    def TriggerSource(self, source): 
        """
        Sets the source of the trigger signal.
        
        @param source: the Source of the trigger. Valid values are: ch1, 
        ch2, ch3, ch4, ext
        @type source: string
        """
        self.write("trigger:main:edge:source {}".format(source))
        
    def TriggerSlope(self, slope):
        """
        Sets the edge trigger to either rising or falling.
        
        @param slope: The slope type to trigger on. Valid values: rise, fall
        @type slope: string
        """
        
        self.write("trigger:main:edge:slope {}".format(slope))
        
    def  TriggerLevel(self, level):
        """
        Sets the voltage level of the trigger.
        
        @param level: The trigger level in volts.
        @type level: float
        """
        self.write("trigger:main:level {}".format(level))
        
    def TriggerPosition(self, pos):
        """
        Sets the trigger point on the time scale. 
        
        @param pos: Number of seconds before or after the center time point.
        @type pos: float
        """
        self.write("horizontal:position {}".format(pos))
        
    def AcquireMode(self, mode):
        """
        Sets the acquisition mode of the scope.
        
        @param mode: The scope aquisition mode. Valid values: average, 
        sample, peakdetect
        @type mode: string
        """
        self.write("acquire:mode {}".format(mode)) 
        
    def AcquireSweeps(self, sweeps):
        """
        The number of sweeps to average when displaying data.
        
        @param sweeps: The number of sweeps to take.
        @type sweeps: int
        """
        self.write("acquire:numavg {}".format(sweeps))
        
    def AcquireStateOn(self, yn):
        """
        Turns data acquisition on or off on the selected scope.
        
        @param yn: True for data acquisition on, false for off.
        @type yn: Boolean
        """
        if yn:
            self.write("acquire:state on")
        else:
            self.write("acquire:state off")
            
    def DataWidth(self, width):
        """
        Set the byte width of data acquired form the scope.
        
        @param width: The data width in bytes. Valid values: 1, 2
        @type width: int
        """
        self.write("data:width {}".format(width))
        
    def DataEncoding(self, encdg):
        """
        Sets the type of data that will be returned by the scope.
        
        @param encdg: The data type returned by the scope. Valid values: 
        ascii, ribinary, rpbinary, sribinary, srpbinary
        @type encdg: string
        """
        self.write("data:encdg {}".format(encdg))
        
    def GetUnit(self, axis):
        """
        Gets unit for the given axis
        
        @param axis: The axis you of which you would like the units. Valid values:
        x,y
        @type axis: string
        
        @return: String stating the specified axis units.
        """
        return str(self.ask("wfmpre:{}unit?".format(axis)))
        
    def GetXIncrement(self):
        """
        Gets the increment value between data points.
        
        @returns: Increment value between data points.
        """
        return float(self.ask("wfmpre:xincr?"))
        
    def GetYMultiplier(self):
        """
        Gets the multiplyer to convert digitized Y units to volts.
        
        @return: The multiplier as a float
        """
        return float(self.ask("wfmpre:ymult?"))
        
    def GetYOffset(self):
        """
        Gets the y offset value in digitized units.
        
        @return: Offset value as a float.
        """
        return float(self.ask("wfmpre:yoff?"))
        
    def GetYZero(self):
        """
        Gets the Yzero value. Used to convert digitized units to volts.
        
        @return: Yzero value as a float.
        
        """
        return float(self.ask("wfmpre:yzero?"))    
        
    def SetDataStart(self, location):
        """
        Sets the start location for reading data off the oscilloscope.
        
        @param location: The starting data point position.
        @type location: int
        """
        self.write("data:start {}".format(location))
        
    def SetDataStop(self, location):
        """
        Sets the stop location for reading data from the oscilloscope.
        
        @param location: The data point to stop at.
        @type location: int
        """
        self.write("data:stop {}".format(location))
        
    def GetData(self):
        """
        Returns the data from the scope. The channel from which data is returned is 
        set with SetDataChannel.
        
        @return: A string containing scope data for the specified channel.
        """
        return self.ask("curve?")
    
    
    
if __name__ == "__main__":
    print(FindSupportedDevices()) 
