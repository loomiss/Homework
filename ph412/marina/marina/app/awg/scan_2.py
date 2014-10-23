
# Requires the following modules in the current directory: tek.py, scan_2_instruments.py, scan_2_frequency.py, scan_2_io.py, scan_2_plot.py.
# Requires the following global modules: pyVisa, matplotlib (pylab), scipy, numpy
# The prefered widget set is wx and wxPython.

from scan_2_instruments import *
from scan_2_frequency import *
from scan_2_io import *

def Scan() :
    #FGScopeScan('C031180')
    #fg, scope = InitializeDevices('C031180', 'C055976')
    #fg, scope = FindDevices('C031180', 'C055976')

    #inst, op, error, warning = ReadParametersFile('scan_2_parameters.txt', 'scan_2.py')
    #inst, op, error, warning = ReadParametersFile('scan_2_parameters_bjt_ce_amplifier.txt', 'scan_2.py')
    #inst, op, error, warning = ReadParametersFile('scan_2_parameters_jfet_cd_amplifier.txt', 'scan_2.py')
    inst, op, error, warning = ReadParametersFile('scan_2_parameters_generic.txt', 'scan_2.py')
    if error : print error
    if warning : print warning
    #print inst
    #print op
    fg, error = FindTekInstrument(inst['fg']['id'])
    scope, error = FindTekInstrument(inst['scope']['id'])
    if op.has_key('scan variable') :
        if op['scan variable'][0] == 'frequency' :
            FrequencyScanAndPlot(fg, scope, inst, op)
    else :
        print 'Scan variable not specified. Frequency is assumed.'
        FrequencyScanAndPlot(fg, scope, inst, op)

# -------------------------------------------------------------------------------
if __name__ == '__main__' :
    Scan()



