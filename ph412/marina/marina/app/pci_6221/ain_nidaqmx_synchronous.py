
import numpy
import time

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
        int32 = ctypes.c_long
        self.Cfg_Default = int32(-1)
        self.Volts = int32(10348)
        self.Rising = int32(10280)
        self.FiniteSamps = int32(10178)
        self.GroupByChannel = int32(0)
        self.ChanForAllLines = int32(1)
        self.RSE = int32(10083)
        self.ContSamps = int32(10123)
        self.GroupByScanNumber = int32(1)
        self.Seconds = ctypes.c_long(10364)

        # initialize variables
        self.data = numpy.zeros((parms.samples_raw,),dtype=numpy.float64)

    def PotentialChannel(self, task_handle, parms) :
        # Establish the potential channel
        self.dll.DAQmxCreateAIVoltageChan(task_handle, parms.channel,"",
                                   self.RSE, parms.min, parms.max, self.Volts, None) # or RSE (single-ended) instead of Cfg_Default?

    def ConfigureTiming(self, task_handle, f, c, parms) :
        # (TaskHandle taskHandle, const char source[], float64 rate, int32 activeEdge, int32 sampleMode, uInt64 sampsPerChan)
        f.CfgSampClkTiming(task_handle, parms.clock_source, parms.sample_rate, c.Val_Rising, c.Val_FiniteSamps, parms.samples)    # or ContSamps instead of FiniteSamps?


    def StartTrigger(self, task_handle, f, c) :
        err = 0
        ErrorCheck(f, f.CfgDigEdgeStartTrig(task_handle, ctypes.create_string_buffer('/dev1/pfi0'), c.Val_Rising))
    
    def GetStartTriggerSource(self, task_handle, f) :
        buf_size = 20
        buf = ctypes.create_string_buffer('\000' * buf_size)
        print 'Digital edge start trigger source: '
        ErrorCheck(f, f.GetDigEdgeStartTrigSrc(task_handle, ctypes.byref(buf), ctypes.c_ulong(buf_size)))
        print buf.value

    def DisableTrigger(self, task_handle, f) :
        f.DisableStartTrig(task_handle)

    def SetTriggerDelayUnits(self, task_handle, f) :
        # Delay is float64 and must be in seconds.
        err = f.SetStartTrigDelayUnits(task_handle, self.Seconds)
        if (err != 0) :
            buf_size = 1000
            buf = ctypes.create_string_buffer('\000' * buf_size)
            f.GetExtendedErrorInfo(ctypes.byref(buf),buf_size)
            print(buf.value)

    def SetTriggerDelay(self, task_handle, delay, f) :
        err = f.SetStartTrigDelay(task_handle, delay)
        if (err != 0) :
            buf_size = 1000
            buf = ctypes.create_string_buffer('\000' * buf_size)
            GetExtendedErrorInfo(ctypes.byref(buf),buf_size)
            print 'Set Trigger Delay error :'
            print(buf.value)
        #response = ctypes.c_double()
        #err = f.GetStartTrigDelay(task_handle, ctypes.byref(response))
        #print response

    def TakeData(self, task_handle, parms, f) :
        types=Types()
        read = types.read
        #ErrorCheck(f, f.ReadAnalogF64(task_handle, parms.samples_raw, parms.timeout, self.GroupByChannel, self.data.ctypes.data,
                             #parms.ain_samples, ctypes.byref(read),None))
        err = f.ReadAnalogF64(task_handle, parms.samples_raw, parms.timeout, self.GroupByChannel, self.data.ctypes.data,
                             parms.ain_samples, ctypes.byref(read),None)
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
        self.channel = ctypes.create_string_buffer(channel)     #'Dev1/ai0')
        self.clock_source = ctypes.create_string_buffer(clock)       #'OnboardClock')


