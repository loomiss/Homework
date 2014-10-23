
# This is a modification of the translation of the example program
# C:\Program Files\National Instruments\NI-DAQ\Examples\DAQmx ANSI C\Analog In\Measure Voltage\Acq-Int Clk\Acq-IntClk.c

# This can be imported as a module for a grander program.

# Modules have been "imported as" so that the functionality provided by each module can be clearly identified.

import numpy as np
#import pylab as plt
from matplotlib import pyplot as plt

import nidaqmx as mx    # Note that since ctypes was imported in nidaqmx.py as ct, anything from ctypes now is referenced as mx.ct
import nidaqmx_constants as c

class AnalogInDevice :
    def __init__(self, c, f, parms) :
        # dll is the handle to the dll.  device is the "Dev1", etc..
        # c is the object of constants, such as Val_RSE, and f is the object of functions, such as CreateTask.
        #self.dll = dll
        self.c = c
        self.f = f
        #print dll.DAQmx_Val_RSE
        # Define constants corresponding to values in  C:\Program Files\National Instruments\NI-DAQ\DAQmx ANSI C Dev\include\NIDAQmx.h
        # The following are control constants used by nidaqmx.
        #self.Cfg_Default = c.Val_Cfg_Default    #np.int32(-1)
        #self.Volts = c.Val_Volts    #10348
        #self.Rising = c.Val_Rising  #10280
        #self.FiniteSamps = c.Val_FiniteSamps    #10178
        #self.GroupByChannel = c.Val_GroupByChannel  #0
        #self.ChanForAllLines = c.Val_ChanForAllLines    #1
        #self.RSE = c.Val_RSE    #10083
        #self.ContSamps = c.Val_ContSamps    #10123
        #self.GroupByScanNumber = c.Val_GroupByScanNumber    #1

        # initialize variables
        self.data = np.zeros((parms.samples_raw,),dtype=np.float64)

    def PotentialChannel(self, task_handle, parms) :
        # Establish the potential channel
        self.f.CreateAIVoltageChan(task_handle, parms.channel,"",
                                   self.c.Val_RSE, parms.vmin, parms.vmax, self.c.Val_Volts, None) # or RSE (single-ended) instead of Cfg_Default?

    def ConfigureTiming(self, task_handle, parms) :
        self.f.CfgSampClkTiming(task_handle, parms.clock_source, parms.sample_rate,
                                       self.c.Val_Rising, self.c.Val_FiniteSamps, parms.samples)    # or ContSamps instead of FiniteSamps?

    def TakeData(self, task_handle, parms) :
        types=mx.Types()
        read = types.read
        self.f.ReadAnalogF64(task_handle, parms.samples_raw, parms.buffer_size,
                             self.c.Val_GroupByChannel, self.data.ctypes.data,
                             parms.samples_raw, mx.ct.byref(read),None)
        self.points = read.value
        return  #read

class ADCParameters :
    def __init__(self, device, types, vmin, vmax, timeout, buffer_size, sample_rate, samples, channel, clock):
        # Use: ADCParameters(t, -10.0, 10.0, 10, 10000.0, 2000, 'Dev1/ai0', 'OnboardClock')
        self.vmin = types.float64(vmin)     #-10.0)
        self.vmax = types.float64(vmax)     # 10.0
        self.timeout = types.float64(timeout)     #10.0
        self.buffer_size = types.float64(buffer_size)      #10
        self.pointsToRead = buffer_size
        #self.pointsRead = types.uInt32()
        self.sample_rate = types.float64(sample_rate)     #10000.0)
        self.samples = types.uInt64(samples)      #2000)
        self.samples_raw=samples
        channel_string = device+'/ai' + str(channel)
        self.channel = mx.ct.create_string_buffer(channel_string)     #'Dev1/ai0')
        self.clock_source = mx.ct.create_string_buffer(clock)       #'OnboardClock')

def Synchronous() :
    dll, message = mx.LoadDLL()
    if dll == 0 :
        print 'Library not loadable.  ' + message
        sys.exit()
    c = mx.TranslateDAQmxConstants()
    f = mx.TranslateDAQmxFunctions(dll)
    device = mx.FindDevices(f)
    t = mx.Types()
    task = mx.CreateTask(f, t, 0)    # Create task 0
    sample_rate = 60000.0
    sample_period = 1.0/sample_rate
    samples = 100000
    adc_range = 10.0
    ain_channel = 0
    #for sample_rate in range(30000, 75000, 1000) :
    for k in range(20) :
        p = ADCParameters(device, t, -adc_range, adc_range, 10, 100, sample_rate, samples, ain_channel, 'OnboardClock')    # types, min, max, timeout, buffer_size, sample_rate, samples, channel, clock
        a = AnalogInDevice(c, f, p)     # Initialize the analog input device
        a.PotentialChannel(task, p)     # Open an analog input channel for the task
        a.ConfigureTiming(task, p)    # Configure the timing for taking data points on this channel for this task.
        mx.StartTask(f, task)                     # Begin the task
        sig = 0
        for j in range(10) :
            a.TakeData(task, p)   # Take some data
            # Synchronous detection - assume sampling at exactly twice the expected frequency of a weak signal in noise.
            #new_data = np.array([])
            tot = 0
            for i in range(0, len(a.data), 1) :
                #new_data = np.append(new_data, a.data[i] - a.data[i+1])
                tot += a.data[i] * (-1)**i
            #print 'total = ', tot
            sig += tot
        print 'sample_rate, signal = ', sample_rate, sig
        mx.EndTask(f, task)
    mx.ClearTask(f, task)
    return

