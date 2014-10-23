
# Description --------------------------------------------------------------------------------------------------------------
# Read data files and plot with matplotlib.
# Local modules required: plot_base.py, plot_file_read.py
# Global modules required: numpy, matplotlib
#
# Name:        response_plot.py
# Author:      W. Hetherington, Physics, Oregon State University
# Created:     2009/11/08
# Modified:
# Copyright:   (c) 2009
# License:     No restrictions
#---------------------------------------------------------------------------------------------------------------------------

from response_plot_base import *
from response_plot_files import *
from numpy import *

def TransformTodB(x) :
    return 20.0*log10(abs(x))

def Linear(x) :
    return x

def DivideByPi(x) :
    return x/pi

def PowerSpectrum(x, y) :
    samples = len(x)    # 2500 for scope
    halfway = samples/2
    # Multiplying a waveform by a window function is important when the waveform is not exactly periodic
    # over the range, that is when point[0] != point[2499].  Numpy has hanning, blackman, bartlett, hamming and kaiser.
    window = hanning(samples)   # 2500 for scope
    fty = fft.fft(y*window)
    #fty = fft.fft(window)
    n = fty.size
    ftyabs = abs(fty[0:halfway])
    ftydb = 20.0*log10(ftyabs)
    xstep = x[1] - x[0] #float(raw_input('Enter the time per division in seconds, such as 5e-06 : '))   #scope.chan_refs[0].xinc
    print n, xstep
    ftx = fft.fftfreq(n, xstep)[0:halfway]  #/1.0e03    # in kHz
    print ('Note that the frequency axis will be in Hz.')   #kHz.')
    ftmaxindex = ftyabs.argmax()
    ftmax = ftyabs[ftmaxindex]
    print ftmax, ftmaxindex
    t = [ftx, ftydb]    # not ftyabs
    return t

def AmplitudeSpectrum(x, y) :
    samples = len(x)    # 2500 for scope
    halfway = samples/2
    # Multiplying a waveform by a window function is important when the waveform is not exactly periodic
    # over the range, that is when point[0] != point[2499].  Numpy has hanning, blackman, bartlett, hamming and kaiser.
    window = hanning(samples)   # 2500 for scope
    fty = fft.fft(y*window)
    #fty = fft.fft(window)
    n = fty.size
    ftyraw = fty[0:halfway]
    ftyabs = abs(ftyraw)
    #ftydb = 20.0*log10(ftyabs)
    xstep = x[1] - x[0] #float(raw_input('Enter the time per division in seconds, such as 5e-06 : '))   #scope.chan_refs[0].xinc
    print n, xstep
    ftx = fft.fftfreq(n, xstep)[0:halfway]  #/1.0e03    # in kHz
    print ('Note that the frequency axis will be in Hz.')   #kHz.')
    ftmaxindex = ftyabs.argmax()
    ftmax = ftyabs[ftmaxindex]
    print ftmax, ftmaxindex
    t = [ftx, ftyabs]    # not ftyraw, which is complex
    return t

def OscillatorAnalysis(x, y) :
    #if legends :
        #if i >= len(legends) :
            #legends.append('Channel '+str(scope.channels[i]))
        #the_label = legends[i]
    #else :
        #the_label = 'Channel '+str(scope.channels[i])
    fty = fft.fft(y)
    ftyabs = abs(fty[0:1250])
    ftydb = 20.0*log10(ftyabs)
    n = fty.size
    xstep = x[1] - x[0] #float(raw_input('Enter the time per division in seconds, such as 5e-06 : '))   #scope.chan_refs[0].xinc
    print n, xstep
    ftx = fft.fftfreq(n, xstep)[0:1250]/1.0e06    # in MHz
    print ('Note that the frequency axis will be in MHz.')
    ftmaxindex = ftyabs.argmax()
    ftmax = ftyabs[ftmaxindex]
    print ftmax, ftmaxindex
    lorentz = array([])
    freqo = ftx[ftmaxindex]
    qin = raw_input('Enter Q>0 or just press enter to skip:')
    if qin :
        sim = True
        q = float(qin)
    else :
        sim = False
        q = 200
    fwhm = freqo/q/2.0
    alpha = fwhm**2
    for ftfreq in ftx :
        lorentz = append(lorentz, ftmax*alpha/(alpha + (ftfreq - freqo)**2))
    print lorentz.size
    t = [ftx, ftyabs, ftydb]
    if sim :
        t.append(lorentz)
    return t

