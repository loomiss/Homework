import os
#import sys     #Unused import
import wx

# Description --------------------------------------------------------------------------------------------------------------

# This is a simple editor for any application.
# Any text can be edited.

# Name:        text_editor_simple.py
# Author:      W. Hetherington
# Created:     2007/02/18
# Last modified: 2009/12/11
# Copyright:   (c) 2007, 2009
# License:     No restrictions

#---------------------------------------------------------------------------------------------------------------------------
class EditWindow(wx.Frame):
    def __init__(self,parent, id, filename, caller, size=(640,480)):
        self.filename=filename
        #self.dirname="."
        self.dirname = os.getcwd()
        wx.Frame.__init__(self,parent,-1, "Text Editor", wx.Point(200, 150), size = size, style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)
        self.control = wx.TextCtrl(self, 1, style=wx.TE_MULTILINE)
        try:
            stuff = ''
            for a in caller.client.data :
               stuff += str(a[0]) + ', ' + '%.3G' %a[1] + '\n'
            self.control.SetValue(stuff)
        except:
            pass
        self.CreateStatusBar() # A Statusbar in the bottom of the window
        # Setting up the menu.
        self.Menus()
        self.recent_files = []

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
        # Files menu
        files_menu_elements = [["&Open"," Edit a text file", self.OnOpen]] # item with alt-key, status bar description, and target procedure
        files_menu_elements.append(["Open &Recent", " Reopen a file", self.OnOpenRecent])
        files_menu_elements.append(["&Close"," Close current file", self.OnClose]) 
        files_menu_elements.append(["&New"," Create a new file", self.OnNew]) 
        files_menu_elements.append(["&Save"," Save file", self.OnSave]) 
        files_menu_elements.append(["Save &As"," Save file as ...", self.OnSaveAs]) 
        files_menu = self.MakeMenu(files_menu_elements)
        menuBar.Append(files_menu, "&Files")   # add the entire specific menu to the menubar
        # Add the MenuBar to the Frame.
        self.SetMenuBar(menuBar)  
        self.Show(True)

    def MakeMenu(self, elements) :
        the_menu = wx.Menu()
        for i in range(len(elements)) :
            if i  > 0 : the_menu.AppendSeparator()
            item = the_menu.Append(wx.ID_ANY, elements[i][0], elements[i][1])
            #hook the event - amazingly, the procedure is passed as an argument, that is, elements[i][2] is a procedure!
            self.Bind(wx.EVT_MENU, elements[i][2], item)
        return the_menu

    def OnHelp(self,event):
        d= wx.MessageDialog( self, "This is a simple editor. \n\n"
            +"Upon invocation by a calling program, the current text is loaded into the editor. \n\n"
            +"Upon invocation, the default file name is the current file name in the calling program. \n\n"
            +"Edited data can be saved to a file but cannot be directly passed back to the caller. \n\n"
            +"Any text can be edited. \n\n",
            "For New Users", wx.ICON_INFORMATION) # Create a message dialog box
        d.ShowModal() # Shows it
        d.Destroy() # finally destroy it when finished.

    def OnAbout(self,event):
        d= wx.MessageDialog( self,
            "Simple editor\n"
            + "Name:\t text_editor.py\n"
            + "Author: W. Hetherington\n"
            + "Created:\t 2007/07/18\n"
            + "Modified:\t 2009/12/11\n"
            + "Copyright:\t (c) 2007, 2009\n"
            + "License:\t No restrictions\n",
            "About text_editor", wx.ICON_INFORMATION)  # Create a message dialog box
        d.ShowModal() # Shows it

    def OnExit(self,e):
        self.Close(True)  # Close the frame.
        #if __name__ == '__main__' : sys.exit(0)

    def OnSave(self,e):
        """ Save the current file """
        f=open(os.path.join(self.dirname,self.filename),"w")
        f.write(self.control.GetValue())
        f.close()

    def OnNew(self, e) :
        self.control.SetValue("")

    def OnOpen(self,e):
        """ Open a file"""
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()
            self.edit_file_path = os.path.join(self.dirname,self.filename)
            dlg.Destroy()
            self.EditFile()
        else :
            dlg.Destroy()
    
    def EditFile(self) :
        try:
            f=open(self.edit_file_path,'r')
        except :
            self.ErrorReport('file read error for path ' + self.edit_file_path)
            return
        try:
            self.control.SetValue(f.read())
            f.close()
            self.AddToRecent()      # Add this file path to the list of recent files.
            self.SetStatusText('editing: ' + self.edit_file_path)
        except :
            self.ErrorReport('the requested file is not a text file and is not editable.')

    def AddToRecent(self) :
        if self.recent_files.count(self.edit_file_path) :
            self.recent_files.pop(self.recent_files.index(self.edit_file_path))
        self.recent_files.insert(0, self.edit_file_path)
        if len(self.recent_files) > 10 :
            self.recent_files.pop()
    
    def OnOpenRecent(self, e) :
        # SingleChoiceDialog has no size argument.
        dlg = wx.SingleChoiceDialog(self, 'Recently Opened Files', 'Select one', self.recent_files, wx.CHOICEDLG_STYLE)
        if dlg.ShowModal() == wx.ID_OK :
            self.edit_file_path = dlg.GetStringSelection()
            dlg.Destroy()
            self.AddToRecent()
            self.EditFile()
        else :
            dlg.Destroy()
        return
    
    def OnClose(self, e) :
        # Close the current file
        self.control.SetValue('')
        self.SetStatusText('')

    def OnSaveAs(self,e):
        """ Save as """
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, self.filename,"*.*", wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()
            self.OnSave(e)
        dlg.Destroy()

    def ErrorReport(self, error) :
        d= wx.MessageDialog( self,
            error + "\n", "Error Report", wx.ICON_INFORMATION)  # Create a message dialog box
        d.ShowModal() # Shows it

def Main(filename, caller):
    app = wx.PySimpleApp()
    frame = EditWindow(None, -1, filename, caller)
    frame.Show(1)
    app.MainLoop()
    
if __name__ == '__main__' :
    #Main('')
    app = wx.PySimpleApp()
    frame = EditWindow(None, -1, "", None, size=(640,480))
    frame.Show(1)
    app.MainLoop()
