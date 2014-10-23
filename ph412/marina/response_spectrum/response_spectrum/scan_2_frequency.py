
from scan_2_plot import *
from scan_2_io import *
from numpy import *
import time
import string as s


def MakeFrequencyArrayDecades(decades, steps) :
    nu = array([], dtype=float)
    delta = (decades[1] - decades[0])/steps
    logf = decades[0] - delta   # logf is the log10(nu)
    for i in range(steps) :
        logf += delta
        freq = power(10, logf)
        if freq > 2.5e+07 : # limit for the Tek AFG3021B
            break
        nu = append(nu, freq)
    return nu

def MakeFrequencyArrayLinear(freq_range, steps) :
    nu = array([], dtype=float)
    delta = (freq_range[1] - freq_range[0])/steps
    freq = freq_range[0] - delta
    for i in range(steps) :
        freq += delta
        if freq > 2.5e+07 : # limit for the Tek AFG3021B
            break
        nu = append(nu, freq)
    return nu

def PrepareForFrequencyScan(fg, scope, inst, op) :
    # parms is the list of parameters read from the <program name>_commands.txt file.
    # Amplitude is half the pk-pk value, and average is the number of sweeps to average.
    # Creat array of frequencies
    error = ''
    tab = '\t'
    # Set the function generator
    # First execute the commands from the command file.
    print '\nSend function generator commands: '
    for c in inst['fg']['com'] :
        fg.Write(c)
        time.sleep(0.3)
        print tab + c
    if op.has_key('steps') :
        try:
            steps = int(s.strip(op['steps'][0]))
        except :
            print 'Steps parameter in scan_parameters.txt cannot be evaluated as an integer, so steps = 10.'
            steps = 10
    else :
        steps = 10
    freq_def = 'decadic'    # or linear default value
    if op.has_key('linear frequency range') :
        freq_def = 'linear'
        linear = array([])
        for o in op['linear frequency range'] :
            linear = append(linear, float(o))
    else :
        linear = array([1e05, 1e06])
    if op.has_key('decadic frequency range') :
        freq_def = 'decadic'
        decades = array([])
        for o in op['decadic frequency range'] :
            decades = append(decades, float(o))
    else :
        decades = array([2, 3, 4, 5])
    print 'Frequency scan definition = ' + freq_def
    print 'Steps = ', steps
    if freq_def == 'decadic':
        print 'decadic range = ', decades
        freqs = MakeFrequencyArrayDecades(decades, steps)
    elif freq_def == 'linear' :
        print 'Linear range = ', linear
        freqs = MakeFrequencyArrayLinear(linear, steps)
    #freqs = array([], dtype=float)      # A numpy array
    #for p in op['log multipliers'] :
        #for f in op['base frequencies']:
            #freqs = append(freqs, float(f) * power(10.0, float(p)))
    if op.has_key('input amplitude') :
        vin = op['input amplitude'][0]    # vin pk-pk
        vertical_scale1 = float(vin)/4.0
        if fg.identity == 'DG1022' :
            fg.Write('voltage ' + vin)
        else :
            fg.Write('voltage:amplitude ' + vin)
    else :
        error = 'Fatal error: input amplitude not specified.'
        return '', '', '', error
        vertical_scale1 = vertical_scale2
    #vertical_scale2 = float(op['amplitude'][0])/4.0
    if op.has_key('gain') :
        gain = float(op['gain'][0])    # maximum gain expected
        vertical_scale2 = gain * vertical_scale1
    else :
        vertical_scale2 = vertical_scale1
    period = 1.0/freqs[0]
    horizontal_scale = period/5.0
    #print freqs
    #print period, vertical_scale, horizontal_scale
    # Set the scope
    # First execute the commands from the command file.
    print '\nSend scope commands: '
    scope.Write('*rst')
    time.sleep(5.0)
    for c in inst['scope']['com'] :
        scope.Write(c)
        time.sleep(0.5)
        print tab + c
    com = []
    com.append('ch1:scale ' + str(vertical_scale1) + ';position ' + '0')   #str(2.0*vertical_scale)  # Volts and seconds
    com.append('ch2:scale ' + str(vertical_scale2) + ';position ' + '0')   #str(-2.0*vertical_scale)  # Volts and seconds
    com.append('horiz:scale ' + str(horizontal_scale))    # Trigger point is centered on the screen. If set to -horizontal_scale, it moves right 1 division.
    for c in com :
        scope.Write(c)
        print tab + c
    time.sleep(1.0)     # Wait a moment for the instruments to stabilize.
    return freqs, vertical_scale1, vertical_scale2, error

