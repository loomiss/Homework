
import numpy

#from pylab import *
import matplotlib
try:
    # As a backend, wxAgg seems visually superior to wx.
    be = 'wxagg'
    if be == 'wxagg':
        matplotlib.use(be) # The recommended way to use wx is with the WXAgg backend.
        from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as Canvas
        from matplotlib.backends.backend_wxagg import NavigationToolbar2Wx as Toolbar
        #import matplotlib.backends.backend_wxagg.RendererAgg as renderer
        #renderer = Canvas
    elif be == 'gtkagg':
        matplotlib.use('gtkagg')    # Install pygtk to use this backend.
        from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as Canvas
        from matplotlib.backends.backend_gtkagg import NavigationToolbar2Wx as Toolbar
    elif be == 'wx':
        matplotlib.use('wx')    # Native wx backend.
        from matplotlib.backends.backend_wx import FigureCanvasWx as Canvas
        from matplotlib.backends.backend_wx import NavigationToolbar2Wx as Toolbar
    print('Using ' + be + '.')
except :
    print('Requested backend ' + be + ' not found.  Try another.')
    sys.exit(0)
from matplotlib import pyplot as plt
from nidaqmx import *
import ctypes

class AnalogInDevice :
    def __init__(self, dll, parms) :
        # dll is the handle to the dll.  device is the "Dev1", etc..
        self.dll = dll
        # Define constants corresponding to values in  C:\Program Files\National Instruments\NI-DAQ\DAQmx ANSI C Dev\include\NIDAQmx.h
        self.Cfg_Default = numpy.int32(-1)
        self.Volts = 10348
        self.Rising = 10280
        self.FiniteSamps = 10178
        self.GroupByChannel = 0
        self.ChanForAllLines = 1
        self.RSE = 10083
        self.ContSamps = 10123
        self.GroupByScanNumber = 1
        self.Seconds = ctypes.c_long(10364)

        # initialize variables
        self.data = numpy.zeros((parms.samples_raw,),dtype=numpy.float64)

    def PotentialChannel(self, task_handle, parms) :
        # Establish the potential channel
        self.dll.DAQmxCreateAIVoltageChan(task_handle, parms.channel,"",
                                   self.Cfg_Default, parms.min, parms.max, self.Volts, None) # or RSE (single-ended) instead of Cfg_Default?

    def ConfigureTiming(self, task_handle, parms) :
        self.dll.DAQmxCfgSampClkTiming(task_handle, parms.clock_source, parms.sample_rate,
                                       self.Rising, self.FiniteSamps, parms.samples)    # or ContSamps instead of FiniteSamps?


    def StartTrigger(self, task_handle, parms, f) :
        err = 0
        ErrorCheck(f, f.CfgDigEdgeStartTrig(task_handle, ctypes.create_string_buffer('/Dev1/pfi0'), self.Rising))
        if (err != 0) :
            buf_size = 1000
            buf = ctypes.create_string_buffer('\000' * buf_size)
            self.dll.DAQmxGetExtendedErrorInfo(ctypes.byref(buf),buf_size)
            print(buf.value)

    def SetTriggerDelay(self, task_handle, delay) :
        # Delay is float64 and must be in seconds.
        err = self.dll.DAQmxSetStartTrigDelayUnits(task_handle, self.Seconds)
        if (err != 0) :
            buf_size = 1000
            buf = ctypes.create_string_buffer('\000' * buf_size)
            self.dll.DAQmxGetExtendedErrorInfo(ctypes.byref(buf),buf_size)
            print(buf.value)
        err = self.dll.DAQmxSetStartTrigDelay(task_handle, delay)
        if (err != 0) :
            buf_size = 1000
            buf = ctypes.create_string_buffer('\000' * buf_size)
            self.dll.DAQmxGetExtendedErrorInfo(ctypes.byref(buf),buf_size)
            print(buf.value)

    def TakeData(self, task_handle, parms, f) :
        types=Types()
        read = types.read
        ErrorCheck(f, f.ReadAnalogF64(task_handle, parms.ain_samples_per_channel, parms.timeout, self.GroupByChannel, self.data.ctypes.data,
                             parms.ain_samples, ctypes.byref(read),None))
        return read