def SynchronousBurstWaveform() :     # Recover a cycle at 10 kHz from a dominant noise signal using a burst from a function generator.
    dll, message = LoadDLL()
    if dll == 0 :
        print 'Library not loadable.  ' + message
        sys.exit()
    c = TranslateDAQmxConstants()
    f = TranslateDAQmxFunctions(dll)
    dev = FindDevices(f)
    print dev
    #ResetDevice(f)
    #time.sleep(3.0)
    t = Types()
    task = CreateTask(f, t, 0)    # Create task 0
    #p = ADCParameters(t, -5, 5, 10, 100, 253164, 200, 'Dev1/ai0', 'OnboardClock')    # types, min, max, timeout, buffer_size, sample_rate, samples, channel, clock
    samples = 1000
    applied_freq = 10000.0
    period = 1.0/applied_freq
    sample_rate = 2.0 * applied_freq   # This should be twice the signal frequency
    sample_period = 1.0/sample_rate
    adc_range = 1.0
    p = ADCParameters(t, -adc_range, adc_range, 10, 40000, sample_rate, samples, 'Dev1/ai0', 'OnboardClock')    # types, min, max, timeout, buffer_size, sample_rate, samples, channel, clock
    a = AnalogInDevice(dll, p)     # Initialize the analog input device
    a.PotentialChannel(task, p)     # Open an analog input channel for the task
    #a.GetStartTriggerSource(task, f)
    a.ConfigureTiming(task, f, c, p)    # Configure the timing for taking data points on this channel for this task.
    a.StartTrigger(task, f, c)
    a.SetTriggerDelayUnits(task, f)
    #sample_delay = sample_period/2.0
    delays = 6.0   # The number of delays is used to determine the set of delay times after the burst trigger pulse.
    cycles = 0.5    # The delays will be uniformly distributed over the specified number of cycles.  Not all (delays, cycles) pairs make sense.
    delta_t = cycles/delays * period
    #delta_t = sample_period/delays
    #points = 300.0
    #timesx = numpy.arange(sample_delay - trials*delta_t/2, sample_delay + trials*delta_t/2, delta_t)
    #cycles = 4.0*points/delays
    #time_limit = cycles*sample_period
    time_limit = cycles*period
    timesx = numpy.arange(0, time_limit + delta_t, delta_t)
    #print timesx
    times = timesx
    print times
    bursts = 10   # For each delay, average over this many bursts.
    signal = numpy.array([])
    print 'Points remaining : ',
    points = len(times)
    for dtime in times :
        a.SetTriggerDelay(task, t.float64(dtime), f)
        #StartTask(f, task)                     # Begin the task
        tot = 0
        for i in range(bursts) :
            f.StartTask(task)
            data_points_taken = a.TakeData(task, p, f)   # Take some data
            EndTask(f, task)
            #numpoints = data_points_taken.value
            #print "Acquired %d points"%(data_points_taken.value)
            #print a.data
            toto = 0
            for i in range(0, len(a.data), 1) :
                toto += a.data[i] * (-1)**i
            tot += toto/len(a.data)
        signal = numpy.append(signal, tot/bursts)
        points += -1
        print points,
        #print 'sample_rate, delay, signal = ', sample_rate, dtime, tot
    ClearTask(f, task)
    #ResetDevice(f)
    #print 'First 50 data points:'
    #print a.data[:50]
    f1 = plt.figure()
    sb1 = f1.add_subplot(111)
    sb1.plot(times, signal)
    #sb1.set_ylim(ymin=-20.0, ymax =20.0)
    sb1.set_xlabel('Time Delay in Seconds')
    sb1.set_ylabel('Amplitude in Volts')
    title = 'Synchronous Signal Burst Mode: '+str(applied_freq/1000)+' kHz, '+str(samples/1000)+' kSamples per Burst'
    title += '\n' + str(int(sample_rate)/1000)+' kSPS, ' + str(delays) + ' Delay Values, ' + str(bursts) + ' Bursts per Delay Value'
    sb1.set_title(title)
    sb1.grid(True)
    plt.show()
    plt.close()

    #plot(b)
    #plot(a.data)
    #grid(True)
    #show()

