#! /usr/bin/env python


try:
    import wx, wx.aui, os
    from wx.lib import dialogs as wd
except ImportError as er:
    print('frame_spec failed to import a required module')
    print(er)
    exit(0)

        
class _Notebook(wx.aui.AuiNotebook):
        def __init__(self,  parent):
            super(_Notebook,  self).__init__(parent, id=wx.ID_ANY, style=wx.aui.AUI_NB_DEFAULT_STYLE)
            self.parent = parent
            self.tabs = {}      # {Tab Name: Tab Object}            
            self.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.OnTabClose) # Destroys a tab and removes it from the tabs dictionary when it is closed. 
            
            
        def OnTabClose(self, event):
            name = self.GetPage(event.GetSelection()).name
            self.RemoveTab(name)
            
            if len(self.tabs) is 0:
                self.parent.OnExit(None)


        def AddTab(self,  tab,  name, select = False):
            if self.GetTab(name):
                name = self.FindNextAvailName(name)
                tab.SetName(name)
                
            self.AddPage(tab,  name,  select)
            self.tabs[name]=tab
            
        
        def GetTab(self,  name):
            if name in self.tabs.keys():
                return self.tabs[name]
            else:
                return None
                
                
        def RemoveTab(self,  name):
            if self.GetTab(name):
                self.tabs.pop(name)
                print("Tab {} deleted!".format(name))
            
            
        def FindNextAvailName(self, name):
            """
            Takes the name passed and checks if it has already been used in 
            self.tabs. If it has then a number is concatinated on the end.
            
            @param name: The proposed name of the tab.
            @type name: string
            
            @return: The suggested name.
            @type: string
            """
            matches = []
            for tab in self.tabs.keys():
                if tab.count(name):
                    matches.append(tab)
                
            if len(matches) is 0:   
                return name         #No matching name was found, return the original name.
            
            for index in range(len(matches)):
                matches[index] = matches[index].strip(name).strip() # Remove name match and space, convert to int.            
            
            try:
                matches.remove('')
            except ValueError:
                print("No empty string found!")  
            
            if len(matches) is 0:
                return name + " 1"
            else:
                highest = 0
                for index in range(len(matches)):
                    if int(matches[index]) > highest:
                        highest = int(matches[index])
                return name + " {}".format(highest + 1)