class ADCParameters :
    def __init__(self, types, min, max, timeout, buffer_size, sample_rate, samples, channel, clock):
        # Use: ADCParameters(t, -10.0, 10.0, 10, 10000.0, 2000, 'Dev1/ai0', 'OnboardClock')
        self.min = types.float64(min)     #-10.0)
        self.max = types.float64(max)     # 10.0
        self.timeout = types.float64(timeout)     #10.0
        self.buffer_size = types.float64(buffer_size)      #10
        self.pointsToRead = buffer_size
        #self.pointsRead = types.uInt32()
        self.sample_rate = types.float64(sample_rate)     #10000.0)
        self.samples = types.uInt64(samples)      #2000)
        self.samples_raw=samples
        self.ain_samples = types.uInt32(samples)
        self.ain_samples_per_channel = types.int32(samples)
        self.channel = ctypes.create_string_buffer(channel)     #'Dev1/ai0')
        self.clock_source = ctypes.create_string_buffer(clock)       #'OnboardClock')


def Synchronous() :
    dll, message = LoadDLL()
    if dll == 0 :
        print 'Library not loadable.  ' + message
        sys.exit()
    c = TranslateDAQmxConstants()
    f = TranslateDAQmxFunctions(dll)
    dev = FindDevices(f)
    print dev
    ResetDevice(f)
    t = Types()
    task = CreateTask(f, t, 0)    # Create task 0
    #p = ADCParameters(t, -5, 5, 10, 100, 253164, 200, 'Dev1/ai0', 'OnboardClock')    # types, min, max, timeout, buffer_size, sample_rate, samples, channel, clock
    samples = 2
    applied_freq = 10000.0
    sample_rate = 2.0 * applied_freq   # This should be twice the signal frequency
    sample_period = 1.0/sample_rate
    adc_range = 5.0
    p = ADCParameters(t, -adc_range, adc_range, 10, 40000, sample_rate, samples, 'Dev1/ai0', 'OnboardClock')    # types, min, max, timeout, buffer_size, sample_rate, samples, channel, clock
    a = AnalogInDevice(dll, p)     # Initialize the analog input device
    a.PotentialChannel(task, p)     # Open an analog input channel for the task
    a.StartTrigger(task, p, f)
    a.ConfigureTiming(task, p)    # Configure the timing for taking data points on this channel for this task.
    sample_delay = sample_period/2.0
    trials = 10.0
    delta_t = sample_delay/trials
    times = numpy.arange(sample_delay - trials*delta_t/2, sample_delay + trials*delta_t/2, delta_t)
    signal = numpy.array([])
    #StartTask(f, task)                     # Begin the task
    for dtime in times :
        #ResetDevice(f)
        #task = CreateTask(f, t, 0)    # Create task 0
        #a.PotentialChannel(task, p)     # Open an analog input channel for the task
        #a.StartTrigger(task, p, f)
        #a.ConfigureTiming(task, p)    # Configure the timing for taking data points on this channel for this task.
        #a.SetTriggerDelay(task, t.float64(dtime))
        #StartTask(f, task)                     # Begin the task
        data_points_taken = a.TakeData(task, p, f)   # Take some data
        #EndTask(f, task)
        #numpoints = data_points_taken.value
        #print "Acquired %d points"%(data_points_taken.value)
        tot = 0
        print a.data
        for i in range(0, len(a.data), 1) :
            tot += a.data[i] * (-1)**i
        signal = numpy.append(signal, tot)
        print 'sample_rate, delay, signal = ', sample_rate, dtime, tot
    #EndTask(f, task)
    f1 = plt.figure()
    sb1 = f1.add_subplot(111)
    sb1.plot(times, signal)
    #sb1.set_ylim(ymin=-20.0, ymax =20.0)
    sb1.set_xlabel('Time Delay in Seconds')
    sb1.set_ylabel('Amplitude in Volts')
    sb1.set_title('Synchronous Signal : '+str(applied_freq/1000)+' kHz, '+str(int(sample_rate)/1000)+' kSPS, '+str(samples/1000)+' kSamples')
    sb1.grid(True)
    plt.show()
    ClearTask(f, task)
    plt.close()

    #plot(b)
    #plot(a.data)
    #grid(True)
    #show()

def ResetDevice(f) :
    ErrorCheck(f, f.ResetDevice(ctypes.create_string_buffer('Dev1')))


#----------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__' :
        Synchronous()

