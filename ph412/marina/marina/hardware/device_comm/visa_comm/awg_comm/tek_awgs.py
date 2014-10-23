# -*- coding: utf-8 -*-
"""
Created on Fri Nov 08 11:18:20 2013

@author: Brad Hermems
"""

SUPPORTED_DEVICES =['AFG3021B']

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
        
        @param awg: A visa device object identified as a AWG by FindSuppoetedDevices().
        @type awg: VisaDevice
        """
        return self.ask("*IDN?")
        
    def ClearQueue(self):
        """
        Clears the AWG buffer.
        
        @return: Bytes cleared from buffer?
        """
        return self.ask("*esr?")
        
    def Lock(self, yn): 
        """
        Lock the AWG from local input.
        
        @param yn: True for lock, false for unlocked.
        @type yn: Boolean    
        """
        
        if yn:
            self.write("system:klock:state on")
        else:
            self.write("system:klock:state off")
            
    def SetFunctionType(self, channel, type):
        """
        Sets the waveform type.
        
        @param channel: Channel to set waveform type on.
        @type channel: int
        
        @param type: The waveform type. Valid values: sin, square, ramp
        @type type: string
        """
        self.write("source{}:function {}".format(channel, type))
        
    def SetFrequency(self, channel, frequency):
        """
        Sets the waveform generator frequency.
        
        @param channel: The channel to switch the frequency on.
        @type channel: int
        
        @param frequency: The frequency of the wave output.
        @type frequency: float
        """
        self.write("source{}:frequency {}".format(channel, frequency))
        
    def SetVoltage(self, channel, volts):
        """
        Sets the peak to peak voltage.
        
        @param channel: The channel to set voltage on;
        @type channel: int
        
        @param volts: The voltage
        @type volts: float
        """
        self.write("source{}:voltage:amplitude {}".format(channel, volts)) # source channel might be needed
        
    def SetVoltUnit(self, channel, unit): # Unknown if working???
        """
        Sets the voltage unit accepted by awg.
        
        @param channel: The channel to set the units on.
        @type channel: int
        
        @param unit: The unit of voltage accepted. Valid values: VPP, VRMS, DBM
        @type unit: string
        """
        self.write("source{}:voltage:amplitude:unit {}".format(channel, unit)) # source channel might be needed
    
    def SetOffset(self, channel, volts):
        """
        Sets the DC offset of the wave.
        
        @param channel: The channel to set the offset on.
        @type channel: int
        
        @param unit: The offset voltage.
        @type unit: string
        """
        self.write("source{}:voltage:offset {}".format(channel, volts)) #source channel might be needed
        
    def SetPhase(self, channel, phase):
        """
        Sets the phase of the output wave.
        
        @param channel: The channel to set the phase on.
        @type channel: int
        
        @param phase: Phase shift in radians
        @type phase: float
        """
        self.write("source{}:phase:adjust {}".format(channel, phase))
        
    def SetImpedence(self, channel, imp):
        """
        Sets the load impedence for the device on the specified channel.
        
        @param channel: The channel to set the Impedance of.
        @type channel: int
        
        @param imp: The impedence value. Valid values: a number in ohms, MIN, MAX, INF
        @type imp: int, string
        """
        self.write("output{}:impedance {}".format(channel, imp))
        
    def SetChannelStateOn(self, channel, yn):
        """
        Turns a channel on or off
        
        @param channel: The channel to set the state of.
        @type channel: int
        
        @param yn: True for On, false for off.
        @type yn: Boolean
        """
        if yn:
            self.write("output{}:state on".format(channel))
        else:
            self.write("output{}:state off".format(channel))
            
    def GetFunction(self, channel):
        """
        Retrieve the function type.
        
        @param channel: the channel to retrieve the function type from.
        @type channel: int
        
        @return: A string containing the function type.
        """
        self.ask("source{}:function?".format(channel))
        
    def GetFrequency(self, channel):
        """
        Retrieve the channel frequncy.
        
        @param channel: the channel to retrieve the frequency from.
        @type channel: int
        
        @return: A float of the frequency.
        """
        return float(self.ask("source{}:frequency?".format(channel)))
        
    def GetAmplitude(self, channel):
        """
        Retrieve the peak to peak voltage of waveform.
        
        @param channel: the channel to retrieve the amplitude.
        @type channel: int
        
        @return: A float of the peak to peak amplitude.
        """
        return float(self.ask("source{}:voltage:amplitude?".format(channel)))
        
    def GetOffset(self, channel):
        """
        Retrieve the channel offset.
        
        @param channel: the channel to retrieve the offset from.
        @type channel: int
        
        @return: A float of the offset voltage.
        """
        return float(self.ask("source{}:voltage:offset?".format(channel)))
        
    def GetPhase(self, channel):
        """
        Retrieve the phase of the waveform.
        
        @param channel: the channel to retrieve the phase from.
        @type channel: int
        
        @return: A float of the phase in radians.
        """
        return float(self.ask("source{}:phase:adjust?".format(channel)))
        
    def GetImpedance(self, channel):
        """
        Retrieve the impedance of the channel.
        
        @param channel: the channel to retrieve the impedance from.
        @type channel: int
        
        @return: A float of the impedance.
        """
        return float(self.ask("output{}:impedance?".format(channel)))