def TransformDataSetsNew(data_sets, num_graphs, transform_list):
    # Data_set is a list of data from several files, to be processed sequentially.
    # The data from an individual files consists of a list [x, y1, y2, ..., yn]
    # Transform_list is a list of defined functions or python functions without parentheses.
    # Each function is associated with a particular list of data from a file, eg, log10(x), 20*log10(abs(y)), y
    # Examples of functions: min, max, abs, sqrt (from math or numpy modules), log10, ...
    # Invocation examples: TransformDataSets([[[x_values from file 1], [y_values from file 1]], [[x_values from file 2], [y_values from file 2], ...]], [log10, TransformTodB, ...]).
    # Use of the Numpy array structure makes this a simple task.
    # The array returned is a list of [x data, y data] pairs.
    errors = ''
    tdata = []
    flag_osc = False
    for data in data_sets :
        t = []
        for j in range(len(data)) :
            print 'line 93', j, len(data[j])
            if transform_list[j] :
                if transform_list[j] == OscillatorAnalysis :
                    flag_osc = True
                    t = OscillatorAnalysis(data[0], data[j])
                elif transform_list[j] == PowerSpectrum :
                    tf, tp = PowerSpectrum(data[0], data[j])
                    t[0] = transform_list[0](tf)
                    t.append(tp)
                else :
                    td = transform_list[j](data[j])
                    if transform_list[j] == fft.rfft :
                        #td2 = td[0: len(td) - 1]
                        #print len(td)
                        td = td[0 : len(td) - 1]
                        td = append(td, td)
                        print (len(td))
                    t.append(td)    # new array = function(array)
            else :
                t.append(data[j])    # new array = function(array)
        pairwise = []
        for i in range(1, len(t)) :
            pairwise.append([t[0], t[i]])
        tdata.append(pairwise)
        print 'length tdata', len(tdata)

    return tdata, errors

def MakeTransformList(xaxis, yaxis) :
    # xaxis is 'linear' or 'log10'
    # yaxis is a list ['linear', 'linear', ...] or ['db', 'linear', ...]
    x = s.strip(xaxis).lower()
    y = []
    for yax in yaxis :
        y.append(s.strip(yax).lower())
    tlist = []
    if x == 'linear' : tlist.append(Linear)
    elif x == 'log10' : tlist.append(log10)     # Reference to the built-in numpy function log10
    else : tlist.append('')
    for yax in y :
        if yax == 'linear' : tlist.append(Linear)
        elif yax == 'db' : tlist.append(TransformTodB)  # Reference to the locally-defined function TransformTodB
        elif yax == 'log10' : tlist.append(log10)
        elif yax == 'divide_by_pi' : tlist.append(DivideByPi)
        elif yax == 'rfft' : tlist.append(fft.rfft)
        elif yax == 'osc' : tlist.append(OscillatorAnalysis)
        elif yax == 'power' : tlist.append(PowerSpectrum)
        else :
            tlist.append('')
            print 'Unknown transformation requested: ' + yax
    #print tlist
    return tlist

def MakeLabels(xaxis, yaxis) :
    # xaxis is 'linear' or 'log10'
    # yaxis is a list ['linear', 'linear', ...] or ['db', 'linear', ...]
    x = s.strip(xaxis).lower()
    y = []
    for yax in yaxis :
        y.append(s.strip(yax).lower())
    if x == 'linear' : xlabel = 'Frequency'
    elif x == 'log10' : xlabel = 'Log10(Frequency)'
    else : xlabel = 'Unknown'
    ylabels = []
    quants = ['|A|', 'Phase', 'Whatever']
    i = 0
    for yax in y :
        if yax == 'linear' :
            ylabels.append(quants[i])
        elif yax == 'db' : ylabels.append('20 Log10(' + quants[i] + ')')
        elif yax == 'log10' : ylabels.append('Log10(' + quants[i] + ')')
        elif yax == 'divide_by_pi' : ylabels.append(quants[i] + ' (in units of pi)')
        elif yax == 'osc' :
            xlabel = 'Frequency in MHz'
            ylabels = ['|A|', '20 Log10(|A|)', '|A|']
        elif yax == 'power' :
            xlabel = 'Log(Frequency) in Hz'
            ylabels = ['20 Log10(|A|)', '20 Log10(|A|)']
        else : ylabels.append('Unknown')
        i += 1
    return xlabel, ylabels