def SynchronousBurstPeak() :     # Recover only the peak amplitude at 10 kHz from a dominant noise signal using a burst from a function generator.
    dll, message = LoadDLL()
    if dll == 0 :
        print 'Library not loadable.  ' + message
        sys.exit()
    c = TranslateDAQmxConstants()
    f = TranslateDAQmxFunctions(dll)
    dev = FindDevices(f)
    print dev
    #ResetDevice(f)
    #time.sleep(3.0)
    t = Types()
    task = CreateTask(f, t, 0)    # Create task 0
    #p = ADCParameters(t, -5, 5, 10, 100, 253164, 200, 'Dev1/ai0', 'OnboardClock')    # types, min, max, timeout, buffer_size, sample_rate, samples, channel, clock
    samples = 1000
    applied_freq = 10000.0
    period = 1.0/applied_freq
    sample_rate = 2.0 * applied_freq   # This should be twice the signal frequency
    sample_period = 1.0/sample_rate
    adc_range = 1.0
    p = ADCParameters(t, -adc_range, adc_range, 10, 40000, sample_rate, samples, 'Dev1/ai0', 'OnboardClock')    # types, min, max, timeout, buffer_size, sample_rate, samples, channel, clock
    a = AnalogInDevice(dll, p)     # Initialize the analog input device
    a.PotentialChannel(task, p)     # Open an analog input channel for the task
    #a.GetStartTriggerSource(task, f)
    a.ConfigureTiming(task, f, c, p)    # Configure the timing for taking data points on this channel for this task.
    a.StartTrigger(task, f, c)
    a.SetTriggerDelayUnits(task, f)
    #sample_delay = sample_period/2.0
    #delays = 6.0   # The number of delays is used to determine the set of delay times after the burst trigger pulse.
    cycles = 10    # An integer number of cycles over which to measure the amplitude.
    delta_t = period/4.0
    #delta_t = sample_period/delays
    #points = 300.0
    #timesx = numpy.arange(sample_delay - trials*delta_t/2, sample_delay + trials*delta_t/2, delta_t)
    #cycles = 4.0*points/delays
    #time_limit = cycles*sample_period
    time_limit = cycles*period
    timesx = numpy.arange(0, time_limit + delta_t, delta_t)
    #print timesx
    times = timesx
    print times
    bursts = 10   # For each delay, average over this many bursts.
    signal = numpy.array([])
    print 'Points remaining : ',
    points = len(times)
    for dtime in times :
        a.SetTriggerDelay(task, t.float64(dtime), f)
        #StartTask(f, task)                     # Begin the task
        tot = 0
        for i in range(bursts) :
            f.StartTask(task)
            data_points_taken = a.TakeData(task, p, f)   # Take some data
            EndTask(f, task)
            #numpoints = data_points_taken.value
            #print "Acquired %d points"%(data_points_taken.value)
            #print a.data
            toto = 0
            for i in range(0, len(a.data), 1) :
                toto += a.data[i] * (-1)**i
            tot += toto/len(a.data)
        signal = numpy.append(signal, tot/bursts)
        points += -1
        print points,
        #print 'sample_rate, delay, signal = ', sample_rate, dtime, tot
    ClearTask(f, task)
    #ResetDevice(f)
    #print 'First 50 data points:'
    #print a.data[:50]
    f1 = plt.figure()
    sb1 = f1.add_subplot(111)
    sb1.plot(times, signal)
    #sb1.set_ylim(ymin=-20.0, ymax =20.0)
    sb1.set_xlabel('Time Delay in Seconds')
    sb1.set_ylabel('Amplitude in Volts')
    title = 'Synchronous Signal Burst Mode: '+str(applied_freq/1000)+' kHz, '+str(samples/1000)+' kSamples per Burst'
    title += '\n' + str(int(sample_rate)/1000)+' kSPS, ' + str(delays) + ' Delay Values, ' + str(bursts) + ' Bursts per Delay Value'
    sb1.set_title(title)
    sb1.grid(True)
    plt.show()
    plt.close()

