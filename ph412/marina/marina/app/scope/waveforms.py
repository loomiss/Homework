import wx       #wx import is required to inherit from wx.Panel.
import csv

NAME = "Waveforms"   #Put the name of your tab here.
DEFAULT_COLOR = [200, 200, 200]

required_modules = ['visa_comm', 'notebook_plots_base', 'notebook_plots_graph','wx.lib.dialogs']
required_modules.extend(['response_plot_files', 'response_plot', 'csv'])


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
        self.wx = wx
        self.version = '1'
        self.content = 'This module will acquire waveforms from a specified oscilloscope. The module tek_scopes is required.'
        self.about = "Module: waveforms \n" \
            + "Purpose: Basic Tektronix TDS1012B waveform acquisition.\n"\
            + "Authors:\t W. Hetherington\n" \
            + "Created:\t 2011/4/23, 2011/10/26\n" \
            + "Copyright:\t (c) 2011\n" \
            + "License:\t No restrictions\n"
        self.this_dir = 'app/scope'
        self.help = 'waveforms_help.txt'
        self.save_file = 'data.csv'
        self.save_directory = 'data'
        # Define the controls.  The order in which they are defined determines the placement on the grid.
        self.controls = {}
        self.ctl_count = 0
        
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
        self.DefineControl('setup', {'format':'control_2', 'tab':'yes', 'rows':4, 'columns':3})
        self.DefineControl('select_device', {'type':'combo_box', 'dimensions':[150,25],'label':'Select Oscilloscope', 'function':self.OnSelectDevice})
        self.DefineControl('channels',  {'type':'text_and_button','dimensions':[100,30],'label':'Channels to Acquire','button_label':'Acquire','function':self.AcquireWaveforms})
        self.DefineControl('blank_1', {'type':'blank'})
        self.DefineControl('simple_plot_buttons', {'type':'two_buttons_vertical', 'label_1':'Plot Channels(t)', 'function_1':self.OnPlotChannels, \
            'label_2':'Plot XY Mode', 'function_2':self.OnPlotXY})
        self.DefineControl('fft_plot_buttons', {'type':'two_buttons_vertical', 'label_1':r'Power Spectrum vs Log(Freq)', 'function_1':self.OnPowerSpectrumLog, \
            'label_2':r'Power Spectrum vs Freq', 'function_2':self.OnPowerSpectrumLinear})
        self.DefineControl('spectum_button', {'type':'button', 'label':'Spectrum vs Freq', 'function':self.OnSpectrumPlot})
        self.DefineControl('save_button', {'type':'button', 'label':'Save File', 'function':self.OnSave})
        self.DefineControl('open_spreadsheet', {'type':'button', 'label':'Open Spreadsheet', 'function':self.OnSpreadsheet})
        self.DefineControl('blank_2', {'type':'blank'})
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
        self.np = self.dock.GetSystemModule('numpy')
        self.rpf = self.dock.GetSystemModule('response_plot_files')
        self.visa_comm =  self.dock.GetSystemModule('visa_comm')
        self.x = self.np.array([])
        self.ys = []
        self.aqChans = ['1', '2']
        self.chans = [] #Where channel data will be stored
        self.SetChannelsString()
        self.filein = ''    # Will be replaced by a filein object.
        # Define the control boxes AFTER the controls have been created.  Place references to other modules at the end of this list.
