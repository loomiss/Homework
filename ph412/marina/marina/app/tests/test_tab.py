"""
This is a skeleton module for defining a Tab object to be used in Marina.
"""

import wx       #wx import is required to inherit from wx.Panel.

NAME = "Skeleton Tab"   #Put the name of your tab here.
DEFAULT_COLOR = [200, 200, 200]

required_moules = [] # List required support modules here.


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
    
    
if __name__ == '__main__':
    print('This is a Tab object to be used in Marina.')
