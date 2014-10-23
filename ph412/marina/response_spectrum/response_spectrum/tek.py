
# Module of functions to access the TDS 1012B using visa32.dll and PyVisa

from usb_devices import *
from pylab import *
from numpy import *
import time
import string as s

class TDS1012BChannelParameters :
    def __init__(self, channel) :
        # Specify channel at 1 or 2
        self.channel = channel
        self.xunit = 0
        self.xinc = 0
        self.yunit = 0
        self.ymult = 0
        self.yoff = 0
        self.yzero = 0

class TDS1012B :
    def __init__(self, devices, sn) :
        # Devices is the dictionary of usb devices
        for key in devices :
            if key[0:3] == 'TDS' :
                self.visa = devices[key]
        #if devices.has_key('TDS1012B' + '-' + sn.upper()) :
            #self.visa = devices['TDS1012B' + '-' + sn.upper()]
        #elif devices.has_key('TDS1012B') :
            #self.visa = devices['TDS1012B']     # No serial number was found.
        #else :
            #self.visa = ''      # Device not found
        self.identity = 'TDS1012B'
        self.sn = sn.upper()
        self.ch1 = TDS1012BChannelParameters(1)
        self.ch2 = TDS1012BChannelParameters(2)
        self.error = ''
        self.time = 0   # Used to report time taken for read and write functions

    def Write(self, stuff) :
        zero = time.time()
        try:
            self.visa.write(stuff)
        except:
            self.error = self.identity + ' write operation probably timed out.'
        self.time = time.time() - zero

    def Read(self) :
        zero = time.time()
        try:
            q = self.visa.read()
        except:
            self.error = self.identity + ' read operation probably timed out.'
            q = self.error
        self.time = time.time() - zero
        return q

    def ClearQueue(self) :
        self.Write('*esr?')
        return self.Read()

    def SetChannel(self, c) :
        error = ''
        if c > 2 | c <1 :
            error = "Incorrect channel request."
        self.Write('data:source ch'+str(c))
        return error

    def GetScaleParameters(self, ch):
        # ch = channel object
        error = ''
        if ch.channel > 2 | ch.channel <1 :
            error = "Incorrect channel request."
            return error
        self.visa.write('data:source ch'+str(ch.channel))
        try :
            self.visa.write('wfmpre:xunit?')
            ch.xunit = s.split(self.visa.read(), 'XUNIT')[1].strip().strip('"')
        except :
            error = 'Parameter read error.  Is channel ' + str(ch.channel) + ' currently displayed?'
            return error
        print ch.xunit
        self.visa.write('wfmpre:xincr?')
        ch.xinc = float(s.split(self.visa.read(), 'XINCR')[1])
        print ch.xinc
        self.visa.write('wfmpre:yunit?')
        ch.yunit = s.split(self.visa.read(), 'YUNIT')[1].strip().strip('"')
        self.visa.write('wfmpre:ymult?')
        ch.ymult = float(float(s.split(self.visa.read(), 'YMULT')[1]))
        self.visa.write('wfmpre:yoff?')
        ch.yoff = float(float(s.split(self.visa.read(), 'YOFF')[1]))
        self.visa.write('wfmpre:yzero?')
        ch.yzero = float(float(s.split(self.visa.read(), 'YZERO')[1]))
        # Make a dictionary of values
        ch.parameters = {}
        ch.parameters['xunit'] = ch.xunit
        ch.parameters['xinc'] = ch.xinc
        ch.parameters['yunit'] = ch.yunit
        ch.parameters['ymult'] = ch.ymult
        ch.parameters['yoff'] = ch.yoff
        ch.parameters['yzero'] = ch.yzero
        return error

    def GetWaveform(self, ch, mode) :
        # Mode is ascii or bin.
        # ch = channel object
        error = ''
        if ch.channel > 2 | ch.channel <1 :
            error = "Incorrect channel request."
            return error, []
        self.visa.write('data:source ch'+str(ch.channel))
        if s.lower(mode).find('asc') > -1 :
            self.visa.write('data:encdg ascii')
        else :
            error = 'Only ascii mode is supported.'
            return error, []
        self.visa.write('curve?')
        w = self.visa.read().split('CURVE')[1].split(',')
        x, y = self.ScaleWaveform(w, ch)
        return error, x, y

    def ScaleWaveform(self, w, ch) :
        y = []
        x = []
        delx = 0
        #yoff = p['yoff']
        for z in w:
            y.append((float(z)-ch.yoff)*ch.ymult + ch.yzero)
            x.append(delx)
            delx += ch.xinc
        return x, y