#        self.selected_scope_box = self.controls['selected_scope']
        #self.parameters_box = self.dock.tabs[self.name].controls['scope_parameters']
        # Refer to attributes in another module object which is an attribute of the associated tab.  Tricky.
        #self.active_scope = self.dock.tabs['tek_scopes'].module_object.active_scope
        self.scopes_module = None #self.dock.tabs['scopes'].module_object
        self.PopulateScopeList()
        #self.active_scope_obj = self.dock.tabs['tek_scopes'].module_object.scopes[self.active_scope]
        
    def OnSelectDevice(self, event):
        print(self.controls["select_device"].GetStringSelection())
        self.selected_scope_name = self.controls["select_device"].GetStringSelection()
        self.selected_scope = self.available_scopes[self.selected_scope_name]
    
    def PopulateScopeList(self):
        self.available_scopes = self.visa_comm.GetConnectedScopes()
        for item in self.available_scopes:
            self.controls['select_device'].Append(item)

    def GetSelectedScope(self, event) :
        try:
            self.available_scopes = self.scopes_module.devices
            self.selected_scope = self.scopes_module.device
            self.selected_scope_name = self.scopes_module.active_device
            message = self.selected_scope_name
        except:
            message = 'Select the oscilloscope from the Oscilloscope tab on the Instruments frame.'
        self.selected_scope_box.SetValue(message)

    def SetChannelsString(self) :
        channels_string = self.aqChans[0]
        for ch in self.aqChans[1:] :
            channels_string += ', ' + ch
        self.controls['channels'].SetValue(channels_string)

    def OnAbout(self, event):
        d = self.wx.MessageDialog( self, self.about, "About Waveforms", self.wx.ICON_INFORMATION)  # Create a message dialog box
        d.ShowModal() # Show it.
        d.Destroy() # Destroy it when finished.

    def OnHelp(self, event):
        try :
            help = self.dock.dirs[self.this_dir] + '/' + self.help        #self.dock.dirs['help'] + '/' + self.help
            f = open(help)
            help_caption = self.name
            help_me = f.read()
            f.close()
            d = self.wd.ScrolledMessageDialog(self, help_me, caption=help_caption, pos=(100,100), size=(800,500))#, style=self.wx.HSCROLL)
            d.ShowModal() # Show it.
            d.Destroy() # Destroy it when finished.
        except :
            print('Help file error.')

    def OnError(self, error) :
        d = self.wx.MessageDialog( self.dock.tabs[self.name].tab, error, "You made a mistake.", self.wx.ICON_ERROR)  # Create a message dialog box
        d.ShowModal() # Show it.
        d.Destroy() # Destroy it when finished.

    def Notify(self, message) :
        d = self.wx.MessageDialog( self.dock.tabs[self.name].tab, message, "There is a problem.", self.wx.ICON_INFORMATION)  # Create a message dialog box
        d.ShowModal() # Show it.
        d.Destroy() # Destroy it when finished.
        
    def AcquireWaveforms(self, event):
        busy = self.wx.BusyInfo("Data acquisition in progress ... ", self.parent)
        self.active_scope = self.selected_scope
        try:
            channels = self.controls['channels'].GetValue().strip().split(',')
            chDat = [] # a list for data from the specified channels.
            for item in channels:
                chDat.append(self._Channel(self.active_scope, int(item)))
                
            self.chans = chDat 
        except ValueError:
            print("Must put only integers in the channel box.")
            
        busy.Destroy()

    def OnRead(self, event) :
        self.error = ''
        d = self.wx.FileDialog(self, 'Read CSV File', self.read_directory, self.read_file, '*', self.wx.FD_OPEN, self.wx.DefaultPosition)
        if d.ShowModal() != self.wx.ID_OK : # Show it.
            return self.error
        self.read_directory = d.GetDirectory()
        self.read_file = d.GetFilename()
        self.read_path = d.GetPath()
        self.filein = self.rpf.DataFromFile(self.read_path, ',')
        if self.filein.error :
            print self.filein.error
            return self.filein.error    # Bail out if something is not quite right.
        # Create the quantities necessary for plotting using the existing buttons.
        message = ''
        for i in range(len(self.filein.data)) :
            message += ',' + str(i)
        self.read_file_box.SetValue(message[1:])
        return self.error


    def OnSave(self, event) :
        if len(self.chans) is 0:
            print("There is no data to save!")
            return
            
        #self.wd.saveFileDialog(parent, title, directory, filename, wildcard, style)
        d = self.wx.FileDialog(self, 'Save File', self.save_directory, self.save_file, '*', self.wx.FD_SAVE | self.wx.FD_OVERWRITE_PROMPT, self.wx.DefaultPosition)
        if d.ShowModal() == self.wx.ID_OK : # Show it.
            self.save_directory = d.GetDirectory()
            self.save_file = d.GetFilename()
            self.save_path = d.GetPath()
            o = open(self.save_path, 'wb')
            cw = csv.writer(o)
            column_headers = []
            for channel in self.chans :
                column_headers.append("Channel {}, {}".format(channel.channel, channel.xunit))
                column_headers.append("Channel {}, {}".format(channel.channel, channel.yunit))
                print column_headers
            cw.writerow(column_headers)
            for i in range(len(self.chans[0].data)) :
                line=[]
                for ch in self.chans:
                    line.append(ch.xdata[i])
                    line.append(ch.data[i])
                cw.writerow(line)
            del(cw)
            o.close()
        d.Destroy() # Destroy it when finished.

    def OnSpreadsheet(self, event) :
        if len(self.chans) is 0:
            print("No data has been recorded!")
            return
            
        if self.dock.os == 'win' :
            #self.Notify('Accessing Excel via PyWin32 is not yet implemented.')
            spread = [] 
            tmp = []# Index will be spreadsheet row.
            for channel in self.chans :
                tmp.append("Channel {}, {}".format(channel.channel, channel.xunit))
                tmp.append("Channel {}, {}".format(channel.channel, channel.yunit))
            spread.append(tmp)
            for i in range(len(self.chans[0].data)) :
                line=[]
                for ch in self.chans:
                    line.append(ch.xdata[i])
                    line.append(ch.data[i])
                spread.append(line)
            self.dock.system_modules['excel'].MakeSheet(self.wx, self, spread)
        else :
            self.Notify('This control is not yet functional')
            
    def OnPlotChannels(self, event):
        if len(self.chans) == 0:
            print("No data aquired, nothing to plot!")
            return            
            
        base = self.dock.system_modules['notebook_plots_base']
        graph = self.dock.system_modules['notebook_plots_graph']
        f = base.PlotFrame(title='Channels versus Time', size=(800,800))
        plist = []
        legends = []
        for channel in self.chans:
            xunit = channel.xunit
            yunit = channel.yunit
            chvt = graph.Graph('plot', [[channel.xdata, channel.data]], symbols=['b','g'],grid=False, title='Ch {} vs Time'.format(channel.channel), titlesize=24,\
                background='w', xlabel=r'Time {}'.format(xunit), ylabel=r'Signal {}'.format(yunit), labelsize=18, ticklabelsize=14)
            graph.DefineTab(f, [chvt], name='Channel {} vs Time'.format(channel.channel))
            plist.append([channel.xdata, channel.data])
            legends.append(channel.channel)
        allchvt = graph.Graph('plot', plist, symbols=['','', '', ''], grid=False, title = 'All Channels vs Time', background='w', \
            xlabel=r'Time {}'.format(xunit), ylabel=r'Signal {}'.format(yunit), labelsize=18, ticklabelsize=14, customize=None)#, legend=['1','2'])
        graph.DefineTab(f, [allchvt], name='All Channels vs Time')
        f.Show()

    def OnPlotXY(self, event) :
         if len(self.chans) < 2 :
             print("Insufficient channels for an XY plot.")
             return
             
         b = self.dock.system_modules['notebook_plots_base']
         g = self.dock.system_modules['notebook_plots_graph']
         f = b.PlotFrame(title='XY Mode Plots', size=(800,800))
         chjvchi = g.Graph('plot', [[self.chans[0].data, self.chans[1].data]], symbols=['b','g'], grid=True, \
             title = 'Ch {} vs Ch {}'.format(self.chans[1].channel, self.chans[0].channel), background='w', xlabel=r'Ch {} {}'.format(self.chans[0].channel, self.chans[0].yunit), \
             ylabel=r'Ch {} {}'.format(self.chans[1].channel, self.chans[1].yunit), labelsize=25, customize=None) 
         g.DefineTab(f, [chjvchi], name='Channel {} vs Channel {}'.format(self.chans[1].channel, self.chans[0].channel))
         f.Show()

    def OnPowerSpectrumLog(self, event) :
        self.PowerSpectrum(self.np.log10)
        return

    def OnPowerSpectrumLinear(self, event) :
        self.PowerSpectrum(None)
        return

    def PowerSpectrum(self, x_axis_transform) :
        #self.Notify('Not yet functional.')
        if len(self.chans) == 0 :
            print("There is no data to transform!")
            return
        b = self.dock.system_modules['notebook_plots_base']
        g = self.dock.system_modules['notebook_plots_graph']
        f = b.PlotFrame(title='Power Spectra', size=(800,800))
        symbols = ['', '', '', '', '']
        grid = True
        titlesize = 24
        background = 'w'
        if x_axis_transform == None :
            xlabel = r'$\nu$ (Hz)'
        else :    # assume log10
            xlabel = r'Log($\nu$)'
        ylabel = r'Power Density'
        labelsize = 18
        ticklabelsize = 14
        customize = None
        #legend=[r'1', r'2']
        #for i in range(len(self.chans)) :
        tp = []
        for channel in self.chans :
            t = self.dock.system_modules['response_plot'].PowerSpectrum(channel.xdata, channel.data)
            if x_axis_transform :
                t[0] = x_axis_transform(t[0])
            title = 'Power spectrum for Ch {}'.format(channel.channel)
            tab_name = title
            chps = g.Graph('plot', [t], symbols=symbols, grid=grid, title=title, titlesize=titlesize, background=background, \
                xlabel=xlabel, ylabel=ylabel, labelsize=labelsize, ticklabelsize=ticklabelsize, customize=customize)
            g.DefineTab(f, [chps], name=tab_name)
            tp.append(t)
            #legends.append(self.chans[i])
        title = 'Power Spectrum for all Channels'
        tab_name = title
        allchps = g.Graph('plot', tp, symbols=symbols, grid=grid, title=title, titlesize=titlesize, background=background, \
                xlabel=xlabel, ylabel=ylabel, labelsize=labelsize, ticklabelsize=ticklabelsize, customize=customize)
        g.DefineTab(f, [allchps], name=tab_name)
        f.Show()

    def OnSpectrumPlot(self, event) :
        x_axis_transform = None
        #self.Notify('Not yet functional.')
        tp = []
        if len(self.chans) == 0 :
            print('There is no data to transform!')
            return
        b = self.dock.system_modules['notebook_plots_base']
        g = self.dock.system_modules['notebook_plots_graph']
        f = b.PlotFrame(title='Spectra', size=(800,800))
        symbols = ['', '', '', '', '']
        grid = True
        titlesize = 24
        background = 'w'
        if x_axis_transform == None :
            xlabel = r'$\nu$ (Hz)'
        else :    # assume log10
            xlabel = r'Log($\nu$)'
        ylabel = r'Spectral Amplitude'
        labelsize = 18
        ticklabelsize = 14
        customize = None
        #legend=[r'1', r'2']
        #for i in range(len(self.chans)) :
        tp = []
        for channel in self.chans :
            t = self.dock.system_modules['response_plot'].AmplitudeSpectrum(channel.xdata, channel.data)
            if x_axis_transform :
                t[0] = x_axis_transform(t[0])
            title = 'Amplitude Spectrum for Ch {}'.format(channel.channel)
            tab_name = title
            chps = g.Graph('plot', [t], symbols=symbols, grid=grid, title=title, titlesize=titlesize, background=background, \
                xlabel=xlabel, ylabel=ylabel, labelsize=labelsize, ticklabelsize=ticklabelsize, customize=customize)
            g.DefineTab(f, [chps], name=tab_name)
            tp.append(t)
            #legends.append(self.chans[i])
        title = 'Amplitude Spectrum for all Channels'
        tab_name = title
        allchps = g.Graph('plot', tp, symbols=symbols, grid=grid, title=title, titlesize=titlesize, background=background, \
                xlabel=xlabel, ylabel=ylabel, labelsize=labelsize, ticklabelsize=ticklabelsize, customize=customize)
        g.DefineTab(f, [allchps], name=tab_name)
        f.Show()

    def OnNothing(self, event) :
        return
        
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
        
    class _Channel:
        """
        Holds scope channel data.
        """
        def __init__(self, scope, chanNum):
            """
            Constructor
            
            @param scope: The scope object to communicate with.
            @type scope: VisaDevice
            
            @param chanNum: The channel to acquire from.
            @type chanNum: int
            """
            self.channel = chanNum
            self.scope = scope
            self.scope.SetDataChannel(chanNum)
            self.scope.DataEncoding("ribinary")
            self.scope.DataWidth(1)
            self.scope.HeaderOn(False)
            self.scope.ChannelOn(self.channel, True)
            self.scope.SetDataStart(0)
            self.scope.SetDataStop(2500)
            self.AcqChanData()
            
        def AcqChanData(self):
            """
            Acquires data from the channel
            """
            self.data = self.scope.GetData()
            self.data = self.data[6:]
            self.yoff = self.scope.GetYOffset()
            self.ymult = self.scope.GetYMultiplier()
            self.yzero = self.scope.GetYZero()
            self.xmult = self.scope.GetXIncrement()
            self.data = map(self._ToVolts, self.data)
            self.yunit = self.scope.GetUnit("y")
            self.xunit = self.scope.GetUnit("x")
            self.xdata = self._GenXData()
            
        def _ToVolts(self, val):
            """
            Converts the binary string passed from the scope to list containing 
            values of voltage.
            
            @param val: The data string passed by the scope
            @type val: string
            """
            intVal = ord(val)
            if intVal > 127:
                intVal = (intVal - 256)
            else:
                pass
            
            return (((intVal - self.yoff)*self.ymult)+self.yzero)
            
        def _GenXData(self):
            xDat = []
            for item in range(2500):
                xDat.append(self.xmult*item)
                
            return xDat
            

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