def Correlation() :
    dll, message = mx.LoadDLL()
    if dll == 0 :
        print 'Library not loadable.  ' + message
        sys.exit()
    c = mx.TranslateDAQmxConstants()
    f = mx.TranslateDAQmxFunctions(dll)
    device = mx.FindDevices(f)
    t = mx.Types()
    task = mx.CreateTask(f, t, 0)    # Create task 0
    sample_rate = 240000.0
    sample_period = 1.0/sample_rate
    samples = 10000
    applied_freq = 30000
    adc_range = 2.0
    ain_channel = 0
    p = ADCParameters(device, t, -adc_range, adc_range, 10, 100, sample_rate, samples, ain_channel, 'OnboardClock')    # types, min, max, timeout, buffer_size, sample_rate, samples, channel, clock
    a = AnalogInDevice(c, f, p)     # Initialize the analog input device
    a.PotentialChannel(task, p)     # Open an analog input channel for the task
    a.ConfigureTiming(task, p)    # Configure the timing for taking data points on this channel for this task.
    mx.StartTask(f, task)                     # Begin the task
    a.TakeData(task, p)   # Take some data
    print "Acquired %d points"%(a.points)
    print a.points/sample_rate, sample_period
    x = np.arange(0, a.points/sample_rate, sample_period)
    data_array = np.array([x, a.data])
    #data_arrays = [[x, a.data]]
    corr = np.correlate(data_array[1], data_array[1], mode='full')
    #data_arrays.append([x, corr[len(corr)/2 :]])
    #print corr
    # time domain graph
    f3 = plt.figure()
    sb3 = f3.add_subplot(111)
    sb3.plot(data_array[0], data_array[1])
    sb3.set_xlabel('Time in Seconds')
    sb3.set_ylabel('Amplitude in Volts')
    sb3.set_title('Time Domain Signal: '+str(applied_freq/1000)+' kHz, '+str(int(sample_rate)/1000)+' kSPS, '+str(samples/1000)+' kSamples')
    sb3.grid(True)
    # Correlation in time
    f4 = plt.figure()
    sb4 = f4.add_subplot(111)
    sb4.plot(data_array[0], corr[len(corr)/2 :])
    sb4.set_ylim(ymin=-20.0, ymax =20.0)
    sb4.set_xlabel('Time in Seconds')
    sb4.set_ylabel('Amplitude in Volts')
    sb4.set_title('Auto-Correlation : '+str(applied_freq/1000)+' kHz, '+str(int(sample_rate)/1000)+' kSPS, '+str(samples/1000)+' kSamples')
    sb4.grid(True)
    plt.show()
    mx.EndTask(f, task)
    mx.ClearTask(f, task)
    q = raw_input('Enter a file name to save this data or just press enter to exit :').strip()
    if q :
        np.savetxt(q, data_array.transpose(), fmt='%-.5e', delimiter=',')  # left justified, exponential format, 5 digits after point
    return

