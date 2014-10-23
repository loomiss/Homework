# -*- coding: utf-8 -*-
"""
Created on Sat Nov 09 15:57:15 2013

@author: Brad Hermens
"""

SUPPORTED_DEVICES =['DG1022']

from .. import visa_devices as vd


def FindSupportedDevices():
    """
    Uses VISA to look for AWGs attached to the system. 
    
    @return: A list of VisaDevice objects that are supported by this module.
    """
    awgs = []
    devices = vd.GetDevices()
    for device in devices:
        if device.MODEL in SUPPORTED_DEVICES:
            awgs.append(device)
    
    return awgs
    
class AWG(vd.VisaDevice):
    def __init__(self, vd):
        super(AWG, self).__init__(vd.resource_name)
        
    def Identity(self):
        """
        Grabs the Identity string form the specified AWG.
        
        @return: AWG identity string.
        """
        return self.ask("*IDN?")
        
    def ClearQueue(self):
        """
        Clears the AWG buffer.
        
        @return: Bytes cleared from buffer?
        """
        return self.ask("syst:err?")
        
    def Lock(self, yn): 
        """
        Lock the AWG from local input.
        
        @param yn: True for lock, false for unlocked.
        @type yn: Boolean    
        """
        
        if yn:
            self.write("syst:rwl")
        else:
            self.write("syst:loc")
            
    def SetFunctionType(self, channel, type):
        """
        Sets the waveform type.
        
        @param channel: Channel to set waveform type on.
        @type channel: int
        
        @param type: The waveform type. Valid values: sin, square, ramp
        @type type: string
        """
        if channel is 1:
            self.write("function {}".format(type))
        else:
            self.write("func:ch{} {}".format(channel, type))
        
    def SetFrequency(self, channel, frequency):
        """
        Sets the waveform generator frequency.
        
        @param channel: The channel to switch the frequency on.
        @type channel: int
        
        @param frequency: The frequency of the wave output.
        @type frequency: float
        """
        if channel is 1:
            self.write("frequency {}".format(frequency))
        else:
            self.write("frequency:ch{} {}".format(channel, frequency))
        
    def SetVoltage(self, channel, volts):
        """
        Sets the peak to peak voltage.
        
        @param channel: The channel to set voltage on;
        @type channel: int
        
        @param volts: The voltage
        @type volts: float
        """
        if channel is 1:
            self.write("voltage {}".format(volts)) 
        else:
            self.write("voltage:ch{} {}".format(channel, volts))
        
    def SetVoltUnit(self, channel, unit): # Unknown if working???
        """
        Sets the voltage unit accepted by awg.
        
        @param channel: The channel to set the units on.
        @type channel: int
        
        @param unit: The unit of voltage accepted. Valid values: VPP, VRMS, DBM
        @type unit: string
        """
        if channel is 1:
            self.write("voltage:unit {}".format(unit)) 
        else:
            self.write("voltage:unit:ch{} {}".format(channel, unit)) 
    
    def SetOffset(self, channel, volts):
        """
        Sets the DC offset of the wave.
        
        @param channel: The channel to set the offset on.
        @type channel: int
        
        @param unit: The offset voltage.
        @type unit: string
        """
        if channel is 1:
            self.write("voltage:offset {}".format(volts))
        else:
            self.write("voltage:offset:ch{} {}".format(channel, volts))
        
    def SetPhase(self, channel, phase):
        """
        Sets the phase of the output wave.
        
        @param channel: The channel to set the phase on.
        @type channel: int
        
        @param phase: Phase shift in radians
        @type phase: float
        """
        if channel is 1:
            self.write("phase {}".format(phase))
        else:
            self.write("phase:ch{} {}".format(channel, phase))
        
    def SetImpedence(self, channel, imp):
        """
        Sets the load impedence for the device on the specified channel.
        
        @param channel: The channel to set the Impedance of.
        @type channel: int
        
        @param imp: The impedence value. Valid values: a number in ohms, MIN, MAX, INF
        @type imp: int, string
        """
        if channel is 1:
            self.write("output:load {}".format(imp))
        else:
            self.write("output:load:ch{} {}".format(channel, imp))
        
    def SetChannelStateOn(self, channel, yn):
        """
        Turns a channel on or off
        
        @param channel: The channel to set the state of.
        @type channel: int
        
        @param yn: True for On, false for off.
        @type yn: Boolean
        """
        if channel is 1:
            if yn:
                self.write("output on")
            else:
                self.write("output off")
        else:
            if yn:
                self.write("output:ch{} on".format(channel))
            else:
                self.write("output:ch{} off".format(channel))
                
    def SetTriggerOn(self, yn):
        """
        Turn the trigger on or off.
        
        @param yn: True for on, false for off.
        @Type yn: Boolean
        """
        if yn:
            self.wirte("output:sync on")
        else:
            self.write("output:sync off")
            
    def GetFunction(self, channel):
        """
        Retrieve the function type.
        
        @param channel: the channel to retrieve the function type from.
        @type channel: int
        
        @return: A string containing the function type.
        """
        if channel is 1:
           return self.ask("function?")
        else:
           return self.ask("function:ch{}?")
        
    def GetFrequency(self, channel):
        """
        Retrieve the channel frequncy.
        
        @param channel: the channel to retrieve the frequency from.
        @type channel: int
        
        @return: A float of the frequency.
        """
        if channel is 1:
            return float(self.ask("frequency?"))
        else:
            return float(self.ask("frequency:ch{}?".format(channel)).strip("CH{}:".format(channel)))
        
    def GetAmplitude(self, channel):
        """
        Retrieve the peak to peak voltage of waveform.
        
        @param channel: the channel to retrieve the amplitude.
        @type channel: int
        
        @return: A float of the peak to peak amplitude.
        """
        if channel is 1:
            return float(self.ask("voltage?"))
        else:
            return float(self.ask("voltage:ch{}?".format(channel)).strip("CH{}: ".format(channel)))
        
    def GetOffset(self, channel):
        """
        Retrieve the channel offset.
        
        @param channel: the channel to retrieve the offset from.
        @type channel: int
        
        @return: A float of the offset voltage.
        """
        if channel is 1:
            return float(self.ask("voltage:offset?"))
        else:
            return float(self.ask("voltage:offset:ch{}?".format(channel)))
        
    def GetPhase(self, channel):
        """
        Retrieve the phase of the waveform.
        
        @param channel: the channel to retrieve the phase from.
        @type channel: int
        
        @return: A float of the phase in radians.
        """
        if channel is 1:
            return float(self.ask("phase?"))
        else:
            return float(self.ask("phase:ch2?"))
        
    def GetImpedance(self, channel):
        """
        Retrieve the impedance of the channel.
        
        @param channel: the channel to retrieve the impedance from.
        @type channel: int
        
        @return: A float of the impedance.
        """
        if channel is 1:
            return self.ask("output:load?")
        else:
            return self.ask("output:load:ch{}?".format(channel))
