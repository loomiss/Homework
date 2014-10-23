#ain_nidaqmx.py

# This is a near-verbatim translation of the example program
# C:\Program Files\National Instruments\NI-DAQ\Examples\DAQmx ANSI C\Analog In\Measure Voltage\Acq-Int Clk\Acq-IntClk.c

import numpy
from pylab import *
from nidaqmx import *
import ctypes

class AnalogInDevice :
    def __init__(self, dll, parms) :
        # dll is the handle to the dll.  device is the "Dev1", etc..
        self.dll = dll
        # Define constants corresponding to values in  C:\Program Files\National Instruments\NI-DAQ\DAQmx ANSI C Dev\include\NIDAQmx.h
        self.Cfg_Default = int32(-1)
        self.Volts = 10348
        self.Rising = 10280
        self.FiniteSamps = 10178
        self.GroupByChannel = 0
        self.ChanForAllLines = 1
        self.RSE = 10083
        self.ContSamps = 10123
        self.GroupByScanNumber = 1

        # initialize variables
        self.data = numpy.zeros((parms.samples_raw,),dtype=numpy.float64)

    def PotentialChannel(self, task_handle, parms) :
        # Establish the potential channel
        self.dll.DAQmxCreateAIVoltageChan(task_handle, parms.channel,"",
                                   self.Cfg_Default, parms.min, parms.max, self.Volts, None) # or RSE (single-ended) instead of Cfg_Default?

    def ConfigureTiming(self, task_handle, parms) :
        self.dll.DAQmxCfgSampClkTiming(task_handle, parms.clock_source, parms.sample_rate,
                                       self.Rising, self.FiniteSamps, parms.samples)    # or ContSamps instead of FiniteSamps?


    def StartTrigger(self, task_handle, parms) :
        
        err = self.dll.DAQmxCfgDigEdgeStartTrig(task_handle, ctypes.create_string_buffer('/dev1/pfi0'),
                                           self.Rising)
        if (err != 0) :
            buf_size = 1000
            buf = ctypes.create_string_buffer('\000' * buf_size)
            self.dll.DAQmxGetExtendedErrorInfo(ctypes.byref(buf),buf_size)
            print(buf.value)
        

    def TakeData(self, task_handle, parms) :
        types=Types()
        read = types.read
        self.dll.DAQmxReadAnalogF64(task_handle, parms.samples_raw, parms.buffer_size,
                             self.GroupByChannel, self.data.ctypes.data,
                             parms.samples_raw, ctypes.byref(read),None)
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
        self.channel = ctypes.create_string_buffer(channel)     #'Dev1/ai0')
        self.clock_source = ctypes.create_string_buffer(clock)       #'OnboardClock')


def Simple() :
    dll, message = LoadDLL()
    if dll == 0 :
        print 'Library not loadable.  ' + message
        sys.exit()
    t = Types()
    

    # types, min, max, timeout, buffer_size, sample_rate, samples, channel, clock


    #task = CreateTask(dll, t, 0)    # Create task 0
    task_number = ctypes.c_ulong(0)
    task = ctypes.c_ulong(dll.DAQmxCreateTask("",ctypes.byref(task_number)))    # Create task 0

    p = ADCParameters(t, -5, 5, 10, 100, 253164, 200, 'Dev1/ai0', 'OnboardClock')    # types, min, max, timeout, buffer_size, sample_rate, samples, channel, clock
    a = AnalogInDevice(dll, p)     # Initialize the analog input device

    ErrorCheck(dll, a.PotentialChannel(task, p))     # Open an analog input channel for the task

    a.StartTrigger(task, p)
    a.ConfigureTiming(task, p)    # Configure the timing for taking data points on this channel for this task.

    #StartTask(dll, task)                     # Begin the task
    dll.DAQmxStartTask(task)
    data_points_taken = a.TakeData(task, p)   # Take some data
    numpoints = data_points_taken.value
    print "Acquired %d points"%(data_points_taken.value)

    #EndTask(dll, task)
    dll.DAQmxStopTask(task)
    dll.DAQmxClearTask(task)

    b = rfft(a.data)
    #plot(b)
    plot(a.data)
    show()

def ErrorCheck(dll, err):
    # A simple error checking routine
    # f is the object of functions, such as CreateTask.
    if err < 0:
        buf_size = 100
        buf = ctypes.create_string_buffer('\000' * buf_size)
        dll.DAQmxGetErrorString(err, ctypes.byref(buf), buf_size)
        raise RuntimeError('Call failed with error %d: %s'%(err, repr(buf.value)))
    if err > 0:
        buf_size = 100
        buf = ctypes.create_string_buffer('\000' * buf_size)
        dll.DAQmxGetErrorString(err, ctypes.byref(buf), buf_size)
        print('Warning %d: %s'%(err, repr(buf.value)))


def ResetDll() :
    dll, message = LoadDLL()
    if dll == 0 :
        print 'Library not loadable.  ' + message
        sys.exit()

    dll.DAQmxResetDevice(ctypes.create_string_buffer('dev1'))
    

#----------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__' :
        Simple()