class DG1022 :
    def __init__ (self, devices, sn) :
        # Devices is the dictionary of usb devices
        for key in devices :
            if key[0:2] == 'DG' :
                self.visa = devices[key]
        #if devices.has_key('AFG3021B' + '-' + sn.upper()) :
            #self.visa = devices['AFG3021B' + '-' + sn.upper()]
        #elif devices.has_key('AFG3021B') :
            #self.visa = devices['AFG3021B']     # No serial number found for device
        #else :
            #self.visa = ''      # Device not found
        self.identity = 'DG1022'
        self.sn = sn.upper()
        self.error = ''
        self.time = 0   # Used to report time taken for read and write functions

    def Write(self, stuff) :
        zero = time.time()
        try:
            self.visa.write(stuff)
        except:
            self.error = self.identity + ' write operation probably timed out.'
        self.time = time.time() - zero

    def Read(self) :
        zero = time.time()
        try:
            q = self.visa.read()
        except:
            self.error = self.identity + ' read operation probably timed out.'
            q = self.error
        self.time = time.time() - zero
        return q

    def ClearQueue(self) :
        self.visa.write('*esr?')
        return self.visa.read()

class AFG3021B :
    def __init__ (self, devices, sn) :
        # Devices is the dictionary of usb devices
        for key in devices :
            if key[0:3] == 'AFG' :
                self.visa = devices[key]
        #if devices.has_key('AFG3021B' + '-' + sn.upper()) :
            #self.visa = devices['AFG3021B' + '-' + sn.upper()]
        #elif devices.has_key('AFG3021B') :
            #self.visa = devices['AFG3021B']     # No serial number found for device
        #else :
            #self.visa = ''      # Device not found
        self.identity = 'AFG3021B'
        self.sn = sn.upper()
        self.error = ''
        self.time = 0   # Used to report time taken for read and write functions

    def Write(self, stuff) :
        zero = time.time()
        try:
            self.visa.write(stuff)
        except:
            self.error = self.identity + ' write operation probably timed out.'
        self.time = time.time() - zero

    def Read(self) :
        zero = time.time()
        try:
            q = self.visa.read()
        except:
            self.error = self.identity + ' read operation probably timed out.'
            q = self.error
        self.time = time.time() - zero
        return q

    def ClearQueue(self) :
        self.visa.write('*esr?')
        return self.visa.read()

def FindScopeTDS1012b() :
    # Tek vendor id = 0x0699, TDS1012B id = 0x0366, SN = C055976
    a = get_instruments_list()
    for b in a :
        if b.find('USB') > -1 :
            bb = split(b, '::')
            if strip(bb[1]) == '0x0699' and strip(bb[2]) == '0x0366' :
                print "TDS1012b found."
                if len(bb) > 3 :
                    print "Serial number = ", bb[3]
            h = instrument(b)
    return h    # Return the handle

def FindVisaInstruments() :
    Vendors = {'Tektronix' : '0x0699'}
    a = get_instruments_list()
    return a    # Return list

def ClearQueue(h) :
    h.write('*esr?')
    return h.read()

def SetChannel(h, c) :
    h.write('data:source ch'+str(c))

class ScalingParameters :
    def __init__(self, h, c):
        # c = channel, a number
        # h = the scope
        # assume x increment is in seconds
        h.write('wfmpre:xunit?')
        self.xunit = h.read()
        h.write('wfmpre:xincr?')
        self.xinc = float(h.read())
        h.write('wfmpre:yunit?')
        self.yunit = h.read()
        h.write('wfmpre:ymult?')
        self.ymult = float(h.read())
        h.write('wfmpre:yoff?')
        self.yoff = float(h.read())
        h.write('wfmpre:yzero?')
        self.yzero = float(h.read())


def GetWaveform(h, mode) :
    # mode is ascii or bin
    error = ''
    if lower(mode).find('asc') > -1 :
        h.write('data:encdg ascii')
    else :
        error = 'Only ascii mode is supported.'
        return error, []
    h.write('curve?')
    return error, h.read().split(',')

def TDS1012BDialog(sn) :
    sn = s.strip(sn)
    #sn = 'C055976'
    devices = FindUSBDevices()
    print 'Look for TDS1012B:'
    scope = TDS1012B(devices, sn)
    if scope.visa == '' :
        print "Error: TDS1012B-" + sn + " not found."
        return
    scope.Write('*IDN?')
    print "Scope identification: ", scope.Read()
    scope.ClearQueue()
    a = '1'
    while a :
        a = raw_input('Enter command or query to send or r to read: ')
        a = s.strip(a)
        if a.lower() == 'r' :
            print scope.Read()
        else :
            print scope.Write(a)
    return

