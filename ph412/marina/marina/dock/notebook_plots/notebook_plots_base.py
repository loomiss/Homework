import os, sys
import string as s

try:
    import wx
except:
    print('Wx not found. End of story.')
    sys.exit(0)
try:
    import wx.aui
    aui = True
except:
    print('Wx.aui not found.')
    aui = False
try:
    import matplotlib
except:
    print('Matplotlib not found. End of story.')
    sys.exit(0)

try:
    # As a backend, wxAgg seems visually superior to wx.
    be = 'wxagg'
    if be == 'wxagg':
        matplotlib.use(be) # The recommended way to use wx is with the WXAgg backend.
        from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as Canvas
        from matplotlib.backends.backend_wxagg import NavigationToolbar2Wx as Toolbar
        #import matplotlib.backends.backend_wxagg.RendererAgg as renderer
        #renderer = Canvas
    elif be == 'gtkagg':
        matplotlib.use('gtkagg')    # Install pygtk to use this backend.
        from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as Canvas
        from matplotlib.backends.backend_gtkagg import NavigationToolbar2Wx as Toolbar
    elif be == 'wx':
        matplotlib.use('wx')    # Native wx backend.
        from matplotlib.backends.backend_wx import FigureCanvasWx as Canvas
        from matplotlib.backends.backend_wx import NavigationToolbar2Wx as Toolbar
    print('\t\tUsing ' + be + '.')
except :
    print('Requested backend ' + be + ' not found.  Try another.')
    sys.exit(0)

try:
    from matplotlib import pyplot as plt
    print('\t\tUsing pyplot.')
except:
    try:
        import pylab as plt
        print('\t\tUsing PyLab.')
    except :
        print('Neither pyplot nor pylab was found.  End of story.')
        sys.exit(0)

class Page(wx.Panel):
    def __init__(self, parent, dpi = None):
        wx.Panel.__init__(self, parent)
        self.figure = plt.figure(dpi=dpi,figsize=(6,6))
        self.canvas = Canvas(self, -1, self.figure)
        self.toolbar = Toolbar(self.canvas)
        self.toolbar.Realize()

        #"""
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas,1,wx.EXPAND)
        sizer.Add(self.toolbar, 0 , wx.LEFT | wx.EXPAND)
        self.SetSizer(sizer)
        #"""

class PlotFrame(wx.Frame):
    def __init__(self, title='', size=(800,800)):
        wx.Frame.__init__(self, None, -1, title=title, size=size)
        self.Menus()
        # Create a panel and a notebook on the panel.
        # But for xp, skip the panel and just put the notebook in a sizer on the frame.
        # Under xp, a panel on a frame results in a permanently tiny, unsizable panel.
        # So, skip the panel in general.
        #p = wx.Panel(self, size=(500,100))
        #p2 = wx.Panel(self, size=(500,100))
        if aui :
            self.nb = wx.aui.AuiNotebook(self)  #(p)     # The AuiNotebook has additional functionality such as tab closure.
        else :
            self.nb = wx.Notebook(self)   # This is the wx native notebook.
        # Create a status bar to report the position of the cursor in plot coordinates.
        self.statusBar = wx.StatusBar(self, -1)
        self.statusBar.SetFieldsCount(1)
        self.SetStatusBar(self.statusBar)

        #"""
        # Place the notebook in a sizer for layout management.
        sizer = wx.BoxSizer(wx.VERTICAL)
        #sizer.Add(p, 1, wx.EXPAND)
        #sizer.Add(p2, 1, wx.EXPAND)
        sizer.Add(self.nb, 1, wx.EXPAND)
        self.SetSizer(sizer)
        #"""
        #self.AdjustPresentation(self, 1.1, [250, 250, 230])
        #self.CreateStatusBar() # A StatusBar in the bottom of the window
        #self.Menus()

    def AddTab(self, name='Graph'):    # Add a tab which is a page object on the notebook.  The tab has a plottable canvas.
        p = Page(self.nb)
        self.nb.AddPage(p, name)
        p.canvas.mpl_connect('motion_notify_event', self.UpdateStatusBar)   # Whenever the cursor over a plot, change the cursor position display in plot units.
        return p.figure, self.nb, p.canvas

    def UpdateStatusBar(self, event) :  # Called upon a motion_notify_event (cursor motion) on the canvas wherein lay the plots.
        if event.inaxes:
            x, y = event.xdata, event.ydata     # Report the cursor position in plot units.
            self.statusBar.SetStatusText(( "x= " + str(x) + "  y=" +str(y) ), 0)
        return

    def Menus(self):
        # Setting up the menu.
        menuBar = wx.MenuBar()   # define a menubar
        # Exit menu
        exit_menu_elements = [ ["E&xit"," Terminate the program", self.OnExit]] # item with alt-key, status bar description, and target procedure
        exit_menu = self.MakeMenu(exit_menu_elements)
        menuBar.Append(exit_menu, "&Exit")   # add the entire specific menu to the menubar
        # Information menu
        info_menu_elements = [ ["&New User","Introduction", self.OnHelp]]
        info_menu_elements.append(["&About", "Information about this program", self.OnAbout])
        info_menu = self.MakeMenu(info_menu_elements)
        menuBar.Append(info_menu, "&Information")
        # Add the MenuBar to the Frame.
        self.SetMenuBar(menuBar)

    def MakeMenu(self, elements) :
        the_menu = wx.Menu()
        for i in range(len(elements)) :
            if i  > 0 : the_menu.AppendSeparator()
            #the_menu.Append(elements[i][0] , elements[i][1], elements[i][2])   # add "exit" option to the menu
            item = the_menu.Append(wx.ID_ANY, elements[i][0], elements[i][1])
            #hook the event - amazingly, the procedure is passed as an argument, that is, elements[i][2] is a procedure!
            #self.Connect(elements[i][0],  -1, wx.wxEVT_COMMAND_MENU_SELECTED, elements[i][3])
            self.Bind(wx.EVT_MENU, elements[i][2], item)
        return the_menu

    def OnExit(self, event):
        self.Destroy()
        #self.Close(True)  # Close the frame.
        #sys.exit(0)

    def OnAbout(self,event):
        d= wx.MessageDialog( self,
            "Simple tabbed notebook plotting program: \n"
            + "Name:\t tabbed_plots_frames.py\n"
            + "Author:\t W. Hetherington\n"
            + "Created:\t 2009/12/10\n"
            + "Copyright:\t (c) 2009\n"
            + "License:\t No restrictions\n",
            "About this program ...", wx.ICON_INFORMATION)  # Create a message dialog box
        d.ShowModal() # Shows it
        d.Destroy() # finally destroy it when finished.

    def OnHelp(self,event):
        d= wx.MessageDialog( self, "No information yet. \n\n"
            +"No information concerning when information will be available.\n\n",
            "For New Users", wx.ICON_INFORMATION) # Create a message dialog box
        d.ShowModal() # Shows it
        d.Destroy() # finally destroy it when finished.

