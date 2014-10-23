


def PrepareForInputScan(fg, scope, inst, op) :
    # parms is the list of parameters read from the <program name>_commands.txt file.
    # Amplitude is half the pk-pk value, and average is the number of sweeps to average.
    # Creat array of frequencies
    tab = '\t'
    freq_def = 'decadic'    # or linear
    if op.has_key('steps') :
        try:
            steps = int(s.strip(op['steps'][0]))
        except :
            print 'Steps parameter in scan_parameters.txt cannot be evaluated as an integer, so steps = 10.'
            steps = 10
    else :
        steps = 10
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
    period = 1.0/freqs[0]
    vertical_scale2 = float(op['amplitude'][0])/4.0
    if op.has_key('input amplitude') :
        vertical_scale1 = float(op['input amplitude'][0])/4.0
    else :
        vertical_scale1 = vertical_scale2
    horizontal_scale = period/5.0
    #print freqs
    #print period, vertical_scale, horizontal_scale
    # Set the scope
    # First execute the commands from the command file.
    print '\nSend scope commands: '
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
    # Set the function generator
    # First execute the commands from the command file.
    print '\nSend function generator commands: '
    for c in inst['fg']['com'] :
        fg.Write(c)
        print tab + c
    time.sleep(1.0)     # Wait a moment for the instruments to stabilize.
    return freqs, vertical_scale1, vertical_scale2