def AFG3021BDialog(sn) :
    sn = s.strip(sn)
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
    a = '1'
    while a :
        a = raw_input('Enter command or query to send or r to read: ')
        a = s.strip(a)
        if a.lower() == 'r' :
            print fg.Read()
        else :
            print fg.Write(a)
    return

def AFG3021BTest(sn):
    sn = s.strip(sn)
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

def AFG3021BScan(sn) :
    sn = s.strip(sn)
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
    # Frequencies in Hz
    freq_base = array(range(1, 10, 1), dtype=float)
    log_range = [3, 4]
    for p in log_range :
        freqs = freq_base * power(10.0, p)
        print freqs
        for f in freqs :
            fg.Write('frequency ' + str(f))
            time.sleep(1.0)
    a = '1'
    while a :
        a = raw_input('Enter command or query to send or r to read: ')
        a = s.strip(a)
        if a.lower() == 'r' :
            print fg.Read()
        else :
            print fg.Write(a)
    return

def SaveResults(x, ys, channels=None) :
    # y is an array of y values
    # channels is an array of channels
    outfile = raw_input('Enter a file name or nothing to skip: ')
    if s.strip(outfile) :
        o = open(outfile, 'w')
        if channels :
            o.write('# Channel information:\n')
            for ch in channels :
                o.write('#\t'+ch.xunit+', '+ch.yunit+'\n')
        o.write('\n# x value followed by y for each channel:\n')
        for i in range(len(x)) :
            dat = str(x[i])
            for y in ys:
                dat += ',' + str(y[i])
            dat += '\n'
            o.write(dat)
            #o.write(str(x[i]) + ',' + str(amplitude[i]) + ',' + str(phase[i]) + '\n')
        o.close()
    return

def TDS1012BTest(sn):
    sn = s.strip(sn)
    #sn = 'C055976'
    devices = FindUSBDevices()

    print 'Look for TDS1012B:'
    scope = TDS1012B(devices, sn)
    if scope.visa == '' :
        print "Error: TDS1012B-" + sn + " not found."
        return
    scope.Write('*IDN?')
    print "Scope identification: ", scope.Read()
    scope.ClearQueue()
    print 'Channel 1 parameters:'
    error = scope.GetScaleParameters(scope.ch1)
    if error :
        print error
        return
    print scope.ch1.parameters
    print 'Channel 2 parameters:'
    error = scope.GetScaleParameters(scope.ch2)
    if error :
        print error
        return
    print scope.ch2.parameters
    #return
    print 'Get channel 1 waveform:'
    error, w1x, w1y = scope.GetWaveform(scope.ch1, 'ascii')
    if error:
        print error
        return
    print 'Data array length = ', len(w1x), len(w1y)
    print 'Get channel 2 waveform:'
    error, w2x, w2y = scope.GetWaveform(scope.ch2, 'ascii')
    if error:
        print error
        return
    print 'Data array length = ', len(w2x), len(w2y)
    scope.ClearQueue()
    a = raw_input('Enter plot mode as yt (the default) or xy :')
    aa = a.strip().lower()
    graph_title = raw_input('Enter the title for the graph: ')
    if (aa == '') | (aa == 'yt') :
        x = w1x
        y1 = w1y
        y2 = w2y
        ys = [y1, y2]
        plot(x, y1, label='Channel 1')
        plot(x, y2, label='Channel 2')
        legend()
        title(graph_title)
        xlabel(scope.ch1.xunit)
        ylabel('Amplitude ('+scope.ch1.yunit+')')
        grid(True)
        show()
    elif aa == 'xy' :
        x = w1y
        y = w2y
        ys = [y]
        plot(x,y)
        title(graph_title)
        xlabel('Amplitude ('+scope.ch1.yunit+')')
        ylabel('Amplitude ('+scope.ch2.yunit+')')
        grid(True)
        show()
    show()
    #f = rfft(y)
    #plot(f)
    #show()
    SaveResults(x, ys, channels=[scope.ch1, scope.ch2])

#  Execute -------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    TDS1012BTest('C055976')
    #TDS1012BDialog('C055976')
    #AFG3021BTest('C031180')
    #AFG3021BDialog('C031180')
    #AFG3021BScan('C031180')