def AmplitudesAndPhases(scope, scale1, scale2, patience) :
    tab = '\t'
    stable = 0
    while stable == 0 :
        command = 'measu:immed:source ch1;type pk2pk;value?'
        scope.Write(command)
        a0 = scope.Read()
        #print a0
        a1 = float(s.split(a0, 'VALUE')[1])
        if a1 < scale1 * 5.5 :
            fac = scale1 * 5.5 / a1
            scale1 = scale1/1.5/fac
            #print 'new vertical scale = ', scale2
            command = 'ch1:scale ' + str(scale1) + ';position ' + '0'   #str(-2.0*scale2)  # Volts and seconds
            scope.Write(command)
            print tab + 'adjusting ch1'
            time.sleep(patience)
            stable = 0
        elif a1 > scale1 * 8.4 :
            fac = a1/scale1/8.4
            scale1 = fac*scale1*1.5
            #print 'new vertical scale = ', scale2
            command = 'ch1:scale ' + str(scale1) + ';position ' + '0'   #str(-2.0*scale2)  # Volts and seconds
            scope.Write(command)
            #a1, a2 = AmplitudesAndPhases(scope)     # Retake data
            print tab + 'adjusting ch1'
            time.sleep(patience)
            stable = 0
        else :
            stable = 1
    stable = 0
    while stable == 0 :
        command = 'measu:immed:source ch2;type pk2pk;value?'
        scope.Write(command)
        a2 = float(s.split(scope.Read(), 'VALUE')[1])
        #print 'Channel 1 and 2 amplitudes: ', ch1_amp, ch2_amp
        if a2 < scale2 * 5.5 :
            fac = scale2 * 5.5 / a2
            scale2 = scale2/1.5/fac
            #print 'new vertical scale = ', scale2
            command = 'ch2:scale ' + str(scale2) + ';position ' + '0'   #str(-2.0*scale2)  # Volts and seconds
            scope.Write(command)
            #a1, a2 = AmplitudesAndPhases(scope) # Retake data.
            print tab + 'adjusting ch2'
            time.sleep(patience)
            stable = 0
        elif a2 > scale2 * 8.4 :
            fac = a2/scale2/8.4
            scale2 = fac*scale2*1.5
            #print 'new vertical scale = ', scale2
            command = 'ch2:scale ' + str(scale2) + ';position ' + '0'   #str(-2.0*scale2)  # Volts and seconds
            scope.Write(command)
            #a1, a2 = AmplitudesAndPhases(scope)     # Retake data
            print tab + 'adjusting ch2'
            time.sleep(patience)
            stable = 0
        else :
            stable = 1
    return a1, a2, scale1, scale2

def FgScopeFrequencyScan(fg, scope, freqs, vertical_scale1, vertical_scale2) :
    # Frequencies in Hz
    tab = '\t'
    scale1 = vertical_scale1
    scale2 = vertical_scale2
    raw = array([])
    amp = array([])
    phase = array([])
    print
    if freqs[0] < 20.0 :
        print "Low frequencies have been specified."
        print "Be patient because it will take time for the scope to report valid signals after any change."
    print '\nFrequency, a(pk-pk), a(0), phase: '
    for f in freqs :
        fg.Write('frequency ' + str(f))
        period = 1.0/f
        # At low frequencies, you must wait a long time after changing the frequency on the fg.
        if period > .05 :
            time.sleep(5.0)     # 10 works for samples = 16.  5 works for samples = 4.
        if period > 0.1 :
            time.sleep(10.0)    # sleep some more
        #vertical_scale = 1
        horizontal_scale = period/5.0
        command = 'horiz:scale ' + str(horizontal_scale)    # Reset the horizontal scale to show one cycle
        scope.Write(command)
        time.sleep(0.3)
        #print f, horizontal_scale
        patience = 20.0*period
        a1, a2, scale1, scale2 = AmplitudesAndPhases(scope, scale1, scale2, patience)
        # Determine the phase of ch2 relative to ch1.
        # First, check the phase of the input signal relative to the ttl trigger point.
        #   This should be zero, but for nu , 100 Hz it is not.
        scope.Write('data:source ch1;start 1250;stop 1250;:curve?')
        a0 = float(s.split(scope.Read(), ' ')[1])*scale1*4/100
        r = 2.0*a0/a1
        if abs(r) > 1.0 :
            beta = sign(r)*0.5*pi     # Phase
        else :
            beta = arcsin(r)    # Phase
        # Now get the phase of the ch2 signal
        scope.Write('data:source ch2;start 1250;stop 1250;:curve?')
        a = float(s.split(scope.Read(), ' ')[1])*scale2*4/100
        r = 2.0*a/a2
        if abs(r) > 1.0 :
            alpha = sign(r)*0.5*pi     # Phase
        else :
            alpha = arcsin(r)    # Phase
        alpha = alpha - beta    # Subtract the phase of ch1 from that of ch2 to get the relative phase.
        phase = append(phase, alpha)
        raw = append(raw, a2/a1)
        print tab, f, tab, a2, tab, a, tab, alpha
    ampdb = 20*log10(raw)     # if yaxis = log10
    return ampdb, phase, raw

def FrequencyScanAndPlot(fg, scope, inst, op) :
    freqs, vscale1, vscale2, error = PrepareForFrequencyScan(fg, scope, inst, op)
    if error :
        return
    #amp_theory, phase_theory, log_freq, title_amp, title_phase = TheoreticalResponse(expt, tau, freqs)
    log_amp_expt, phase_expt, amp_expt = FgScopeFrequencyScan(fg, scope, freqs, vscale1, vscale2)
    if op.has_key('xaxis') :
        v = s.strip(op['xaxis'][0]).lower()
        if v == 'log10' :
            xdata = log10(freqs)
            xlabel = 'Log10(Frequency)'
        elif v == 'linear' :
            xdata = freqs
            xlabel = 'Frequency'
    else :
        xdata = log10(freqs)
        xlabel = 'Log10(Frequency)'
    if op.has_key('yaxis') :
        v = s.strip(op['yaxis'][0]).lower()
        if v == 'db' :
            ydata = log_amp_expt
            title_amp = '|A| in dB'
            ylabel = '20Log10(|A|)'
        elif v == 'linear' :
            ydata = amp_expt
            title_amp = '|A|'
            ylabel = '|A|'
    else :
        ydata = log_amp_expt
        title_amp = '|A| in dB'
        ylabel = '20Log10(|A|)'
    phase_over_pi = phase_expt/pi
    title_phase = 'Phase in Units of Pi'
    phase_label = 'Phase in Units of Pi'
    PlotResults(xdata, ydata, phase_over_pi, title_amp, title_phase, xlabel, ylabel, phase_label)
    SaveResults(freqs, amp_expt, phase_expt)

