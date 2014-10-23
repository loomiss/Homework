


# Description --------------------------------------------------------------------------------------------------------------

#test module

#---------------------------------------------------------------------------------------------------------------------------

import wx       #wx import is required to inherit from wx.Panel.

NAME = "Tek Scopes"   #Put the name of your tab here.
DEFAULT_COLOR = [200, 200, 200]

required_modules = ['tek1012b', 'waveforms', 'wx.lib.dialogs']


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
        self.wd = self.dock.GetSystemModule("wx.lib.dialogs")
        self.time = self.dock.GetSystemModule('time')
        self.tek = self.dock.GetSystemModule('tek1012b')
        self.tek_fake = self.dock.GetSystemModule('tek1012b_fake')
        self.np = self.dock.GetSystemModule('numpy')
        self.version = '1'
        self.content = 'This module will locate all Tektronix TDS1012B oscilloscopes on the USB ports.'
        self.about = "Module: tek_scopes\n" \
        + "Purpose: Basic Tektronix TDS1012B I/O.\n"\
        + "Authors:\t W. Hetherington\n" \
        + "Created:\t 2011/4/23\n" \
        + "Copyright:\t (c) 2011\n" \
        + "License:\t No restrictions\n"
        self.this_dir = 'app/scope'
        self.help = 'tek_scopes_help.txt'
        self.delay_by_vendor = {'rig' : 0.3, 'tek' : 0.1}    # in seconds
        self.delay = 0.5
        #self.active_scope = ' '    # name of selected scope
        self.scope_list = []    # list of names
        self.scopes = {}        # (name : handle ) pairs
        dock.usb_instruments = {}
        
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
        self.DefineControl('setup', {'format':'control_2', 'tab':'yes', 'rows':4, 'columns':3})
        self.DefineControl('find_devices', {'type':'text_and_button','dimensions':[200,100],'label':'Instruments Found','button_label':'Find Instruments','function':self.FindDevices})
        self.DefineControl('select_device', {'type':'combo_box', 'dimensions':[150,25],'label':'Select Oscilloscope', 'function':self.OnSelectDevice})
        self.DefineControl('device_properties', {'type':'text_area', 'dimensions':[200, 150], 'read_only':True, 'scroll':True, 'multiline':True, 'label':'Selected Instrument Properties'})
        self.DefineControl('delay', {'type':'text_area', 'dimensions':[50, 30], 'read_only':False, 'scroll':False, 'multiline':False, 'label':'Delay Between Instructions'})
        self.DefineControl('device_commands', {'type':'text_and_button','dimensions':[250,100],'label':'Command String','button_label':'Send','function':self.SendCommandString})
        self.DefineControl('device_reply', {'type':'text_and_button','dimensions':[300,50],'hscroll':True,'label':'Scope Reply','button_label':'Read', 'function':self.GetReply})
        self.DefineControl('device_parameters', {'type':'text_and_button','dimensions':[300,150],'label':'Selected Scope Parameters','button_label':'Get Parameters', 'function':self.ScopeParameters})
        #self.DefineControl('blank_1', {'type':'blank'})
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
        
        
        # Define the control boxes AFTER the controls have been created.
        #self.find_instruments_box = self.dock.tabs[self.name].controls['find_instruments']
        self.find_devices_box = self.controls['find_devices']
        #self.select_scope_box = self.dock.tabs[self.name].controls['select_scope']
        self.select_device_box = self.controls['select_device']
        self.device_properties = self.controls['device_properties']
        self.delay_box = self.controls['delay']
        self.commands_box = self.controls['device_commands']
        self.reply_box = self.controls['device_reply']

        self.waveforms_selected_scope = None #self.dock.tabs['waveforms'].controls['selected_scope']
        self.response_spectrum_selected_scope = None #self.dock.tab['response_spectrum'].controls['selected_scope']
        self.parameters_box = self.controls['device_parameters']
        # Refer to attributes in another module object which is an attribute of the associated tab.  Tricky.

    def FindInstruments(self, event) :
        #the_box = self.dock.modules[self.name]['find_instruments']
        message = ''
        #scope_list = []
        #self.scopes = {}
        try :
            self.scopes = self.tek.FindTDS1012B(self.dock.usb_instruments)
            for key in self.scopes :
                message += key + '\n'
                self.select_scope_box.Append(key)
                self.scope_list.append(key)
        except :
            message = 'FindTDS1012B error.\nMissing import?\nUsing simulation module.\n'
            try :
                self.scopes = self.tek_fake.FindTDS1012B()
                self.select_scope_box.Clear()
                for key in self.scopes :
                    message += key + '\n'
                    self.select_scope_box.Append(key)
                    self.scope_list.append(key)
            except :
                message += 'Simulation module is not functional.\n'
        self.find_instruments_box.SetValue(message)

    def FindDevices(self, event) :
        #the_box = self.dock.modules[self.name]['find_instruments']
        message = ''
        self.device_list = []
        #self.scopes = {}
        try :
            self.devices = self.tek.FindTDS1012B(self.dock.usb_instruments)    # should be FindDevices
            self.select_device_box.Clear()
            for key in self.devices :
                message += key + '\n'
                self.select_device_box.Append(key)
                self.device_list.append(key)
        except :
            message = 'FindDevices error.\nMissing import?\nMissing instruments?\n'
            #try :
                #self.scopes = self.tek_fake.FindTDS1012B()
                #self.select_scope_box.Clear()
                #for key in self.scopes :
                    #message += key + '\n'
                    #self.select_scope_box.Append(key)
                    #self.scope_list.append(key)
            #except :
                #message += 'Simulation module is not functional.\n'
        self.find_devices_box.SetValue(message)

    def OnSelectScope(self, event):
        self.selected_scope_identity = self.select_scope_box.GetCurrentSelection()
        self.active_scope = self.scope_list[self.selected_scope_identity]
        self.waveforms_selected_scope.SetValue(self.active_scope)
        self.response_spectrum_selected_scope.SetValue(self.active_scope)

    def OnSelectDevice(self, event):
        self.selected_device_identity = self.select_device_box.GetCurrentSelection()
        self.active_device = self.device_list[self.selected_device_identity]
        self.active_scope = self.active_device        # this should not be necessary
        #print self.active_device
        self.waveforms_selected_scope.SetValue(self.active_device)
        self.response_spectrum_selected_scope.SetValue(self.active_device)
        self.device = self.devices[self.active_device]
        device_properties = self.device.idn + '\n'
        self.device.protocol = self.device.device['vendor'].lower()[0:3]
        for p in self.device.device :
            #print p, self.device.device[p]
            if p != 'handle' :
                device_properties += p + ' : ' + str(self.device.device[p]) + '\n'
        self.device_properties.SetValue(device_properties)
        try :
            self.delay = self.delay_by_vendor[self.device.device['vendor'].lower()[0:3]]
        except :
            pass
        self.delay_box.SetValue(str(self.delay))
        self.commands_box.Clear()

    def SendCommandString(self, event) :
        commands = self.commands_box.GetValue().split('\n')
        self.delay = float(self.delay_box.GetValue())
        #print('Delay = ' + str(self.delay))
        for c in commands :
            d = c.split('#')[0].strip()
            if len(d) > 0 :
                self.devices[self.active_device].Write(d)
                self.time.sleep(self.delay)
        return

    def GetReply(self, event) :
        reply = ''
        reply += self.devices[self.active_device].Read() + '\n'
        self.reply_box.SetValue(reply)
        return

    def OnAbout(self, event):
        #d = self.wx.MessageDialog( self.dock.modules[self.name]['tab'], self.about, "About Scope", self.wx.ICON_INFORMATION)  # Create a message dialog box
        #print self.name
        #print self.dock.tabs[self.name].tab
        d = self.wx.MessageDialog( self, self.about, "About Scope", self.wx.ICON_INFORMATION)  # Create a message dialog box
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

    def SelectScope(self) :
        print 'Unable to comply.'

    def ScopeParameters(self, event) :
        self.parameters_box.SetValue('Working ... \n')
        message = ''
        message += self.device.Query()    #scopes[self.active_scope].Query()
        self.parameters_box.SetValue(message)
        return

    def SendCommandStringOld(self, event) :
        commands = self.commands_box.GetValue()
        self.scopes[self.active_scope].Write(commands)
        return

    def GetReplyOld(self, event) :
        reply = ''
        reply += self.scopes[self.active_scope].Read() + '\n'
        self.reply_box.SetValue(reply)
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