def SynchronousPeak() :     # Detect at the peak only
    dll, message = LoadDLL()
    if dll == 0 :
        print 'Library not loadable.  ' + message
        sys.exit()
    c = TranslateDAQmxConstants()
    f = TranslateDAQmxFunctions(dll)
    dev = FindDevices(f)
    print dev
    #ResetDevice(f)
    #time.sleep(3.0)
    t = Types()
    task = CreateTask(f, t, 0)    # Create task 0
    #p = ADCParameters(t, -5, 5, 10, 100, 253164, 200, 'Dev1/ai0', 'OnboardClock')    # types, min, max, timeout, buffer_size, sample_rate, samples, channel, clock
    samples = 4500
    applied_freq = 10000.0
    sample_rate = 2.0 * applied_freq   # This should be twice the signal frequency
    sample_period = 1.0/sample_rate
    adc_range = 1.0
    p = ADCParameters(t, -adc_range, adc_range, 10, 40000, sample_rate, samples, 'Dev1/ai0', 'OnboardClock')    # types, min, max, timeout, buffer_size, sample_rate, samples, channel, clock
    a = AnalogInDevice(dll, p)     # Initialize the analog input device
    a.PotentialChannel(task, p)     # Open an analog input channel for the task
    #a.GetStartTriggerSource(task, f)
    a.ConfigureTiming(task, f, c, p)    # Configure the timing for taking data points on this channel for this task.
    a.StartTrigger(task, f, c)
    a.SetTriggerDelayUnits(task, f)
    sample_delay = sample_period/2.0
    trials = 60
    delta_t = sample_period/2.0
    #timesx = numpy.arange(sample_delay - trials*delta_t/2, sample_delay + trials*delta_t/2, delta_t)
    timesx = numpy.arange(0, trials, 1)
    #print timesx
    times = timesx
    signal = numpy.array([])
    print 'Delay : ' + str(delta_t)
    print 'Points remaining : ',
    for dtime in times :
        a.SetTriggerDelay(task, t.float64(delta_t), f)
        StartTask(f, task)                     # Begin the task
        data_points_taken = a.TakeData(task, p, f)   # Take some data
        EndTask(f, task)
        #numpoints = data_points_taken.value
        #print "Acquired %d points"%(data_points_taken.value)
        tot = 0
        #print a.data
        for i in range(0, len(a.data), 1) :
            tot += a.data[i] * (-1)**i
        signal = numpy.append(signal, tot/len(a.data))
        print trials - dtime - 1,
        #print 'sample_rate, delay, signal = ', sample_rate, delta_t, tot
    print
    ClearTask(f, task)
    #ResetDevice(f)
    #print 'First 50 data points:'
    #print a.data[:50]
    #f1 = plt.figure()
    #sb1 = f1.add_subplot(111)
    #sb1.plot(times, signal)
    ##sb1.set_ylim(ymin=-20.0, ymax =20.0)
    #sb1.set_xlabel('Time Delay in Seconds')
    #sb1.set_ylabel('Amplitude in Volts')
    #sb1.set_title('Synchronous Signal : '+str(applied_freq/1000)+' kHz, '+str(int(sample_rate)/1000)+' kSPS, '+str(samples/1000)+' kSamples')
    #sb1.grid(True)
    #plt.show()
    #plt.close()
    order = 1
    fit, fit_n, coeffs, sigma, average = FitDataToPolynomial(times, signal, order)
    # Only one of the following two operations can be performed without a plot error.
    # Uncomment your choice.
    graph_title = 'Synchronous Peak Detection : '+str(applied_freq/1000)+' kHz, '+str(int(sample_rate)/1000)+' kSPS, '+str(samples/1000)+' kSamples'
    average_sig = SigDigits(average, 4)
    sigma_sig = SigDigits(sigma, 4)
    graph_title += '\nAverage = ' + str(average_sig) + ', Sigma = ' + str(sigma_sig) + ', SNR = ' + str(SigDigits(20*numpy.log10(average/sigma), 3)) + ' dB'
    PlotFit(times, signal, fit_n, fit, coeffs, sigma, graph_title)
    #MakeResidualHistogram(y, fit, bins, sigma)