def PlotFiles(file_list, xaxis='linear', yaxes=['linear','linear'], symbols=['o','','o','o','o'], legend=True, legends=[], title_list=True, x_label=None, y_labels=None) :
    # file_list is a list of file objects to be plotted simultaneously.
    # Transform_list is a list of defined functions or python functions without parentheses.
    # Each function is associated with a particular list of data from a file, eg, log10(x), 20*log10(abs(y)), y
    # Examples of functions: min, max, abs, sqrt (from math or numpy modules), log10, ...
    # Defined functions are: 'power' for a power spectrum, 'divide_by_pi', 'osc' for oscillator analysis.
    # xaxis_def = 'log10', 'linear', or ?, the definition of the xaxis as linear in x data or logarithmic.
    # yaxis_defs = ['linear', 'log'], list of axis definitions, the length of which depends upon the number of plottable quantities.
    # Invocation example: PlotFiles(['a.csv','c.csv'],[log10, TransformTodB, ''], 'log10', ['db', 'linear'])
    # This will the first column of data (x), take log10(x) and 20*log10(abs(y1)) and (y2), and label the xaxis as log10, the y1 axis as db, the y2 axis
    data_files = []
    for f in file_list :
        fili = DataFromFile(f, ',')
        if fili.error :
            print fili.error
            return     # Bail out if something is not quite right.
        data_files.append(fili)   # Assume the data delimiter is ','.
    for g in data_files :
        print g.file_name, len(g.data)
    all_data = []
    for d in data_files :
        all_data.append(d.data)
    print len(all_data[0])
    transform_list = MakeTransformList(xaxis, yaxes)
    print transform_list
    num_graphs =  len(yaxes)      # The number of graphs to be made will be len(td[0]) = len(td[1]) = ...
    td, error = TransformDataSetsNew(all_data, num_graphs, transform_list) # td is an array of [x,y] pairs of data
    #print td
    if error :
        print error
        return
    xlabel, ylabels = MakeLabels(xaxis, yaxes)  # The labels for the x axis and all the possible y axes.
    if x_label :
        xlabel = x_label
    if y_labels :
        ylabels = y_labels
    #print xlabel, ylabels
    if legend :
        if len(legends) :
            labels = legends
        else :
            labels = MakeLegends(data_files)    # Used for the legend
    else : labels = None
    #print labels
    titles = MakeTitles(data_files)     # List of Titles for each plot
    if (title_list == None) | (title_list == False) :
        for i in range(len(titles)) :
            titles[i] = ''
    elif title_list != True :
        titles = title_list
    #symbols = ['o','','o','o','o']      # One symbol for each data set: 'o' is good for data, '' for simulations.
    #print len(td[0])
    #print titles
    #print xlabel
    #print ylabels
    #(num_graphs) : #The number of graphs to be made will be len(td[0]) = len(td[1]) = ..., except when yaxes=['osc']
    num_graphs = len(td[0])
    #if yaxes == ['osc'] :
    #   num_graphs -= 1
    for i in range(num_graphs) :
        gd = []
        for j in range(len(td)) :   # Each graph with have len(td) curves.
            #print num_graphs, i, j
            gd.append(td[j][i])
        #print gd
        DefineFigure(gd, title=titles[i], xlabel=xlabel, ylabel=ylabels[i], legend=labels, symbols=symbols)
    plt.show()

# -----------------------------------------------------------------------

