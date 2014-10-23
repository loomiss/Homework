
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
    parameters_file = 'scan_2_parameters_tek_generic.txt'
    #parameters_file = 'scan_2_parameters_rigol_generic.txt'
    #parameters_file = 'scan_2_parameters_opamp.txt'
    #parameters_file = 'scan_2_parameters_diode.txt'
    #parameters_file = 'scan_2_parameters_bjt_ce_amp.txt'
    #parameters_file = 'scan_2_parameters_bjt_ce_amp_high_freq.txt'
    #parameters_file = 'scan_2_parameters_jfet_cs_amp.txt'
    #parameters_file = 'scan_2_parameters_cable_junction_high_freq.txt'
    #parameters_file = 'scan_2_parameters_lc_filter.txt'
    #parameters_file = 'scan_2_parameters_rlc_with_transformer.txt'
    #parameters_file = 'scan_2_parameters_colpitts.txt'
    inst, op, error, warning = ReadParametersFile(parameters_file, 'scan_2.py')
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
            print 'Only frequency scanning is currently available.'
    else :
        print 'Scan variable not specified. Add the statement "scan variable = frequency" in the operational parameters section.'

# -------------------------------------------------------------------------------
if __name__ == '__main__' :
    Scan()