def Simple(caller, device, f, ain_channel, sample_rate, samples, adc_range, applied_freq) :
    # caller is an object.
    dll, message = mx.LoadDLL()
    if dll == 0 :
        print 'Library not loadable.  ' + message
        sys.exit()
    c = mx.TranslateDAQmxConstants()
    #f = mx.TranslateDAQmxFunctions(dll)
    #device = mx.FindDevices(f)
    t = mx.Types()
    task = mx.CreateTask(f, t, 0)    # Create task 0
    #sample_rate = 200000.0
    sample_period = 1.0/sample_rate
    #samples = 10000
    #applied_freq = 30000
    #adc_range = 2.0
    #ain_channel = 0
    p = ADCParameters(device, t, -adc_range, adc_range, 10, 100, sample_rate, samples, ain_channel, 'OnboardClock')    # types, min, max, timeout, buffer_size, sample_rate, samples, channel, clock
    print 'ADC min, max: ', p.vmin.value, p.vmax.value
    a = AnalogInDevice(c, f, p)     # Initialize the analog input device
    a.PotentialChannel(task, p)     # Open an analog input channel for the task
    a.ConfigureTiming(task, p)    # Configure the timing for taking data points on this channel for this task.
    mx.StartTask(f, task)                     # Begin the task
    a.TakeData(task, p)   # Take some data
    mx.EndTask(f, task)
    mx.ClearTask(f, task)
    print "Acquired %d points"%(a.points)
    print a.points/sample_rate, sample_period
    x = np.arange(0, a.points/sample_rate, sample_period)
    data_arrays = [[x, a.data]]
    # Time domain plot
    frame_title = 'Analog Input'
    xlabels = ['Time in Seconds']
    ylabels = ['Amplitude in Volts']
    titles = ['Time Domain Signal: '+str(applied_freq/1000)+' kHz, '+str(int(sample_rate)/1000)+' kSPS, '+str(samples/1000)+' kSamples']
    grids = [True]
    tab_names = ['Channel '+str(ain_channel)+' vs Time']
    #GraphSimple(a, sample_rate, sample_period, applied_freq, samples)
    #NotebookPlot(caller, [data_array], frame_title, titles, xlabels, ylabels, grids, tab_names)
    # Frequency domain
    fty = np.fft.fft(a.data)
    halfway = samples/2
    ftyabs = np.abs(fty[0:halfway])
    n = fty.size
    ftx = np.fft.fftfreq(n, sample_period)[0:halfway]/1.0e03    # in kHz
    data_arrays.append([ftx, 20.0*np.log10(ftyabs)])
    # Frequency domain plot
    xlabels.append('Frequency in kHz')
    ylabels.append(r'20 Log $V(\nu)$')
    titles.append('Power Spectrum: '+str(applied_freq/1000)+' kHz, '+str(int(sample_rate)/1000)+' kSPS, '+str(samples/1000)+' kSamples')
    grids.append(True)
    tab_names.append('Channel '+str(ain_channel)+' Power Spectrum')
    NotebookPlot(caller, data_arrays, frame_title, titles, xlabels, ylabels, grids, tab_names)
    return data_arrays, {'titles':titles, 'xlabels':xlabels, 'ylabels':ylabels, 'tab_names':tab_names}

def NotebookPlot(caller, data_arrays, frame_title, titles, xlabels, ylabels, grids, tab_names) :
    b = caller.dock.system_modules['notebook_plots_base']
    g = caller.dock.system_modules['notebook_plots_graph']
    pf = b.PlotFrame(title=frame_title, size=(800,700))
    for i in range(len(data_arrays)) :
        print len(data_arrays[i][0]), len(data_arrays[i][1])
        p = g.Graph('plot', [data_arrays[i]], symbols=['b','g'], grid=grids[i], title = titles[i], titlesize=18,\
            background='w', xlabel=xlabels[i], ylabel=ylabels[i], labelsize=16, ticklabelsize=12, customize=None)
        g.DefineTab(pf, [p], name=tab_names[i])
    pf.Show()

def GraphSimple(a, sample_rate, sample_period, applied_freq, samples) :
    x = np.arange(0, a.points/sample_rate, sample_period)
    data_array = np.array([x, a.data])
    #plot(x, a.data)
    # time domain graph
    f4 = plt.figure()
    sb4 = f4.add_subplot(111)
    sb4.plot(data_array[0], data_array[1])
    sb4.set_xlabel('Time in Seconds')
    sb4.set_ylabel('Amplitude in Volts')
    sb4.set_title('Time Domain Signal: '+str(applied_freq/1000)+' kHz, '+str(int(sample_rate)/1000)+' kSPS, '+str(samples/1000)+' kSamples')
    sb4.grid(True)
    # Frequency domain
    fty = np.fft.fft(data_array[1])
    halfway = samples/2
    ftyabs = np.abs(fty[0:halfway])
    n = fty.size
    ftx = np.fft.fftfreq(n, sample_period)[0:halfway]/1.0e03    # in kHz
    f1 = plt.figure()
    sb1 = f1.add_subplot(111)
    sb1.plot(ftx, 20.0*np.log10(ftyabs))
    sb1.grid(True)
    # filter the fft
    #ftyabs_filtered = ftyabs /np.sqrt(1.0 + (2.0*np.pi*ftx*1.0e03*1.0e-04)**2)
    # add it to the plot
    #sb1.plot(ftx, 20.0*np.log10(ftyabs_filtered))
    sb1.set_xlabel('Frequency in kHz')
    sb1.set_ylabel(r'20 Log $V(\nu)$')
    sb1.set_title('Power Spectrum: '+str(applied_freq/1000)+' kHz, '+str(int(sample_rate)/1000)+' kSPS, '+str(samples/1000)+' kSamples')
    #sb1.set_title('Power spectrum: 10 kHz with 50% Modulation at 9 kHz')
    #sb1.text(4.0,85,'Rate = '+str(sample_rate)+'\nSamples = '+str(samples))
    #sb1.legend(['no filter', 'with filter'], 'best')
    plt.show()
    plt.close()
    #q = raw_input('Enter a file name to save this data or just press enter to exit :').strip()
    #if q :
        #np.savetxt(q, data_array.transpose(), fmt='%-.5e', delimiter=',')  # left justified, exponential format, 5 digits after point

#----------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__' :
    print 'This is not the module you want.'
    #Simple()
    #Synchronous()
    #Correlation()
