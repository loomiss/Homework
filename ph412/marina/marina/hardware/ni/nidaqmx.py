import os
import sys
import ctypes as ct
import nidaqmx_constants as mxc
import nidaqmx_functions as mxf

#required_modules = ['ctypes', 'nidaqmx_functions', 'nidaqmx_constants']

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

def TranslateDAQmxConstants() :
    return mxc.TranslatedConstants()

def TranslateDAQmxFunctions(dll) :
    return mxf.TranslatedFunctions(dll)

def FindDevices(f) :
    # f is the object of translated functions.
    buf_size = 10
    buf = ct.create_string_buffer('\000' * buf_size)
    f.GetSysDevNames(buf, buf_size);
    #print(ct.sizeof(buf), repr(buf.raw))
    #print(buf.raw)      # Labels for devices found by nicaiu
    return buf.raw.strip(chr(0))

def GetDeviceParameters(f) :
    message = ''
    buf_size = 20
    buf = ct.create_string_buffer('\000' * buf_size)
    #f.GetDevBusType(ct.byref(buf), buf_size)         #(const char device[], int32 *data);
    a = ct.c_char_p('')
    data = ct.c_ulong(0)
    bus = ct.c_ulong(0)
    #bus = f.GetDevBusType(a, data)
    prod = f.GetDevProductNum(a, data)
    message = 'Product number: ' + str(prod) + '\n'
    return message

class Types :
    def __init__(self) :
        self.int32 = ct.c_long
        self.uInt32 = ct.c_ulong
        self.uInt64 = ct.c_ulonglong
        self.float64 = ct.c_double
        self.task_handle = self.uInt32
        self.written = self.int32
        self.read = self.int32()

def ResetDevice(f, device_string) :
    f.ResetDevice(ct.create_string_buffer(device_string))

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


def CreateTask(f, types, task) :
    task_handle = types.task_handle()
    ErrorCheck(f, f.CreateTask(str(task), ct.byref(task_handle)))
    print 'Task handle: ', task_handle
    return task_handle

def StartTask(f, task_handle) :
    ErrorCheck(f, f.StartTask(task_handle))

def EndTask(f, task_handle) :
    f.StopTask(task_handle)

def ClearTask(f, task_handle) :
    ErrorCheck(f, f.ClearTask(task_handle))


def Test() :
    dll, message = LoadDLL()    # Establish a handle to the dll
    if dll == 0 :
        print 'Library not loadable.  ' + message
        sys.exit()
    print message
    c = TranslateDAQmxConstants()
    print c.Val_RSE
    f = TranslateDAQmxFunctions(dll)
    print f.CreateTask
    devices = FindDevices(f)
    print devices, len(devices)
    t = Types()                         # Define some recognizable data types.
    th = CreateTask(f, t, 0)    # Create the handle for task 0.
    print th
    #StartTask(dll, th)     # Must have some channels associated with the task before you can start it

#----------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__' :
    Test()


