import wx       #wx import is required to inherit from wx.Panel.

NAME = "File Plot Basic"   #Put the name of your tab here.
DEFAULT_COLOR = [200, 200, 200]       

required_modules = ['notebook_plots_base', 'notebook_plots_graph', 'numpy', 'response_plot_files']


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
        self.wx = wx
        self.help = "app/data_analysis/help.txt"
        self.wd = self.dock.GetSystemModule("wx.lib.dialogs")
        self.np = self.dock.GetSystemModule('numpy')
        self.rpf = self.dock.GetSystemModule('response_plot_files')
        self.x = self.np.array([])
        self.ys = []
        self.filein = ''    # Will be replaced by a filein object.
        # Define the control boxes AFTER the controls have been created.  Place references to other modules at the end of this list.
        
        self.version = '1'
        self.name = name
        self.display_name = 'Basic Data File Plots'
        self.content = 'This module will read data from a csv file and perform simple plotting operations.'
        self.about = "Module: file_plot_basic.py \n" \
            + "Purpose: Basic plotting of data from files.\n"\
            + "Authors:\t W. Hetherington\n" \
            + "Created:\t 2011/05/05\n" \
            + "Copyright:\t (c) 2011\n" \
            + "License:\t No restrictions\n"
        self.read_file = ''
        self.read_directory = 'data'    #dock.dirs['default_data_dir']        #'data'
        self.read_file_ext = '*'#'|*.csv|*.dat|*.txt|'    #'csv files (*.csv)|*.csv |'    # txt files (*.txt)|*.txt | dat files (*.dat)|*.dat |'
        self.symbols = ['', '', '', '', '', '', '', '']    #['o','o', 'o', 'o', 'o', 'o', 'o']
        
        self.ControlSetup()
        self.MakeControls()
        
        self.read_files_box = self.controls['read_files_panel']    # The arrays are listed here.
        #self.selected_scope_box = self.dock.tabs[self.name].controls['selected_scope']
        # Refer to attributes in another module object which is an attribute of the associated tab.  Tricky.
        #self.active_scope = self.dock.tabs['tek_scopes'].module_object.active_scope
        
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
        
        
    def ControlSetup(self):
        self.controls = {}
        self.controls['setup'] = {'format':'control_2', 'tab':'yes', 'rows':4, 'columns':2}

        self.controls['read_files_panel']={'order':0, 'type':'text_over_two_buttons', 'dimensions':[700,200],'label':'Arrays From Files', 'button_label_1':'Read Data Files','function_1':self.OnRead}
        self.controls['read_files_panel'].update({'button_label_2':'Append Data from Files', 'function_2':self.OnAppend})
        self.controls['plot_buttons']={'order':1, 'type':'two_buttons_vertical', 'label_1':'Plot Arrays vs Ch 0', 'function_1':self.OnPlotArrays}
        self.controls['plot_buttons'].update({'label_2':'Plot Arrays as XY', 'function_2':self.OnPlotArraysXY})

        self.controls['about+help_buttons']={'order':2, 'type':'two_buttons_horizontal', 'label_1':'About This Module', 'function_1':self.OnAbout}
        self.controls['about+help_buttons'].update({'label_2':'Help', 'function_2':self.OnHelp})

    
    def OnAbout(self, event):
        d = self.wx.MessageDialog( self, self.about, "About Basic Data File Plots", self.wx.ICON_INFORMATION)  # Create a message dialog box
        d.ShowModal() # Show it.
        d.Destroy() # Destroy it when finished.

    def OnHelp(self, event):
        f = open(self.help)
        help_me = f.read()
        f.close()
        d = self.wd.ScrolledMessageDialog(self, help_me, caption='Basic Data File Plots Help', pos=(100,100), size=(800,500))#, style=self.wx.HSCROLL)
        d.ShowModal() # Show it.
        d.Destroy() # Destroy it when finished.

    def OnError(self, error) :
        d = self.wx.MessageDialog( self, error, "You made a mistake.", self.wx.ICON_ERROR)  # Create a message dialog box
        d.ShowModal() # Show it.
        d.Destroy() # Destroy it when finished.

    def Notify(self, message) :
        d = self.wx.MessageDialog( self, message, "There is a problem.", self.wx.ICON_INFORMATION)  # Create a message dialog box
        d.ShowModal() # Show it.
        d.Destroy() # Destroy it when finished.

    def OnRead(self, event) :
        self.error = ''
        d = self.wx.FileDialog(self, 'Read Multiple CSV Files', self.read_directory, self.read_file, self.read_file_ext, self.wx.FD_OPEN | self.wx.FD_MULTIPLE, self.wx.DefaultPosition)
        if d.ShowModal() != self.wx.ID_OK :
            #self.Notify('Read error: ')
            return self.error
        #if d.ShowModal() != self.wx.ID_OK : # Show it.
            #return self.error
        self.read_directory = d.GetDirectory()
        self.read_files = d.GetFilenames()
        self.read_file = self.read_files[0]
        self.read_paths = d.GetPaths()
        self.fobs = []        # file objects
        for p in self.read_paths :
            fin = self.rpf.DataFromFile(p, ',')
            if fin.error :
                self.OnError(fin.error)
                return fin.error    # Bail out if something is not quite right.
            self.fobs.append(fin)
        # Extract the data from the file objects
        self.data = [f.data for f in self.fobs]        # Isn't this special.
        self.DisplayArrays()
        return self.error

    def DisplayArrays(self) :
        # Display the file object arrays in the box.
        message = ''
        for i in range(len(self.fobs)) :
            message += self.read_files[i] + ' : data arrays = '
            #message += self.read_paths[i] + '='
            dat_list = ''
            for j in range(len(self.fobs[i].data)) :
                dat_list += ',' + str(j)
            message += dat_list[1:]  + '\n'
            if True == False :
                message += 'Attributes : '    # remove the leading comma
                fd = self.fobs[i].__dict__    #dir(self.fobs[i])
                for f in fd :
                    if f != 'data' :
                        message += f + ' = ' + str(fd[f]) + ' ; '
                message = message[:-2] + '\n'    # Remove the trailing ;<space>
        self.read_files_box.SetValue(message)
        return self.error

    def OnAppend(self, event) :
        #self.Notify('Append data from files is not functional.')
        self.error = ''
        d = self.wx.FileDialog(self, 'Read Multiple CSV Files', self.read_directory, self.read_file, self.read_file_ext, self.wx.FD_OPEN | self.wx.FD_MULTIPLE, self.wx.DefaultPosition)
        if d.ShowModal() != self.wx.ID_OK : # Show it.
            return self.error
        self.read_directory = d.GetDirectory()
        read_files = d.GetFilenames()
        self.read_file = self.read_files[0]
        read_paths = d.GetPaths()
        fobs = []        # file objects
        for p in read_paths :
            fin = self.rpf.DataFromFile(p, ',')
            if fin.error :
                print fin.error
                return fin.error    # Bail out if something is not quite right.
            fobs.append(fin)
        # Extract the data from the file objects
        data = [f.data for f in fobs]        # Isn't this special.
        self.fobs.extend(fobs)
        self.data.extend(data)
        self.read_paths.extend(read_paths)
        self.read_files.extend(read_files)
        self.DisplayArrays()
        return self.error

    def MinimumArraysInDataSets(self) :
        arrays = 100
        for d in self.data :
            if len(d) < arrays :
                arrays = len(d)        # The minimum number of arrays in a data set from a file.
        return arrays

    def OnPlotArrays(self, event) :
        arrays = self.MinimumArraysInDataSets()
        if arrays < 2 :
            self.OnError('Nothing to plot.  Insufficient number of input arrays.')
            return
        b = self.dock.GetSystemModule('notebook_plots_base')
        g = self.dock.GetSystemModule('notebook_plots_graph')
        f = b.PlotFrame(title='Channels versus Time', size=(800,800))
        #legends = [] #Unused list
        # First, compare the number of arrays in each file.  Need to use only the minimum number of arrays.
        plist = []
        for i in range(1, arrays) :
            #xunit = 's' #Unused Variable
            #yunit = 'V' #Unused Varibale
            plist.append([])
            for j in range(len(self.data)) :
                plist[i-1].append([self.data[j][0], self.data[j][i]])
            title = 'Ch '+ str(i) +' vs Ch 0'
            xlabel = 'Ch 0'     #('+xunit+')'
            ylabel = 'Signal'    # ('+yunit+')'
            chvt = g.Graph('plot', plist[i-1], symbols=self.symbols, grid=False, title = title, titlesize=24,\
                background='w', xlabel=xlabel, ylabel=ylabel, labelsize=18, ticklabelsize=14, customize=None)#, legend=[r'1', r'2'])
            g.DefineTab(f, [chvt], name='Channel '+ str(i) +' vs Ch 0')
        bigplist = []
        for p in plist :
            bigplist.extend(p)
            #plist.append([self.filein.data[0], self.filein.data[i]])
            #legends.append(str(i))
        allchvt = g.Graph('plot', bigplist, symbols=self.symbols, grid=False, title = 'All Channels vs Channel 0', background='w', \
            xlabel=xlabel, ylabel=ylabel, labelsize=18, ticklabelsize=14, customize=None)#, legend=['1','2'])
        g.DefineTab(f, [allchvt], name='All Channels vs Channel 0')
        f.Show()

    def OnPlotArraysXY(self, event) :
        arrays = self.MinimumArraysInDataSets()
        if arrays < 3 :
            self.OnError('Insufficient number of arrays for an XY plot.')
            return
        b = self.dock.GetSystemModule('notebook_plots_base')
        g = self.dock.GetSystemModule('notebook_plots_graph')
        f = b.PlotFrame(title='XY Mode Plots', size=(800,800))
        #xunit = 'V'
        #yunit = 'V'
        plist = []
        for i in range(1, arrays) :
            for j in range(i+1, arrays) :
                plist.append([])
                for k in range(len(self.data)) :
                    plist[i-1].append([self.data[k][i], self.data[k][j]])
                title = 'Ch '+ str(j) +' vs Ch '+ str(i)
                xlabel = 'Ch '+ str(i)    # +' ('+yunit+')'
                ylabel = 'Ch '+ str(j)     #+' ('+yunit+')'
                chjvchi = g.Graph('plot', plist[i-1], symbols=self.symbols, grid=True, title = title, background='w', xlabel=xlabel, ylabel=ylabel, labelsize=25, customize=None)    #, legend=[r'1', r'2']
                g.DefineTab(f, [chjvchi], name='Channel '+ str(j) +' vs Channel '+ str(i))
        f.Show()
        
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
