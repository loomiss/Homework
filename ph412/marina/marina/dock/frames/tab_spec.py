

class ModuleTab():
    def __init__(self, frame, dock, module_name, module, color = [200,200,200]):
        # d is the Master object.
        self.d = dock
        self.wx = self.d.GetSystemModule("wx")
        self.frame = frame
        self.module_name = module_name
        self.tab_name = module_name
        self.module = module                        # The imported module
        self.color = color
        self.module_object = module.setup(self.d)   # The module object, or instance of the class specified in the module.
        self.module_object.name = module_name       # The module object needs to know its name.
        self.tab_items = {}                         # Dictionary of things associated with this tab.
        self.tab_items['object'] = self.module_object
        self.controls_defs = self.module_object.controls    # Dictionary of specifications for the controls on the tab.
        self.controls = {}          # Dictionary of wx controls as (control name : wx control) pairs.
        self.error = ''
        self.version = '1'
        print '\tTab created for module ' + module_name + ' : ' #, module
        self.MakeControls()

    def Configure(self) :
        # After the tab and controls have been created and added to the central dictionaries, some configuration might be necessary.
        # Define interfaces to some controls, such as text boxes in controls.
      
        try :
            self.module_object.PostCreationConfigure()
            message = ' : ok'
        except AttributeError:
             message = ' : PostCreationConfigure() is not defined or an error has occurred.'
        print '\t' + self.tab_name + message
    
    def MakeControls(self) :
        if self.controls_defs['setup']['tab'] != 'yes' :  # If the module is not to be associated with a visible tab, then nothings is to be done.
            return self.error
        try:
            display_name = self.module_object.display_name
        except :
            display_name = self.module_object.name
        tab = self.frame.AddTab(display_name, self.color)
        self.tab = tab
        #mod_items['tab'] = tab
        rows = self.controls_defs['setup']['rows']
        columns = self.controls_defs['setup']['columns']
        print '\t\tCreate controls for this tab using sizer of ' +  str(rows) + ' rows by ' + str(columns) + ' columns:'
        sizer = self.wx.FlexGridSizer(rows,columns,5,5) #layout grid size (rows, cols, horiz. gap, vert. gap)

        # Construct the control in the order specified by the 'order' key.
        control_list = range(len(self.controls_defs)-1)
        for key in self.controls_defs :
            if key != 'setup' :
                try :
                    control_list[self.controls_defs[key]['order']] = key    # Creates an ordered list of control labels.
                except :
                    self.error = 'Error in controls list of module ' + self.module_object.name + '.  ' + 'They must be ordered from zero up.'
                    print self.error
                    return self.error

        self.error = self.d.mc.TranslateControls(self, tab, sizer, control_list)
        tab.SetSizer(sizer)
        return self.error


