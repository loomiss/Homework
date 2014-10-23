
#contAcquireNChan.py

import ctypes
import numpy

nidaq = ctypes.windll.nicaiu # load the DLL

##############################
# Setup some typedefs and constants
# to correspond with values in
# C:\Program Files\National Instruments\NI-DAQ\DAQmx ANSI C Dev\include\NIDAQmx.h

# the typedefs
int32 = ctypes.c_long
uInt32 = ctypes.c_ulong
uInt64 = ctypes.c_ulonglong
float64 = ctypes.c_double
TaskHandle = uInt32
written = int32()
pointsRead = uInt32()

# the constants
DAQmx_Val_Cfg_Default = int32(-1)
DAQmx_Val_Volts = 10348
DAQmx_Val_Rising = 10280
DAQmx_Val_FiniteSamps = 10178
DAQmx_Val_GroupByChannel = 0
DAQmx_Val_ChanForAllLines = 1
DAQmx_Val_RSE = 10083
DAQmx_Val_Volts = 10348
DAQmx_Val_ContSamps = 10123
DAQmx_Val_GroupByScanNumber = 1
##############################

def CHK(err):
    """a simple error checking routine"""
    if err < 0:
        buf_size = 1000
        buf = ctypes.create_string_buffer('\000' * buf_size)
        nidaq.DAQmxGetErrorString(err,ctypes.byref(buf),buf_size)
        raise RuntimeError('nidaq call failed with error %d: %s'%(err,repr(buf.value)))

# initialize variables
taskHandle = TaskHandle(0)
min = float64(-10.0)
max = float64(10.0)
timeout = float64(10.0)
bufferSize = uInt32(10)
pointsToRead = bufferSize
pointsRead = uInt32()
sampleRate = float64(10000.0)
samplesPerChan = uInt64(2000)
chan = ctypes.create_string_buffer('Dev1/ai0')
clockSource = ctypes.create_string_buffer('OnboardClock')


data = numpy.zeros((1000,),dtype=numpy.float64)


# Create Task and Voltage Channel and Configure Sample Clock
def SetupTask():
    CHK(nidaq.DAQmxCreateTask("",ctypes.byref(taskHandle)))
    CHK(nidaq.DAQmxCreateAIVoltageChan(taskHandle,chan,"",DAQmx_Val_RSE,min,max,
        DAQmx_Val_Volts,None))
    CHK(nidaq.DAQmxCfgSampClkTiming(taskHandle,clockSource,sampleRate,
        DAQmx_Val_Rising,DAQmx_Val_ContSamps,samplesPerChan))
    CHK(nidaq.DAQmxCfgInputBuffer(taskHandle,200000))

#Start Task
def StartTask():
    CHK(nidaq.DAQmxStartTask (taskHandle))

#Read Samples
def ReadSamples(points):
    bufferSize = uInt32(points)
    pointsToRead = bufferSize
    data = numpy.zeros((points,),dtype=numpy.float64)
    CHK(nidaq.DAQmxReadAnalogF64(taskHandle,pointsToRead,timeout,
            DAQmx_Val_GroupByScanNumber,data.ctypes.data,
            uInt32(2*bufferSize.value),ctypes.byref(pointsRead),None))

    print "Acquired %d pointx(s)"%(pointsRead.value)

    return data

def StopAndClearTask():
    if taskHandle.value != 0:
        nidaq.DAQmxStopTask(taskHandle)
        nidaq.DAQmxClearTask(taskHandle)
