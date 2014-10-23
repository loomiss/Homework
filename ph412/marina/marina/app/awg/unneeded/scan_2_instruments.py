
from tek import *


def FindDevices(fg_sn, scope_sn) :
    # Function generator first
    sn = s.strip(fg_sn)
    #sn = 'C031180'
    devices = FindUSBDevices()
    print 'Look for AFG3021B:'
    fg = AFG3021B(devices, sn)
    if fg.visa == '' :
        print "Error: AFG3021B-" + sn + " not found."
        return
    fg.Write('*IDN?')
    print "Function generator identification: ", fg.Read()
    fg.ClearQueue()
    # Now the scope
    sn = s.strip(scope_sn)
    #sn = 'C055976'
    print 'Look for TDS1012B:'
    scope = TDS1012B(devices, sn)
    if scope.visa == '' :
        print "Error: TDS1012B-" + sn + " not found."
        return
    scope.Write('*IDN?')
    print "Scope identification: ", scope.Read()
    scope.ClearQueue()
    return fg, scope

def FindTekInstrument(inst_list) :
    # inst_list is of the form [instrument name, serial number string]
    inst = s.strip(inst_list[0]).upper()
    sn = s.strip(inst_list[1]).upper()
    devices = FindUSBDevices()
    error = ''
    if inst == 'AFG3021B' :
        #sn = 'C031180'
        #print 'Look for AFG3021B:'
        dev = AFG3021B(devices, sn)
        if dev.visa == '' :
            error += "Error: AFG3021B-" + sn + " not found.\n"
        else :
            dev.Write('*IDN?')
            try:
                response = dev.Read()
                print "Function generator identification: ", response
                dev.ClearQueue()
            except :
                error += 'Function generator has been found, but it is not responsive.\n'
    elif inst == 'TDS1012B' :
        # Now the scope
        #sn = 'C055976'
        #print 'Look for TDS1012B:'
        dev = TDS1012B(devices, sn)
        if dev.visa == '' :
            error += "Error: TDS1012B-" + sn + " not found.\n"
        else :
            dev.Write('*IDN?')
            try:
                response = dev.Read()
                print "Scope identification: ", response
                dev.ClearQueue()
            except :
                error += 'Scope has been found, but it is not responsive.\n'
    else :
        error += inst + ' is not supported.\n'
        dev = ''
    if error :
        error += 'Available USB devices: \n'
        for key in devices :
            error += key + '   ' + str(devices[key]) + '\n'
    return dev, error



def InitializeDevices(fg_sn, scope_sn) :
    # Function generator first
    sn = s.strip(fg_sn)
    #sn = 'C031180'
    devices = FindUSBDevices()
    print 'Look for AFG3021B:'
    fg = AFG3021B(devices, sn)
    if fg.visa == '' :
        print "Error: AFG3021B-" + sn + " not found."
        return
    fg.Write('*IDN?')
    print "Function generator identification: ", fg.Read()
    fg.ClearQueue()
    command = '*rst'
    fg.Write(command)
    time.sleep(3.0)
    command = 'function sin;frequency 1.0e3'
    fg.Write(command)
    time.sleep(1.0)
    command = 'voltage:amplitude 1.0;voltage:offset 0;phase:adjust 0' # amplitude, not pk-pk
    fg.Write(command)
    time.sleep(1.0)
    command = ':output:impedance maximum;:output:state on'
    fg.Write(command)
    time.sleep(2.0)
    # Now the scope
    sn = s.strip(scope_sn)
    #sn = 'C055976'
    print 'Look for TDS1012B:'
    scope = TDS1012B(devices, sn)
    if scope.visa == '' :
        print "Error: TDS1012B-" + sn + " not found."
        return
    scope.Write('*IDN?')
    print "Scope identification: ", scope.Read()
    scope.ClearQueue()
    scope.Write('factory')
    time.sleep(2.0) # Sleeping only 1 second leads to a timeout error below.
    command = 'ch1:probe 1e0;scale 0.5;position 2.0'  # Factory default yunit is V, xunit is s
    scope.Write(command)
    command = 'ch2:probe 1e0;scale 0.5;position -2.0'  # Factory default yunit is V, xunit is s
    scope.Write(command)
    command = 'select:ch1 1;ch2 1'
    scope.Write(command)
    command = 'horiz:scale 1e-04;position 0'    # Trigger point is centered on the screen. -1e-04 moves it right 1 division.
    scope.Write(command)
    command = 'acquire:mode sample'     # Continuous display of input signals
    scope.Write(command)

    return fg, scope

