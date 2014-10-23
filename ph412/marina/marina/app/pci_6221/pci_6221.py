
# Description --------------------------------------------------------------------------------------------------------------

#test module

#---------------------------------------------------------------------------------------------------------------------------

import wx       #wx import is required to inherit from wx.Panel.

NAME = "PCI 6221"   #Put the name of your tab here.
DEFAULT_COLOR = [200, 200, 200]

required_modules = ['nidaqmx', 'ain_nidaqmx', "datetime"]


class Tab(wx.Panel):
    def __init__(self, parent, dock, name = NAME, bkg_color = DEFAULT_COLOR):
        """
        @param parent: The parent frame of the Tab object.
        @type parent: wx.Frame object
        
        @param dock: The Master object.
        @type dock: dock.Master object
        
        @param name: The name of the Tab object.
        @type name: string
        
        @param bkg_color: The color of the Tab. [Red, Green, Blue]
        @type bkg_color: list
        """
        super(Tab,  self).__init__(parent, style=wx.RAISED_BORDER)
        self.color = wx.Colour(bkg_color[0],  bkg_color[1],  bkg_color[2])
        self.SetBackgroundColour(self.color)
        self.dock = dock     
        self.parent = parent
        self.name = name
        self.dock = dock
        self.wx = wx
        self.dt = self.dock.GetSystemModule("datetime")
        self.version = '1'
        self.content = 'This module establishes communication with an NI PCI-6221 and read analog input signals.'
        self.about = "Module: pci_6221\n" \
        + "Purpose: Basic NI PCI-6221 communication.\n"\
        + "Authors:\t W. Hetherington\n" \
        + "Created:\t 2011/5/10\n" \
        + "Copyright:\t (c) 2011\n" \
        + "License:\t No restrictions\n"
        self.active_scope = ' '    # name of selected scope
        self.scope_list = []    # list of names
        self.scopes = {}        # (name : handle ) pairs
        self.help = 'pci_6221_help.txt'
        self.save_file = 'data.csv'
        self.save_directory = 'data'
        
        self.DefControls()
        self.MakeControls()
        self.PostCreationConfigure()
        
        
    def SetName(self, name):
        """
        Changed the name of the Tab object.
        
        @param name: The new name of the Tab object.
        @type name: string
        """
        self.name = name
        
    
    def GetName(self):
        """
        Returns The name of the Tab object.
        
        @return: The Tab name.
        """
        return self.name
        
    def GetParent(self):
        """
        Retrieves the parent frame for the Tab object.
        
        @return: Parent wx.Frame object
        """
        return self.parent
        
    def GetDock(self):
        """
        Retrieves the Master object.
        
        @return: dock.Master object
        """
        return self.dock
        
    def DefControls(self):
        # Define the controls.  The order in which they are defined determines the placement on the grid.
        self.controls = {}
        self.ctl_count = 0
        self.DefineControl('setup', {'format':'control_2', 'tab':'yes', 'rows':4, 'columns':4})
        self.DefineControl('find_devices', {'type':'text_and_button','dimensions':[100,70],'label':'NIDAQmx -Compatible\nDevices Found','button_label':'Find Instruments','function':self.FindDevices})
        self.DefineControl('select_device', {'type':'combo_box', 'dimensions':[150,25],'label':'Select Device', 'function':self.OnSelectDevice})
        self.DefineControl('device_parameters', {'type':'text_and_button','dimensions':[200,70],'label':'Selected Device Parameters','button_label':'Get Parameters', 'function':self.DeviceParameters})
        self.DefineControl('channels', {'type':'text_area', 'dimensions':[100, 30], 'read_only':False, 'scroll':False, 'multiline':False, 'label':'Specify Analog Input Channel\n\t\t(0-15)'})
        self.DefineControl('sample_rate', {'type':'text_area', 'dimensions':[100, 30], 'read_only':False, 'scroll':False, 'multiline':False, 'label':'Specify Sample Rate\n(samples/second)'})
        self.DefineControl('samples', {'type':'text_area', 'dimensions':[100, 30], 'read_only':False, 'scroll':False, 'multiline':False, 'label':'Specify Number of Samples\n\t to Acquire'})
        self.DefineControl('adc_range', {'type':'text_area', 'dimensions':[100, 30], 'read_only':False, 'scroll':False, 'multiline':False, 'label':'Specify Analog Input Range\n(2, 5, 10, assumed bipolar)'})
        self.DefineControl('frequency', {'type':'text_area', 'dimensions':[100, 30], 'read_only':False, 'scroll':False, 'multiline':False, 'label':'Input Signal Frequency\n(used only for the plot title)'})
        self.DefineControl('button_block', {'type':'four_buttons_square', 'label_1':'Acquire and Plot', 'function_1':self.OnAcquire, 'label_2':'Autocorrelation', 'function_2':self.OnAutocorrelate, 'label_3':'Synchronous Detection', 'function_3':self.OnSynchronous, 'label_4':'Reset Device', 'function_4':self.OnResetDevice})
        self.DefineControl('save_button', {'type':'button', 'label':'Save File', 'function':self.OnSave})
        self.DefineControl('about_button', {'type':'button', 'label':'About This Module', 'function':self.OnAbout})
        self.DefineControl('help_button', {'type':'button', 'label':'Help', 'function':self.OnHelp})

    def DefineControl(self, ctl_name, c) :
        if ctl_name.lower() != 'setup' :
            c['order'] = self.ctl_count
            self.ctl_count += 1
        self.controls[ctl_name] = c

    def PostCreationConfigure(self) :
        # Label some system or tabbed modules which will be used.
        #self.wd = self.dock.system_modules['wx.lib.dialogs']    # This is a different module?
        
        self.wd = self.dock.GetSystemModule("wx.lib.dialogs")
        self.mx = self.dock.GetSystemModule('nidaqmx')
        self.np = self.dock.GetSystemModule('numpy')
        # Define the control boxes AFTER the controls have been created.
        self.find_devices_box = self.controls['find_devices']
        self.select_device_box = self.controls['select_device']
        self.parameters_box = self.controls['device_parameters']
        self.channels_box = self.controls['channels']
        self.sample_rate_box = self.controls['sample_rate']
        self.samples_box = self.controls['samples']
        self.adc_range_box = self.controls['adc_range']
        self.frequency_box = self.controls['frequency']
        # Refer to attributes in another module object which is an attribute of the associated tab.  Tricky.
        self.simple = self.dock.GetSystemModule('ain_nidaqmx').Simple
        # Default parameters
        self.ain_channel = 0
        self.channels_box.SetValue(str(self.ain_channel))
        self.sample_rate = 200000    #float(self.tab.controls['sample_rate'].GetValue())
        self.sample_rate_box.SetValue(str(self.sample_rate))
        self.samples = 10000    #int(self.tab.controls['samples'].GetValue())
        self.samples_box.SetValue(str(self.samples))
        self.adc_range = 5.0    #float(self.tab.controls['adc_range'].GetValue())
        self.adc_range_box.SetValue(str(self.adc_range))
        self.applied_freq = 10000    #int(self.tab.controls['frequency'].GetValue())
        self.frequency_box.SetValue(str(self.applied_freq))


    def FindDevices(self, event) :
        #the_box = self.dock.modules[self.name]['find_instruments']
        message = ''
        #scope_list = []
        #self.scopes = {}
        #try :
        dll, message = self.mx.LoadDLL()
        if message :
            print message
            return
        f = self.mx.TranslateDAQmxFunctions(dll)
        self.devices = []
        devices = self.mx.FindDevices(f)    # Returns only one label if one 6221 is present.
        self.select_device_box.Append(devices)
        self.devices.append(f)    # Assuming only one device.
        self.find_devices_box.SetValue(devices)
        self.active_device = f        # Assuming only one device is present and make i the active device.
        self.device = devices    # only a string
        #except :
            #message = 'Find NI-DAQmx compatible device error.\nMissing import?'
            #self.find_devices_box.SetValue(message)

    def OnSelectDevice(self, event):
        self.selected_device_identity = self.select_device_box.GetCurrentSelection()
        self.active_device = self.devices[self.selected_device_identity]
        #print self.active_device
        #self.waveforms_selected_scope.SetValue(self.active_scope)

    def OnAbout(self, event):
        #d = self.wx.MessageDialog( self.dock.modules[self.name]['tab'], self.about, "About Scope", self.wx.ICON_INFORMATION)  # Create a message dialog box
        #print self.name
        #print self.dock.tabs[self.name].tab
        d = self.wx.MessageDialog( self.dock.tab.tab, self.about, "About Scope", self.wx.ICON_INFORMATION)  # Create a message dialog box
        d.ShowModal() # Show it.
        d.Destroy() # Destroy it when finished.

    def OnHelp(self, event):
        #d = self.wx.MessageDialog( self.dock.modules[self.name]['tab'], self.about, "About Scope", self.wx.ICON_INFORMATION)  # Create a message dialog box
        try :
            help = self.dock.dirs['help'] + '/' + self.help
            f = open(help)
            help_caption = self.help
        except :
            help = self.dock.dirs['help'] + '/' + 'generic_help.txt'
            f = open(help)
            help_caption = 'generic_help.txt'
        help_me = f.read()
        f.close()
        #d = self.wx.MessageDialog( self.dock.tabs[self.name].tab, help_me, "Scope Help", self.wx.ICON_INFORMATION)  # Create a message dialog box
        d = self.wd.ScrolledMessageDialog(self.dock.tab.tab, help_me, caption=help_caption, pos=(100,100), size=(800,500))#, style=self.wx.HSCROLL)
        d.ShowModal() # Show it.
        d.Destroy() # Destroy it when finished.

    def DeviceParameters(self, event) :
        self.parameters_box.SetValue('Working ... \n')
        message = ''
        message = self.mx.GetDeviceParameters(self.active_device)
        self.parameters_box.SetValue(message)
        return

    def OnAcquire(self, event) :
        self.ain_channel = int(self.channels_box.GetValue())
        self.sample_rate = float(self.sample_rate_box.GetValue())
        self.samples = int(self.samples_box.GetValue())
        adc_range = float(self.adc_range_box.GetValue())
        self.applied_freq = int(self.frequency_box.GetValue())
        # Call to simple returns [[t, signal], [freq, power]] and graphing lables, which might be useful when saving a file.
        self.data_arrays, self.graph_labels = self.simple(self, self.device, self.active_device, self.ain_channel, self.sample_rate, self.samples, adc_range, self.applied_freq)
        self.date = self.dt.now().isoformat()

    def OnAutocorrelate(self, event) :
        corr_full = self.np.correlate(self.data_arrays[0][1], self.data_arrays[0][1], mode='full')
        corr = corr_full[len(corr_full)/2 :]
        points = len(self.data_arrays[0][0])
        index_array = self.np.arange(points, dtype=float)    #[:-1]    # Remove troublesome last point.
        norm = float(points)/(float(points) - index_array + 4.)
        normalized_corr = norm * corr    #[:-1]    # Remove troublesome last point.
        #print norm
        auto_arrays = [[self.data_arrays[0][0], corr], [self.data_arrays[0][0], normalized_corr]]
        frame_title = 'Autocorrelation'
        xlabels = ['Time in Seconds', 'Time in Seconds']
        ylabels = ['Amplitude', 'Amplitude']
        titles = ['Autocorrelation: '+str(self.applied_freq/1000)+' kHz, '+str(int(self.sample_rate)/1000)+' kSPS, '+str(self.samples/1000)+' kSamples']
        titles.append('Normalized Autocorrelation: '+str(self.applied_freq/1000)+' kHz, '+str(int(self.sample_rate)/1000)+' kSPS, '+str(self.samples/1000)+' kSamples')
        grids = [True, True]
        tab_names = ['Channel '+str(self.ain_channel)+' Autocorrelation', 'Channel '+str(self.ain_channel)+' Normalized Autocorrelation']
        b = self.dock.system_modules['notebook_plots_base']
        g = self.dock.system_modules['notebook_plots_graph']
        pf = b.PlotFrame(title=frame_title, size=(800,700))
        for i in range(len(auto_arrays)) :
            print len(auto_arrays[i][0]), len(auto_arrays[i][1])
            p = g.Graph('plot', [auto_arrays[i]], symbols=['b','g'], grid=grids[i], title = titles[i], titlesize=18,\
                background='w', xlabel=xlabels[i], ylabel=ylabels[i], labelsize=16, ticklabelsize=12, customize=None)
            g.DefineTab(pf, [p], name=tab_names[i])
        pf.Show()
        return

    def OnSynchronous(self, event) :
        return

    def OnResetDevice(self, event) :
        self.mx.ResetDevice(self.active_device, self.device)
        print self.device, self.active_device

    def OnSave(self, event) :
        d = self.wx.FileDialog(self.tab.frame, 'Save File', self.save_directory, self.save_file, '*', self.wx.FD_SAVE | self.wx.FD_OVERWRITE_PROMPT, self.wx.DefaultPosition)
        if d.ShowModal() == self.wx.ID_OK : # Show it.
            self.save_directory = d.GetDirectory()
            self.save_file = d.GetFilename()
            self.save_path = d.GetPath()
            o = open(self.save_path, 'w')
            header = '# ' + self.date + '\n'
            header += '# Acquired by pci6221.py\n'
            for key in self.graph_labels :
                header += '# ' + key + '\n'
                for i in range(len(self.graph_labels[key])) :
                    header += '#\t' + self.graph_labels[key][i] + '\n'
            header += '\n# Begin data: time '
            for i in range(1, len(self.data_arrays[0])) :
                header += 'signal, '
            header += '\n'
            o.write(header)
            #print 'j : ', len(self.data_arrays)
            #print 'k : ', len(self.data_arrays[0])
            #print 'i : ', len(self.data_arrays[0][0])
            for i in range(len(self.data_arrays[0][0])) :
                stuff = ''
                for k in range(len(self.data_arrays[0])) :
                        stuff += str(self.data_arrays[0][k][i]) + ', '
                stuff = stuff[:-2] + '\n'
                o.write(stuff)
            #for i in range(len(self.data_arrays[0][0])) :
                #stuff = ''
                #for j in range(len(self.data_arrays)) :
                    #for k in range(len(self.data_arrays[0])) :
                        #try :
                            #stuff += str(self.data_arrays[k][j][i]) + ', '
                        #except :
                            #pass
                #stuff = stuff[:-2] + '\n'
                #o.write(stuff)
            o.close()
        d.Destroy() # Destroy it when finished.
        
    def MakeControls(self) :
        rows = self.controls['setup']['rows']
        columns = self.controls['setup']['columns']
        print '\t\tCreate controls for this tab using sizer of ' +  str(rows) + ' rows by ' + str(columns) + ' columns:'
        sizer = self.wx.FlexGridSizer(rows,columns,5,5) #layout grid size (rows, cols, horiz. gap, vert. gap)

        # Construct the control in the order specified by the 'order' key.
        control_list = range(len(self.controls)-1)
        for key in self.controls:
            if key != 'setup' :
                try :
                    control_list[self.controls[key]['order']] = key    # Creates an ordered list of control labels.
                except :
                    self.error = 'Error in controls list of module ' + self.name + '.  ' + 'They must be ordered from zero up.'
                    print self.error
                    return self.error

        self.error = self.dock.mc.TranslateControls(self, sizer, control_list)
        self.SetSizer(sizer)
        return self.error

# The setup routine must be in each application module. --------------------------------------------

def Setup(dock, parent,  name = NAME,  color = DEFAULT_COLOR):
    """
    Creates the Tab object and passes a handle to the Master object to it.
    
    @param dock: The Master object.
    @type dock: dock.Master object
    
    @param parent: The parent frame of the tab.
    @type parent: wx.Frame object
    
    @param name: The name of the tab. It will be displayed on the tab.
    @type name: string
    
    @param color: The color of the tab. [Red, Green, Blue]
    @type color: list
    
    @return: The Tab object.
    """
    object = Tab(parent, dock,  name,  color)
    return object

# Optional test routines ---------------------------------------------------------------------------

def Test() :
    print 'This is not the module you want.  Execute control.py'

#---------------------------------------------------------------------------------------------------------------------------

#  Execute
if __name__ == '__main__':
    Test()