class MainFrame(wx.Frame) :      
    def __init__(self, d, name, parent=None, pos=(0, 0), size=(900, 700), style=wx.wx.DEFAULT_FRAME_STYLE, text_editor=None) :
        super(MainFrame,self).__init__(parent, title=name, pos=pos, size=size, style=style)
        self.text_editor = text_editor
        self.Menus()
        self.recent_dirs = []
        self.nb = _Notebook(self)       # Create notebook to hold tabs.
       
        self.statusBar = wx.StatusBar(self, -1)  # Create a status bar for later use.
        self.statusBar.SetFieldsCount(1)
        self.SetStatusBar(self.statusBar)
        self.d = d
        self.name = name
        self.error = ''
        self.version = '1'
        print('Frame created for {}:'.format(self.name))
        
        
    ## MakeTab - This will create a new tab in the frame. Returns
    ##           the tab object.
    def MakeTab(self, dock,  tabModule, tabName = None,  color = None):
        tab = None
        
        if color is None and tabName is None:
            tab = tabModule.Setup(dock,  self)
            tabName = tabModule.NAME
        elif color is None:
            tab = tabModule.Setup(dock,  self,  name = tabName)
        elif tabName is None:
            tab = tabModule.Setup(dock, self, color = color)
            tabName = tabModule.NAME
        else:
            tab = tabModule.Setup(dock, self,  tabName,  color)
            
        self.nb.AddTab(tab,  tabName)
        return tab


    ## GetTab - Returns the tab object of the given name. If no name is 
    ##          provided then the whole tabs dictionary is returned. If
    ##          the specified tab is not present then None is returned.
    ## name -- The name of the tab object you wish to retrieve.
    def GetTab(self,  name = None):
        if name is None:
            return self.tabs
        elif name in self.tabs.keys():
            return self.tabs[name]
        else:
            return None

    ## MakeTabs - creates all tabs specified in modules.txt for this frame.
    ## d -- The dock Master object.
    def MakeTabs(self, d):
        try:
            modules = d.GetTabModules(self.name) # Modules is a list of tab modules for the given frame name
        except:
            print("Modules could not be loaded for frame: {}".format(self.name))
            return
            
        try:
            color = d.GetFrameParameters(self.name)["bkg_color"]
            for m in modules:
                self.MakeTab(self.d,  m, color = color)
        except:
            print("Color not found in Frame Parameters, using defaults for frame: {}".format(self.name))
            for m in modules:
                self.MakeTab(self.d,  m)

    
    def Menus(self):
        # Setting up the menu.
        menuBar = wx.MenuBar()   # define a menubar

        # Exit menu
        exit_menu_elements = [ ["E&xit"," Terminate the program", self.OnExit]] # item with alt-key, status bar description, and target procedure
        exit_menu = self.MakeMenu(exit_menu_elements)
        menuBar.Append(exit_menu, "&Exit")   # add the entire specific menu to the menubar

        # Information menu
        info_menu_elements = [ ["&Read Me","Introduction", self.OnHelp]]
        info_menu_elements.append(["&About", "Information about this program", self.OnAbout])
        info_menu = self.MakeMenu(info_menu_elements)
        menuBar.Append(info_menu, "&Information")

        # Files menu
        files_menu_elements = [ ["&Edit"," Edit a text file", self.OnEdit]] # item with alt-key, status bar description, and target procedure
        files_menu_elements.append(["&Data Directory"," Select Data Directory", self.OnDataDir]) # item with alt-key, status bar description, and target procedure
        files_menu_elements.append(["&Recent Data Directories", " Reselect a Data Directory", self.OnRecentDataDirectory])
        #files_menu_elements.append( ["&Plot"," Plot a data file", self.OnPlot])
        #files_menu_elements.append( ["&Filter"," Filter and plot a data file", self.OnFilter])
        #files_menu_elements.append( ["&Set Filter"," Set the filter type and parameters", self.OnSetFilter])
        files_menu = self.MakeMenu(files_menu_elements)
        menuBar.Append(files_menu, "&Files")   # add the entire specific menu to the menubar

        # Add the MenuBar to the Frame.
        self.SetMenuBar(menuBar)
        

    def MakeMenu(self, elements) :
        the_menu = wx.Menu()
        for i in range(len(elements)) :
            if i  > 0 : the_menu.AppendSeparator()
            item = the_menu.Append(wx.ID_ANY, elements[i][0], elements[i][1])
            #hook the event - amazingly, the procedure is passed as an argument, that is, elements[i][2] is a procedure!
            self.Bind(wx.EVT_MENU, elements[i][2], item)
        return the_menu


    def OnExit(self, event):
        self.Destroy()


    def OnAbout(self,event):
        mess = "The Module Dock was designed for modules related to experiments, instrumentation and various tasks.\n" \
            + "Authors:\t K.Paul, W. Hetherington\n" \
            + "Created:\t 2010/12/15\n" \
            + "Copyright:\t (c) 2010, 2011\n" \
            + "License:\t No restrictions\n"
        d= wx.MessageDialog( self, mess, "About Control", wx.ICON_INFORMATION)  # Create a message dialog box
        d.ShowModal() # Shows it
        d.Destroy() # finally destroy it when finished.


    def OnHelp(self,event):
        print os.getcwd()
        print self.help
        f = open(self.help)
        help_me = f.read()
        f.close()
        d = wd.ScrolledMessageDialog(self, help_me, caption='Help', pos=(100,100), size=(800,500))
        d.ShowModal() # Show it.
        d.Destroy() # Destroy it when finished.


    def OnEdit(self, event):
        self.text_editor.Main("", self)


    def OnDataDir(self, event) :
        #dlg = wx.FileDialog(self, "Choose a directory to which to save data", self.save_dir, "", "*.")
        dlg = wx.GenericDirCtrl(self, dir=self.save_dir, pos=wx.DefaultPosition, size=wx.DefaultSize)
        if dlg.ShowModal() == wx.ID_OK:
            #self.filename=dlg.GetFilename()
            self.save_dir=dlg.GetDirectory()
            self.action.AppendText(self.dirname +'\n' + self.filename + '\n')
        dlg.Destroy()


    def OnRecentDataDirectory(self, event) :
        return


## Depricated ??
def AdjustPresentation(client, font_factor, bkg_color) :
    client.SetBackgroundColour(wx.Colour(bkg_color[0], bkg_color[1], bkg_color[2]))
    #self.SetBackgroundColour(wx.Color(253,253,240))
    ScaleFontSize(client, font_factor)   # This scales the fonts within the window but not in the title, menu or status bars.

def ScaleFontSize(some_frame, factor) :
    the_font = some_frame.GetFont()
    the_font.SetPointSize(the_font.GetPointSize() * factor)
    some_frame.SetFont(the_font)


if __name__ == "__main__":
   print("This is a support module for Marina. Please run control.py if you wish to run Marina.")