if __name__ == '__main__' :
    #os.chdir('C:\Documents and Settings\instructor\python\expt')
    # Default symbol is 'o' for data.  Other include symbol='' for a simulation.
    run = 11    #9 #6.4    #6.2
    if run == 1:
        symbols = ['o','o','','o','o']      # One symbol for each data set: 'o' is good for data, '' for simulations.
        files_to_plot = ['lp_filter.csv', 'hp_filter.csv']
        # The following functions will be applied to the data
        xaxis = 'log10' # Only linear and log10 are possible currently.
        # For the y axis, the possibilities are 'db', 'linear', log10', 'divide_by_pi'
        yaxes = ['db', 'linear']    # The first set of y values will be transformed to db, the second will be unchanged.  Add to the list if there are more y values.
        PlotFiles(files_to_plot, xaxis=xaxis, yaxes=yaxes, symbols=symbols, legend=False)   # Set legend = True if a legend is desired.
    if run == 1.1:
        symbols = ['o','','','o','o']      # One symbol for each data set: 'o' is good for data, '' for simulations.
        #files_to_plot = ['../response_spectrum/low_pass_f=10Hz-21MHz.csv']
        #files_to_plot = ['../response_spectrum/clip_junction_f=10Hz-23MHz.csv']
        files_to_plot = ['../response_spectrum/low_pass_f=10Hz-21MHz.csv', '../simulate/rclp_48k_1nf.csv']
        # The following functions will be applied to the data
        xaxis = 'log10' # Only linear and log10 are possible currently.
        # For the y axis, the possibilities are 'db', 'linear', log10', 'divide_by_pi'
        yaxes = ['db', 'divide_by_pi']    # The first set of y values will be transformed to db, the second will be unchanged.  Add to the list if there are more y values.
        PlotFiles(files_to_plot, xaxis=xaxis, yaxes=yaxes, symbols=symbols, legend=False)   # Set legend = True if a legend is desired.
    if run == 1.2:
        symbols = ['o','','','o','o']      # One symbol for each data set: 'o' is good for data, '' for simulations.
        #files_to_plot = ['../response_spectrum/low_pass_f=10Hz-21MHz.csv']
        #files_to_plot = ['../response_spectrum/clip_junction_f=10Hz-23MHz.csv']
        files_to_plot = ['../data/rl/RL_Filter_L=(0.8_H,1.1_nF,62.5_Ohm)_response.csv', '../data/rl/RL_Filter_R=5.1k_L=(0.8_H,1.1_nF,62.5_Ohm)_simulation.csv']
        # The following functions will be applied to the data
        xaxis = 'log10' # Only linear and log10 are possible currently.
        # For the y axis, the possibilities are 'db', 'linear', log10', 'divide_by_pi'
        yaxes = ['db', 'divide_by_pi']    # The first set of y values will be transformed to db, the second will be unchanged.  Add to the list if there are more y values.
        PlotFiles(files_to_plot, xaxis=xaxis, yaxes=yaxes, symbols=symbols, legend=False)   # Set legend = True if a legend is desired.
    if run == 1.3:
        symbols = ['o','','','o','o']      # One symbol for each data set: 'o' is good for data, '' for simulations.
        #files_to_plot = ['../response_spectrum/low_pass_f=10Hz-21MHz.csv']
        #files_to_plot = ['../response_spectrum/clip_junction_f=10Hz-23MHz.csv']
        files_to_plot = ['../data/rlc_parallel/R=1100+parallel(L=15e-6,C=1e-9)_response_logfreq=5.6-6.6.csv', '../data/rlc_parallel/R=1100+parallel(L=15e-6,C=1e-9)_simulation_logfreq=5.6-6.6.csv']
        titles = ['R=1100+parallel(L=15e-6,C=1e-9) Amplitude', 'R=1100+parallel(L=15e-6,C=1e-9) Phase']
        legends = ['Experiment', 'Simulation']
        # The following functions will be applied to the data
        xaxis = 'log10' # Only linear and log10 are possible currently.
        # For the y axis, the possibilities are 'db', 'linear', log10', 'divide_by_pi'
        yaxes = ['db', 'divide_by_pi']    # The first set of y values will be transformed to db, the second will be unchanged.  Add to the list if there are more y values.
        PlotFiles(files_to_plot, xaxis=xaxis, x_label=r'Log($\nu$)', yaxes=yaxes, y_labels=None, symbols=symbols, legend=True, legends=legends, title_list=titles)   # Set legend = True if a legend is desired, or False if not, or a list of strings.
    if run == 2:
        symbols = ['o','o','','o','o']      # One symbol for each data set: 'o' is good for data, '' for simulations.
        files_to_plot = ['lp_filter.csv', 'hp_filter.csv', 'lp_rcrc_filter.dat']
        # The following functions will be applied to the data
        xaxis = 'log10' # Only linear and log10 are possible currently.
        # For the y axis, the possibilities are 'db', 'linear', log10', 'divide_by_pi'
        yaxes = ['db', 'divide_by_pi']    # The first set of y values will be transformed to db, the second will be unchanged.  Add to the list if there are more y values.
        titles = ['a', 'b', 'c']
        # Title_list can be either a list of titles you provide, True for automatically-generated titles, or None or False for no titles. Default is True.
        PlotFiles(files_to_plot, xaxis=xaxis, yaxes=yaxes, symbols=symbols, legend=False, title_list=True)   # Set legend = True if a legend is desired.
    if run == 3:
        symbols = ['','o','','o','o']      # One symbol for each data set: 'o' is good for data, '' for simulations.
        files_to_plot = ['10MHz_span=50MHz_center=25MHz.dat']
        # The following functions will be applied to the data
        xaxis = '' # Only linear and log10 are possible currently.  If blank, then linear is assumed.
        # For the y axis, the possibilities are 'db', 'linear', log10', 'divide_by_pi'
        yaxes = ['']    # The first set of y values will be transformed to db, the second will be unchanged.  Add to the list if there are more y values.
        #titles = ['a', 'b', 'c']
        titles = ['Signal in dBm']
        # Title_list can be either a list of titles you provide, True for automatically-generated titles, or None or False for no titles. Default is True.
        PlotFiles(files_to_plot, xaxis=xaxis, yaxes=yaxes, symbols=symbols, legend=False, title_list=True)   # Set legend = True if a legend is desired.
    if run == 4:
        symbols = ['o','','','o','o']      # One symbol for each data set: 'o' is good for data, '' for simulations.
        os.chdir('C:\Documents and Settings\instructor\data\lc')
        files_to_plot = ['lc_15e-7uh_1e-1ohm_24inch_coax_decades=6to7.csv', 'lc_simulation_l=15e-07_r=1e-1_c=18e-11_decades=6to7.csv']
        # The following functions will be applied to the data
        xaxis = 'log10' # Only linear and log10 are possible currently.
        # For the y axis, the possibilities are 'db', 'linear', log10', 'divide_by_pi'
        yaxes = ['db', 'divide_by_pi']    # The first set of y values will be transformed to db, the second will be unchanged.  Add to the list if there are more y values.
        #titles = ['a', 'b', 'c']
        # Title_list can be either a list of titles you provide, True for automatically-generated titles, or None or False for no titles. Default is True.
        PlotFiles(files_to_plot, xaxis=xaxis, yaxes=yaxes, symbols=symbols, legend=False, title_list=True)   # Set legend = True if a legend is desired.
    if run == 5:
        symbols = ['','o','','o','o']      # One symbol for each data set: 'o' is good for data, '' for simulations.
        os.chdir('../data/fpga')
        files_to_plot =['NOV18_FFTDATA_10MhzStripped'] #['NOVSIXTEEN10_100K_131000']
        # The following functions will be applied to the data
        xaxis = 'linear' # Only linear and log10 are possible currently.  If blank, then linear is assumed.
        # For the y axis, the possibilities are 'db', 'linear', log10', 'divide_by_pi' and 'rfft'.
        yaxes = ['linear']    # The first set of y values will be transformed to db, the second will be unchanged.  Add to the list if there are more y values.
        #titles = ['a', 'b', 'c']
        titles = ['Signal in dBm']
        # Title_list can be either a list of titles you provide, True for automatically-generated titles, or None or False for no titles. Default is True.
        PlotFiles(files_to_plot, xaxis=xaxis, yaxes=yaxes, symbols=symbols, legend=False, title_list=True)   # Set legend = True if a legend is desired.
    if run == 6:
        symbols = ['.','.','','o','o']      # One symbol for each data set: 'o' is good for data, '' for simulations.
        #os.chdir('../data/fpga')
        #files_to_plot =['waveform.csv']
        files_to_plot =['../ph411_f10/data/low_pass.csv']
        # The following functions will be applied to the data
        xaxis = 'linear' # Only linear and log10 are possible currently.  If blank, then linear is assumed.
        # For the y axis, the possibilities are 'db', 'linear', log10', 'divide_by_pi' and 'rfft'.
        yaxes = ['linear', 'linear']    # The first set of y values will be transformed to db, the second will be unchanged.  Add to the list if there are more y values.
        titles = ['Channel 1', 'Channel 2']
        # Title_list can be either a list of titles you provide, True for automatically-generated titles, or None or False for no titles. Default is True.
        PlotFiles(files_to_plot, xaxis=xaxis, yaxes=yaxes, symbols=symbols, legend=False, title_list=titles, x_label='Time (s)', y_labels=['Signal (Volts)', 'Signal (Volts)'])   # Set legend = True if a legend is desired.
    if run == 6.1:
        symbols = ['','o','','o','o']      # One symbol for each data set: 'o' is good for data, '' for simulations.
        os.chdir('../ph411_f10/data')
        #files_to_plot =['low_pass.csv']
        files_to_plot =['low_pass_square_10kHz_50us.csv']
        # The following functions will be applied to the data
        xaxis = 'log10' # Only linear and log10 are possible currently.  If blank, then linear is assumed.  Ignored if yaxes =['osc']
        # For the y axis, the possibilities are 'db', 'linear', log10', 'divide_by_pi', 'rfft' and 'osc' for oscillator analysis.
        yaxes = ['power', 'power']    # The first set of y values will be tranformed by fft to power spectrum.  Add to the list if there are more y values.
        titles = ['Power Spectrum in dB', 'Power Spectrum in dB']
        #titles = None
        # Title_list can be either a list of titles you provide, True for automatically-generated titles, or None or False for no titles. Default is True.
        PlotFiles(files_to_plot, xaxis=xaxis, yaxes=yaxes, symbols=symbols, legend=False, title_list=titles)   # Set legend = True if a legend is desired.
    if run == 6.2:
        symbols = ['','o','','o','o']      # One symbol for each data set: 'o' is good for data, '' for simulations.
        os.chdir('../data/rlc_parallel/time_domain')
        #files_to_plot =['low_pass.csv']
        #files_to_plot =['transient_response_parallel_L=10uH_C=940pF_500ns-div_20MHzBWoff.csv']
        #files_to_plot =['transient_response_parallel_L=10uH_C=940pF_1us-div.csv']
        #files_to_plot =['transient_response_parallel_L=10uH_C=940pF_2.5us-div_20MHzBWon.csv']
        files_to_plot =['transient_response_parallel_L=10uH_C=940pF_2.5us-div_20MHzBWoff.csv']
        # The following functions will be applied to the data
        xaxis = 'log10' # Only linear and log10 are possible currently.  If blank, then linear is assumed.  Ignored if yaxes =['osc']
        # For the y axis, the possibilities are 'db', 'linear', log10', 'divide_by_pi', 'rfft' and 'osc' for oscillator analysis.
        yaxes = ['power', 'power']    # The first set of y values will be tranformed by fft to power spectrum.  Add to the list if there are more y values.
        titles = ['Power Spectrum in dB', 'Transient Response Parallel L=10uH C=940pF Power Spectrum']
        #titles = None
        # Title_list can be either a list of titles you provide, True for automatically-generated titles, or None or False for no titles. Default is True.
        PlotFiles(files_to_plot, xaxis=xaxis, yaxes=yaxes, symbols=symbols, x_label=r'Log($\nu$)', legend=False, title_list=titles)   # Set legend = True if a legend is desired.
    if run == 6.3:
        symbols = ['','','','o','o']      # One symbol for each data set: 'o' is good for data, '' for simulations.
        os.chdir('../data/nonlinear_divider')
        #files_to_plot =['low_pass.csv']
        #files_to_plot =['transient_response_parallel_L=10uH_C=940pF_500ns-div_20MHzBWoff.csv']
        #files_to_plot =['transient_response_parallel_L=10uH_C=940pF_1us-div.csv']
        #files_to_plot =['transient_response_parallel_L=10uH_C=940pF_2.5us-div_20MHzBWon.csv']
        files_to_plot =['nonlinear_response_of_91+91_ohm_divider_with_bidirectional_diode_pair_parallel_to_upper_resistor_1khz_sine_2500_points_over_100_cycles_time_data.csv',
        'nonlinear_response_of_91+91_ohm_divider_with_one_diode_parallel_to_upper_resistor_1khz_sine_2500_points_over_100_cycles_time_data.csv']
        legends = ['Bidirectional', 'Unidirectional']
        #files_to_plot = ['nonlinear_response_of_91+91_ohm_divider_with_one_diode_parallel_to_upper_resistor_1khz_sine_2500_points_over_100_cycles_time_data.csv']
        #files_to_plot = ['diode_yt.csv']
        # The following functions will be applied to the data
        xaxis = 'linear' # Only linear and log10 are possible currently.  If blank, then linear is assumed.  Ignored if yaxes =['osc']
        # For the y axis, the possibilities are 'db', 'linear', log10', 'divide_by_pi', 'rfft' and 'osc' for oscillator analysis.
        yaxes = ['power', 'power']    # The first set of y values will be tranformed by fft to power spectrum.  Add to the list if there are more y values.
        titles = ['Power Spectrum in dB', 'Power Spectrum of Nonlinear Response of a Divider'+' with a Bidirectional Diode Pair\nParallel To Upper Resistor'+' (1 kHz Sine, 2500 Points Over 100 Cycles)']
        #titles = ['Power Spectrum in dB', 'Power Spectrum of Nonlinear Response of a Divider'+' with One Diode \nParallel To Upper Resistor'+' (1 kHz Sine, 2500 Points Over 100 Cycles)']
        #titles = None
        # Title_list can be either a list of titles you provide, True for automatically-generated titles, or None or False for no titles. Default is True.
        PlotFiles(files_to_plot, xaxis=xaxis, yaxes=yaxes, symbols=symbols, x_label=r'Frequency in Hz', legend=True, legends=legends, title_list=titles)   # Set legend = True if a legend is desired.
    if run == 6.4:
        symbols = ['','o','','o','o']      # One symbol for each data set: 'o' is good for data, '' for simulations.
        os.chdir('../scope/temp/')
        files_to_plot = ['2n4123_ce_amp_zin=1kohm+220nf_rc=1kohm_vcc=12_vc=6_10khz_100cycles_2500points.csv']
        #files_to_plot = ['2n4123_bjt_ce_amp_with_1kohm+220nf_zin_10khz_100cycles.csv']
        # The following functions will be applied to the data
        xaxis = 'log10' # Only linear and log10 are possible currently.  If blank, then linear is assumed.  Ignored if yaxes =['osc']
        # For the y axis, the possibilities are 'db', 'linear', log10', 'divide_by_pi', 'rfft' and 'osc' for oscillator analysis.
        yaxes = ['power', 'power']    # The first set of y values will be tranformed by fft to power spectrum.  Add to the list if there are more y values.
        #titles = ['Power Spectrum in dB', '2N4123 NPN Common Emitter Amplifier\n 1 k$\Omega$ + 220 nF $Z_{in}$, 100 cycles']
        titles = ['Power Spectrum in dB for 10 kHz Input Signal', 'Power Spectrum in dB for 2N4123 Common Emitter Amplifier\n$Z_{in}=1$ k$\Omega$ + 220 nF, $R_c=1$ k$\Omega$, $V_{cc}=12$ V, $V_c=6$ V, 10 kHz Sine, 100 Cycles, 2500 Points']
        # Title_list can be either a list of titles you provide, True for automatically-generated titles, or None or False for no titles. Default is True.
        PlotFiles(files_to_plot, xaxis=xaxis, yaxes=yaxes, symbols=symbols, x_label=r'Log($\nu$)', legend=False, title_list=titles)   # Set legend = True if a legend is desired.
    if run == 7:
        symbols = ['','','','o','o']      # One symbol for each data set: 'o' is good for data, '' for simulations.
        #os.chdir('../data/fpga')
        files_to_plot =['xy.csv']
        # The following functions will be applied to the data
        xaxis = 'linear' # Only linear and log10 are possible currently.  If blank, then linear is assumed.
        # For the y axis, the possibilities are 'db', 'linear', log10', 'divide_by_pi' and 'rfft'.
        yaxes = ['linear']    # The first set of y values will be transformed to db, the second will be unchanged.  Add to the list if there are more y values.
        titles = ['Channel 2 vs. Channel 1']
        # Title_list can be either a list of titles you provide, True for automatically-generated titles, or None or False for no titles. Default is True.
        # You can override the default horizontal and verical axis labels using:
        #  x_labels='something'
        #  y_labels=['first y axis', 'second y axis', 'third y axis', ... ]
        #  These are optional keywords.
        PlotFiles(files_to_plot, xaxis=xaxis, yaxes=yaxes, symbols=symbols, legend=False, title_list=titles, x_label = 'horizontal', y_labels=['vertical'])   # Set legend = True if a legend is desired.
    if run == 8:
        symbols = ['','o','','o','o']      # One symbol for each data set: 'o' is good for data, '' for simulations.
        #os.chdir('../data/fpga')
        files_to_plot =['paradigms_simulation_inductor_with_resistance.csv', 'paradigms_real_inductor.csv']
        # The following functions will be applied to the data
        xaxis = 'log10' # Only linear and log10 are possible currently.  If blank, then linear is assumed.
        # For the y axis, the possibilities are 'db', 'linear', log10', 'divide_by_pi' and 'rfft'.
        yaxes = ['db', 'divide_by_py']    # The first set of y values will be transformed to db, the second will be unchanged.  Add to the list if there are more y values.
        #titles = ['Channel 1', 'Channel 2']
        titles = None
        # Title_list can be either a list of titles you provide, True for automatically-generated titles, or None or False for no titles. Default is True.
        PlotFiles(files_to_plot, xaxis=xaxis, yaxes=yaxes, symbols=symbols, legend=False, title_list=titles)   # Set legend = True if a legend is desired.
    if run == 9:
        symbols = ['','o','','o','o']      # One symbol for each data set: 'o' is good for data, '' for simulations.
        #os.chdir('../../../data/jfet/oscillator')
        #os.chdir('../scope/temp/colpitts/22MHz')
        #os.chdir('../scope/temp/colpitts/170MHz')
        os.chdir('../scope/temp/colpitts/240MHz')
        #os.chdir('../scope/temp/crystal/20MHz')
        #files_to_plot =['jfet_17_MHz_oscillator_5us_per_division_average=128_vpp=425mV.csv']
        #files_to_plot =['waveform_data_2.5us_per_div.csv']
        #files_to_plot =['waveform_170_cycles.csv']
        files_to_plot =['waveform_600_cycles.csv']
        # The following functions will be applied to the data
        xaxis = 'log10' # Only linear and log10 are possible currently.  If blank, then linear is assumed.  Ignored if yaxes =['osc']
        # For the y axis, the possibilities are 'db', 'linear', log10', 'divide_by_pi', 'rfft' and 'osc' for oscillator analysis.
        yaxes = ['osc']    # The first set of y values will be tranformed by fft to power spectrum.  Add to the list if there are more y values.
        titles = ['Spectrum', 'Power Spectrum in dB', 'Lorentzian Simulation']
        #titles = None
        # Title_list can be either a list of titles you provide, True for automatically-generated titles, or None or False for no titles. Default is True.
        PlotFiles(files_to_plot, xaxis=xaxis, yaxes=yaxes, symbols=symbols, legend=False, title_list=titles)   # Set legend = True if a legend is desired.
    if run == 10:
        symbols = ['','o','','o','o']      # One symbol for each data set: 'o' is good for data, '' for simulations.
        os.chdir('../data/rlc_parallel/freq_domain')
        files_to_plot =['R=1100+parallel(L=15e-6,C=1e-9)_response_logfreq=5.6-6.6.csv']
        # The following functions will be applied to the data
        xaxis = 'log10' # Only linear and log10 are possible currently.  If blank, then linear is assumed.  Ignored if yaxes =['osc']
        # For the y axis, the possibilities are 'db', 'linear', log10', 'divide_by_pi', 'rfft' and 'osc' for oscillator analysis.
        yaxes = ['db', 'osc']    # The first set of y values will be tranformed by fft to power spectrum.  Add to the list if there are more y values.
        titles = ['Spectrum', 'Power Spectrum in dB', 'Lorentzian Simulation']
        #titles = None
        # Title_list can be either a list of titles you provide, True for automatically-generated titles, or None or False for no titles. Default is True.
        PlotFiles(files_to_plot, xaxis=xaxis, yaxes=yaxes, symbols=symbols, legend=False, title_list=titles)   # Set legend = True if a legend is desired.
    if run == 11:
        symbols = ['','','','o','o']      # One symbol for each data set: 'o' is good for data, '' for simulations.
        os.chdir('../scope')
        #files_to_plot = ['temp/colpitts/240MHz/50_waveforms_appended_each_240_cycles.csv']
        files_to_plot = ['extended.csv']
        # The following functions will be applied to the data
        xaxis = 'log10' # Only linear and log10 are possible currently.  If blank, then linear is assumed.  Ignored if yaxes =['osc']
        # For the y axis, the possibilities are 'db', 'linear', log10', 'divide_by_pi', 'rfft' and 'osc' for oscillator analysis.
        yaxes = ['power', 'power']    # The first set of y values will be tranformed by fft to power spectrum.  Add to the list if there are more y values.
        titles = ['Power Spectrum in dB', 'whatever']
        #titles = None
        # Title_list can be either a list of titles you provide, True for automatically-generated titles, or None or False for no titles. Default is True.
        PlotFiles(files_to_plot, xaxis=xaxis, yaxes=yaxes, symbols=symbols, legend=False, title_list=titles)   # Set legend = True if a legend is desired.



