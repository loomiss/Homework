
import matplotlib
try:
    import wx
    matplotlib.use('WXAgg') # The recommended way to use wx is with the WXAgg backend. 
except :
    print 'wx not found.'
#from matplotlib.figure import Figure
from matplotlib import pyplot as plt


def DefineFigure(x, y_sets, grid=True, title=None, legends=None, xlabel=None, ylabel=None, symbol='o') :
    # X must be a single array for the x axis.
    # Y must be an array of y arrays.
    f = plt.figure()
    sb = f.add_subplot(111)
    for i in range(len(y_sets)) :
        if legends :
            label_string = legends[i]
        else :
            label_string = ''
        sb.plot(x, y_sets[i], symbol, label=label_string)
    if xlabel : plt.xlabel(xlabel)
    if ylabel : plt.ylabel(ylabel)
    if legends : sb.legend()
    if grid : sb.grid()
    if title : plt.title(title)
    #if legend: sb.legend()
    return

def PlotResults(log_freq, amp_expt, phase_expt, title_amp, title_phase, xlabel, ylabel1, ylabel2) :
    title1 = title_amp
    title2 = title_phase
    #xlabel = 'Log(frequency)'
    #ylabel1 = '20Log|A|'
    #ylabel2 = 'Phase'
    labels = []         # no legends
    DefineFigure(log_freq, [amp_expt], grid=True, title=title1, xlabel=xlabel, ylabel=ylabel1, legends=labels)
    DefineFigure(log_freq, [phase_expt], grid=True, title=title2, xlabel=xlabel, ylabel=ylabel2, legends=labels)
    plt.show()

    #plot(log_freq, amp_expt, 'o', label='Experiment')
    #legend()
    #xlabel('log(frequency (Hz))')
    #ylabel('20*log10(|a|)')
    #title(title_amp)
    #grid(True)
    #show()
    ##close()
    #plot(log_freq, phase_expt, 'o', label = 'Experiment')
    ##legend()
    #xlabel('log(frequency (Hz))')
    #ylabel('Phase in units of pi')
    #title(title_phase)
    #grid(True)
    #show()
    #q = raw_input('Enter enter:')
    #close()

