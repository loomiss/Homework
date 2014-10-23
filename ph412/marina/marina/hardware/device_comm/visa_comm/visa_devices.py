"""
@author: Brad Hermens
"""
import pyvisa
from pyvisa import visa as v

class CommFailure(Exception):
    def __init__(self, *args):
        super(CommFailure, self).__init__(*args)

class VisaDevice(v.Instrument):
    def __init__(self, devIdn, delay = 0.1):
        """ 
        @param devIdn: A string identifying a visa device. Typically returned 
        from calling visa.get_instrument_list
        @type devIdn: string
        
        """
        super(VisaDevice, self).__init__(devIdn)
        
        devInf = devIdn.split("::")
        self.PORT = devInf[0]
        self.PID = devInf[1]
        self.VID = devInf[2]
        self.SERIAL_NUM = devInf[3]
        self.delay = delay
        try:
            devInf = self.ask("*idn?")            
            
        except pyvisa.visa_exceptions.VisaIOError:
           raise CommFailure("Failed to communicate with device {}. Try raising the delay time.".format(devIdn))
        
        finally:
            devInf = devInf.split(',')
        
            self.MAKE = devInf[0].strip()
            self.MODEL = devInf[1].strip()
        
            del(devInf)
        
    
def GetDevices():
    """
    Gets a list of VisaDevice objects generated for each connected device.
    
    @return: List of supported devices currently available.
    """
    
    devs = v.get_instruments_list()
    valid_devs = [] #List to hold devices to return
    
    for device in devs:
        if device.find("::") is not -1:
            valid_devs.append(VisaDevice(device))
            
    return valid_devs
    
def GetDeviceNames():
    """
    Gets a dictionary of devices keyed by device name.
    
    @return: Dictionary of supported devices currently available.
    """
    devsDict = {}
    devs = GetDevices()
    
    for device in devs:
        devsDict[device.MODEL] = device
        
    return devsDict
    
    
    
if __name__ == "__main__":
    print GetDeviceNames().keys()

    