## sigdigits(x,n) - converts a number to a number with n significant digits
 
import sys
 
def SigDigits(x, n):
    if n < 1:
        raise ValueError("number of significant digits must be >= 1")
 
    # Use %e format to get the n most significant digits, as a string.
    format = "%." + str(n-1) + "e"
    r = format % x
    return float(r)
 


def FitDataToPolynomial(x, y, order) :
    np = numpy
    coeffs, residuals, rank, singular_values, rcond = np.polyfit(x, y, order, full=True)
    crev = coeffs[:: -1]    # Reverse the order of the coeffs array
    sigma = np.sqrt(residuals[0]/len(x))
    print('sigma = ' + str(sigma))
    z =np.zeros( (order+1, len(x)) )
    ztot = np.zeros(len(x), float)
    for n in range(0, order+1, 1) :
        z[n] += crev[n] * np.power(x, n)
        ztot += z[n]
    print ztot
    print type(ztot)
    #average, weights = np.average(ztot)
    average = 0
    for zip in ztot : 
        average += zip
    average = average/len(ztot)
    return ztot, z, crev, sigma, average

def PlotFit(x, y, z, ztot, coeffs, sigma, title) :
    np = numpy
    plt.plot(x, y, label='Data')
    coeff_string = 'Fit Coefficients\n'
    n = 0
    for c in coeffs :
        coeff_string += str(n) + ':   ' + str(coeffs[n]) + '\n'
        plt.plot(x, z[n], label='$x^{' + str(n) + '}$ piece')
        n += 1
    coeff_string += 'sigma = ' + str(sigma) + '\n'
    plt.plot(x, ztot, label = 'Total Fit')
    #plt.legend(loc='best')
    plt.legend(loc='lower right')
    plt.title( title )
    plt.xlabel('Samples')
    plt.ylabel('Amplitude (Volt)')
    graph_min = np.min(ztot)
    graph_max = np.max(ztot)
    for zn in z :
        zn_max = np.max(zn)
        zn_min = np.min(zn)
        if zn_max > graph_max :
            graph_max = zn_max
        if zn_min < graph_min :
            graph_min = zn_min
    plt.text(1, graph_min +1, coeff_string)
    plt.show()
    plt.close()
    return

def MakeResidualHistogram(data, fit, bins, sigma) :
    # Make a histogram of the abs(error)
    #e2 = np.abs(data - fit)
    e2 = data - fit
    hist = np.histogram(e2, bins=bins)
    # Histogram returns the array of values and an array of bin edges, which has one more value.
    # Create bin center.
    bincenters = 0.5*(hist[1][1:]+hist[1][:-1])
    histo_max = np.max(hist[0])
    # Simulate the set of error, but with more samples for less noise on the noise.
    #   The mean should be 0.0, but it will fluctuate about that from run to run.
    normal_dist = ran.normal(0.0, sigma, len(e2)*3000) * histo_max * np.sqrt(2.0*np.pi)*sigma
    normal_hist = np.histogram(normal_dist, bins=bins)
    normal_hist_max = np.max(normal_hist[0])
    plt.plot(bincenters, hist[0], label='Data')
    plt.plot(bincenters, normal_hist[0]*histo_max/normal_hist_max, label='Simulation')
    the_title = 'Error Histogram with $\sigma = $' + str(sigma)
    plt.title(the_title)
    plt.legend(loc='best')
    plt.show()
    plt.close()

def ResetDevice(f) :
    ErrorCheck(f, f.ResetDevice(ctypes.create_string_buffer('Dev1')))


#----------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__' :
    SynchronousBurstWaveform()
    #SynchronousPeak()

