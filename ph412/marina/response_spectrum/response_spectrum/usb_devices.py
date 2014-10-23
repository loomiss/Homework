# Module to sort all current USB devices by vendor

from pyvisa import visa as v
import string as s

def FindUSBDevices() :
    vendors = {'Tektronix' : '0x0699', 'Rigol' : '0x1AB1'}
    devices = {'0x0699' : {'0x0366' : 'TDS1012B', '0x0346' : 'AFG3021B', '0x0368' : 'TDS2014B', '0x0367' : 'TDS2012B'}, '0x1AB1' : {'0x0588' : 'DG1022'}}
    a = v.get_instruments_list()
    # Sort the devices by vendor
    vendor_devices = {}
    for b in a :
        if b.find('USB') > -1 :
            bb = s.split(b, '::')
            for key in vendors :
                if vendors[key] == bb[1] :
                    if len(bb) > 3 :
                        sn = ' SN: ' + bb[3]
                        #print sn, key, vendors[key]
                        vendor_devices[devices[vendors[key]][bb[2]] + '-' + bb[3]] = v.instrument(b)
                    else :
                        vendor_devices[devices[vendors[key]][bb[2]]] = v.instrument(b)
    return vendor_devices   # This is a dictionary with device-sn keys.

def Test():
    devices = FindUSBDevices()
    #print device information by looking for the device-sn as a key in the dictionary devices
    if 'TDS1012B-C055976' in devices :
        print 'TDS1012B-C055976 = ', devices['TDS1012B-C055976']
    if 'AFG3021B-C031180' in devices :
        print 'AFG3021B-C031180 = ', devices['AFG3021B-C031180']

#-------------------------------------------------------------------------------

if __name__ == '__main__' :
    Test()

