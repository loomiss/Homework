
import os, sys, time
import ctypes as ct
import numpy
import nidaqmx_constants as mxc
import nidaqmx_functions as mxf

def LoadDLL() :
    # load the DLL with linux or windows specific invocations.
    # os.name is 'posix', 'nt', 'os2', 'mac', 'ce' or 'riscos'
    message = ''
    if os.name == 'posix' :
        try:
            dll = ct.cdll.LoadLibrary("nicaiu.so")
            #dll = ct.CDLL("nicaiu.so")         # create an instance of a dll
        except :
            dll = 0
    elif os.name == 'nt' :
        # cdll loads libraries which export functions using the standard cdecl calling convention.
        # windll libraries call functions using the stdcall calling convention.
        try:
            dll = ct.windll.nicaiu
            #dll = ct.cdll.somelibrary
        except :
            dll = 0
    else :
        message = 'This operating system is not supported.'
        dll = 0
    if dll == 0 :
        message = 'The required dll nicaiu was not found.'
    return dll, message

def FindDevices(f) :
    # f is the object of translated functions.
    buf_size = 10
    buf = ct.create_string_buffer('\000' * buf_size)
    f.GetSysDevNames(buf, buf_size);
    #print(ct.sizeof(buf), repr(buf.raw))
    #print(buf.raw)      # Labels for devices found by nicaiu
    return buf.raw.strip(chr(0))

def ErrorCheck(f, err):
    # A simple error checking routine
    # f is the object of functions, such as CreateTask.
    if err < 0:
        buf_size = 1000
        buf = ct.create_string_buffer('\000' * buf_size)
        f.GetErrorString(err, ct.byref(buf), buf_size)
        #raise RuntimeError('Call failed with error %d: %s'%(err, repr(buf.value)))
        print('Call failed with error %d: %s'%(err, repr(buf.value)))
    if err > 0:
        buf_size = 1000
        buf = ct.create_string_buffer('\000' * buf_size)
        f.GetErrorString(err, ct.byref(buf), buf_size)
        print('Warning %d: %s'%(err, repr(buf.value)))

def CreateTask(f, task) :
    task_handle = ct.c_ulong()
    ErrorCheck(f, f.CreateTask(str(task),ct.byref(task_handle)))
    print 'task handle: ', task_handle
    return task_handle

def Test() :
	dll, message = LoadDLL()
	if dll == 0 :
		print 'Library not loadable.  ' + message
		sys.exit()
	c = mxc.TranslatedConstants()
	f = mxf.TranslatedFunctions(dll)
	dev = FindDevices(f)
	print dev
	f.ResetDevice(ct.create_string_buffer('Dev1'))
	task = CreateTask(f, 0)
	task1 = CreateTask(f, 1)
	#ErrorCheck(f, f.CreateTask(ct.create_string_buffer('0'), 
	# CreateAIVoltageChan(TaskHandle taskHandle, const char physicalChannel[], const char nameToAssignToChannel[], int32 terminalConfig, float64 minVal, float64 maxVal, int32 units, const char customScaleName[])
	# CreateDOChan(TaskHandle taskHandle, const char lines[], const char nameToAssignToLines[], int32 lineGrouping)
	ErrorCheck(f, f.CreateDOChan(task, ct.create_string_buffer('Dev1/port0'), ct.create_string_buffer(''), ct.c_long(c.Val_ChanForAllLines)))
	ErrorCheck(f, f.CreateAIVoltageChan(task1, ct.create_string_buffer('Dev1/ai0'), ct.create_string_buffer('0'), ct.c_long(c.Val_RSE), ct.c_double(-2.0), ct.c_double(2.0), ct.c_long(c.Val_Volts), None))
	# (TaskHandle taskHandle, const char source[], float64 rate, int32 activeEdge, int32 sampleMode, uInt64 sampsPerChan)
	#ErrorCheck(f, f.CfgSampClkTiming(task, ct.create_string_buffer('OnboardClock'), ct.c_double(20000), ct.c_long(c.Val_Rising), ct.c_long(c.Val_FiniteSamps), ct.c_ulonglong(samples)))
	delta = 0.001
	samples = 1
	data = numpy.zeros((samples,),dtype=numpy.float64)
	samples_acquired = ct.c_long()
	f.StartTask(task)
	f.StartTask(task1)
	while True :
	    for i in range(10) :
		#samples_sent = ct.c_long()
		#data_ten = ct.c_int * 1
		#data = data_ten(1)
		#f.WriteDigitalU32(TaskHandle taskHandle, int32 numSampsPerChan, bool32 autoStart, float64 timeout, bool32 dataLayout, const uInt32 writeArray[], int32 *sampsPerChanWritten, bool32 *reserved);
		#ErrorCheck(f, f.WriteDigitalU32(task, ct.c_long(1), ct.c_long(0), ct.c_double(0.1), ct.c_long(c.Val_GroupByChannel), ct.byref(data), ct.byref(samples_sent), None))
		#f.WriteDigitalScalarU32(TaskHandle taskHandle, bool32 autoStart, float64 timeout, uInt32 value, bool32 *reserved)
		ErrorCheck(f, f.WriteDigitalScalarU32(task, ct.c_long(0), ct.c_double(0.01), ct.c_ulong(0), None))
		time.sleep(.0001)
		#data = data_ten(0)
		#f.WriteDigitalU32(TaskHandle taskHandle, int32 numSampsPerChan, bool32 autoStart, float64 timeout, bool32 dataLayout, const uInt32 writeArray[], int32 *sampsPerChanWritten, bool32 *reserved);
		#ErrorCheck(f, f.WriteDigitalU32(task, ct.c_long(1), ct.c_long(0), ct.c_double(0.1), ct.c_long(c.Val_GroupByChannel), ct.byref(data), ct.byref(samples_sent), None))
		#f.WriteDigitalScalarU32(TaskHandle taskHandle, bool32 autoStart, float64 timeout, uInt32 value, bool32 *reserved)
		ErrorCheck(f, f.WriteDigitalScalarU32(task, ct.c_long(0), ct.c_double(0.01), ct.c_ulong(1), None))
		time.sleep(delta)
		#(TaskHandle taskHandle, int32 numSampsPerChan, float64 timeout, bool32 fillMode, float64 readArray[], uInt32 arraySizeInSamps, int32 *sampsPerChanRead, bool32 *reserved)
		ErrorCheck(f, f.ReadAnalogF64(task1, ct.c_long(samples), ct.c_double(1.0), ct.c_long(c.Val_GroupByChannel), data.ctypes.data, ct.c_ulong(samples), ct.byref(samples_acquired), None))
		print data
	    time.sleep(0.01)
	#data = data_ten(0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
	#f.WriteDigitalU32(TaskHandle taskHandle, int32 numSampsPerChan, bool32 autoStart, float64 timeout, bool32 dataLayout, const uInt32 writeArray[], int32 *sampsPerChanWritten, bool32 *reserved);
	#ErrorCheck(f, f.WriteDigitalU32(task, ct.c_long(1), ct.c_long(0), ct.c_double(0.1), ct.c_long(c.Val_GroupByChannel), ct.byref(data), ct.byref(samples_sent), None))
	f.StopTask(task)
	f.StopTask(task1)
	#print samples_sent
	print data


#-----------------------------------------------------------------------

if __name__ == '__main__' :
	Test()
