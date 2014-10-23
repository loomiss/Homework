"""
Dock is the central component of Marina.
"""

try:
    import os, sys, platform, importlib, wx, wx.lib.dialogs
except ImportError as ie:
    print("Dock failed to import a required library!")
    print(ie.args)
    exit(-1)
    

class Master() :
    """
    The Master object holds all imported tab and system modules for Marina. It
    is also responsible for running the GUI and provining top level frame and 
    tab creation functions.
    """
    def __init__(self, imp_file, core_path, debug = False):
        """
        @param imp_file: A file containing frame initilization settings, usually
        it is modules.txt.
        @type imp_file: string
        
        @param core_path: The working directory
        @type core_path: string
        """
        self.version = '1'
        self.system_modules = {"os": os, "sys" : sys, "platform" : platform, "wx" : wx, "importlib" : importlib}      # dictionary of (system module name:imported module) pairs.
        self.frame_objects = {}     # Contains the names of each frame and the associated frame object.
        self.tab_modules = {}       # Contains the name of each frame and a list of associated tab modules
        self.frame_parameters = {}
        self.core_path = core_path

        self.wx = wx
        self.app = wx.App(False)        ## Moved main GUI handling to the master class
        self.display_size = wx.GetDisplaySize().asTuple()     # Size of the display being used.
        self.frame_position = (0, 0)    # Where the next frame will be placed.

        print('Dock Master version: {}'.format(self.version))
        psos = platform.uname()
        print('Operating system : {} {}'.format(psos[0],psos[2]))
        self.sos = psos[0].strip().lower()
        if self.sos.find('linux') > -1 :
            self.os = 'linux'
        elif self.sos.find('win') > -1 :
            self.os = 'win'
        else :
            print('Dock has not been tested with {}.'.format(self.sos))
        exclusions_by_os = {'lin' : ['pywin32', 'excel'], 'win' : []}   # Modules that do not function with the given operating system.
        if self.sos[:3] in exclusions_by_os :
            self.exclusions = exclusions_by_os[self.sos[:3]]
            
        if debug is False:    
            self._SetPaths("dock/System.txt")           # Set directories where other modules can be found.
            self._ImportSysMods("dock/System.txt")      # Import modules specified in System.txt.
            self._SetRequiredCoreModules("text_editor_simple", "frame_spec", "tab_spec", "controls_library")    # Set some required variables.
            self._ImportTabMods(imp_file)               # Import the tab modules as defined in modules.txt.
        
        ######################### GUI CREATION ################################
            self._MakeFrames()              # Create all frames and tabs specified in modules.txt.
            self._DisplayFrames()           # Display the frames and tabs.
            self.app.MainLoop()             # The main loop for the GUI.

        #######################################################################



    ###########################################################################
    #   Below here are private functions that should not be used outside of   #
    #   the master object.                                                    #
    ###########################################################################

    
    def _ImportSystemModule(self, modName):
        """
        Attempts to import a system module and add it to the system_modules 
        dictionary. Returns the module.
        
        @param modName: The name of the desired module passed as a string        
        @type modName: string
        
        @return: Module handle with the specified name. None is returned if 
        the module is not found.
        """
        if modName in self.system_modules:
            #print("{} is already defined, skipping!".format(modName))
            return self.system_modules[modName]
        try:
            module = importlib.import_module(modName)
            self._CheckForRequiredImports(module)
            self.system_modules[modName] = module
            return module
        except ImportError:
            print("Unable to import module {}!".format(modName))
            return None

    
    def _ImportSysMods(self, modsFile):
        """
        Reads a text file containing the names of all system modules. All 
        lines in this file should be started with "System=" and then a 
        comma separated list of required modules. Any comment lines should 
        start with "#". This function returns a list of all modules found
        
        @param modsFile: The path to the configuration file.        
        @type modsFile: string
        
        @return: Returns a list of all lines containing the word "System" 
        at the beginning. 
        """
        lines = self._ConfigFileParse("System", modsFile)
        print("Importing:")
        for line in lines:
            for module in line:
                print("\t{}".format(module))
                self._ImportSystemModule(module)

        return lines

    
    def _ImportTabModule(self, tabMod, frameName):
        """
        Imports a a module that will be displayed as a tab under a given frame. 
        Returns the module if the import  is successful. Otherwise, "None" is 
        returned.
        
        @param tabMod: The tab module you wish to import.
        @type tabMod: string
        
        @param frameName: The frame under which the tab will appear.
        @type frameName: string
        
        @return: The tab Module specified. None is returned if tabMod is not found
        """
        if self.tab_modules.has_key(frameName):   # Check if a dictionary key for frame name has been created yet
            pass
        else:
            self.tab_modules[frameName] = []      # Create an entry if one doesn't already exist.

        try:
            module = importlib.import_module(tabMod)    # Attempt to import the specified tab module
        except ImportError:
            print("Unable to import tab {}".format(tabMod))
            return None

        self._CheckForRequiredImports(module)            # Check imports required by the tab module
        self.tab_modules[frameName].append(module)    # Add the tab module to the appropriate frame
        return module

   
    def _ImportTabMods(self, modsFile):
        """
        Reads a text file containing frame module info and imports those 
        that are specified.
        
        @param modsFile: The file containing the configuration for frame modules.
        @type modsFile: string        
        """
        mods = self._ConfigFileParse("Frame", modsFile)
        print("Importing Tabs:")
        for item in mods:
            info = self._readFrameParams(item)
            name = info.pop("name")
            
            modules = []
            tabs = info.pop("tabs")
            if type(tabs) is "list":
                modules = tabs
            else:
                modules.append(tabs)
            
            print("\t{}".format(name))
            self.frame_parameters[name] = info
          
            for module in modules:
                try:
                    self._ImportTabModule(module,  name)
                except:
                    print("Could not import tab {}".format(module))
            
                


    def _readFrameParams(self, confList):
        """
        returns a dictionary containing the info from a frame configuration list. 
        This function should be used in the ImportFrameMods function. It is 
        expecting a list returned from _ConfigFileParser.
        
        @param confList: A frame configuration list generated form parsing a configuration file.
        @type confList: list
        
        @return: A dictionary containing the parameters for all frames listed to initialize on 
        start up.
        """
        returnDict = {}
        for item in confList:
            item = item.split(":")
            assert(len(item) > 1)

            # assign new names for clarity
            key = item[0]
            value = item[1]

            if value.count(';'):
                value = value.split(';')
                try:        # Attempt to convert to integers
                    for num in range(len(value)):
                        value[num] = int(value[num])    # convert string numbers to integers
                except:
                    pass    # Do nothing if conversion fails

            returnDict[key] = value
        return returnDict


    def _SetPaths(self, dirsFile):
        """
        Appends all paths listed in a config file to the system path variable. 
        Paths should be listed in absolute or relative terms separated by commas. 
        The key "dirs =" should be placed in front of any path list in the config 
        file.
        
        @param dirsFile: The path to the config file.
        @type dirsFile: string
        
        @return: A list of all directories to be added to the python path
        """
        lines = self._ConfigFileParse("dirs", dirsFile)
        for line in lines:
            for item in line:
                sys.path.append(item)

        return lines

    
    def _ConfigFileParse(self, key, confFile):
        """
        Parses through a configuration file looking for the given key at the 
        beginning of a line. Returns a list of values given after the specified 
        key. This will only find keys followed by an "=".
        
        @param key: The line identifier that the function will search for. Should 
        be passed as a string.    ex. System, dirs
        @type key: string
        
        @param confFile: The directory of the configuration file.
        @type confFile: string
        
        @return: A list of all items from a config file that were preceded by the 
        given key.
        """
        try:
            f = open(confFile)
            data = f.readlines()
            f.close()
            values = []

            for line in data:
                line = line.replace("\n", "")       # Remove carriage returns
                line = line.replace("\t", "")       # Remove all tabs
                line = line.strip()                 # Remove leading and trailing spaces

                if (line.lower()).startswith(key.lower()):      # look for key match
                    if "#" in line:
                        line = line[:line.find("#")]            # Remove all text after a "#"

                    line = line[len(key):]          # Remove key from beginning of line
                    line = line.replace("=", "")    # Remove "=" signs
                    line = line.strip()             # Remove leading and trailing spaces
                    line = line.split(",")          # split into individual values

                    for index in range(len(line)):
                        line[index] = line[index].strip()

                    values.append(line)

            return values

        except:
            print("Could not open file {}".format(confFile))


    def _SetRequiredCoreModules(self, textEdit, frame, tab, controls):
        """
        Used to set required variables within the master object.
        
        @param textEdit:
        @type textEdit: string
        
        @param frame:
        @type frame: string
        
        @param tab:
        @type tab: string
        
        @param controls:
        @type controls: string
        """
        self.text_editor = self.system_modules[textEdit]
        self.mf = self.system_modules[frame]
        self.mt = self.system_modules[tab]
        self.mc = self.system_modules[controls]


    def _CheckForRequiredImports(self, module):
        """
        Looks at an imported module and checks if any additional support modules 
        are needed. If additional modules are needed they are imported and added 
        to the system_modules dictionary.
        
        @param module: The name of the module that will be checked for additional
        required imports.
        @type module: A handle to a module that has already been imported.
        """
        try:
            reqMods = module.required_modules   # Attempt to find required_modules variable

        except AttributeError:
            return                              # Assume no imports are needed if variable not found.

        for modName in reqMods:
            self._ImportSystemModule(modName)


    def _CheckBoundaries(self, frameSize):
        """
        Compares the frame size, the current frame position and screen size to make 
        sure the frame will not be off the screen. Returns a tuple for the recommended 
        location to draw the frame.
        
        @param frameSize: The size of the frame to be drawn. (width, height)
        @type frameSize: tuple 
        
        @return: A tuple of the suggested location to draw the frame.
        """
        if (frameSize[0] + self.frame_position[0] > self.display_size[0]):
            return (0, self.frame_position[1])
        elif (frameSize[1] + self.frame_position[1] > self.display_size[1]):
            return (self.frame_position[0], 0)
        else:
            return self.frame_position


    def _MakeFrames(self):
        """
        Creates all frames and associated tabs specified in modules.txt. 
        """
        for fname in self.tab_modules.keys():    
            if 'size' in self.frame_parameters[fname] :
                self.MakeFrame(fname, size=self.frame_parameters[fname]['size'], visible = False)
            else :
                self.MakeFrame(fname, visible = False)

        print('Executing configuration routines for each tab:')
        print('\t')

        for frame in self.frame_objects.values():
            frame.MakeTabs(self)
        
        print('')
        print('The module marina is complete.\n\n')

    def _DisplayFrames(self) :
        """
        Displays all frames located in frame_objects.
        """
        for f in self.frame_objects.values() :   # Show all the frames.
            # XP initially stacks all the controls on a tab in the upper left corner.
            # When the size of the frame is reduced to near zero and then expanded, everything is in the correct location.
            # Can automatic minimizing and maximizing solve the problem?  Possibilities: # f.Maximize(), f.Restore(), f.Iconize().
            if os.name == 'posix' :     # Linux renders well.
                f.Show()
            else :  
                f.Show()        # Diddle with the frame to get XP to render correctly.
                f.Iconize()     # Just minimizing and leaving it to the user to restore to the original size seems to work well.
                
                
    ###########################################################################
    #   Below here are public functions that are designed for use outside of  #
    #   the Master object.                                                    #
    ###########################################################################

 
    def GetSystemModule(self, modName=None):
        """
        Retrieves A system module of the given name.
        
        @param modName: The name of the module you wish to retrieve
        @type modName: string
        
        @return: A handle to the specified module is returned if it is found.
        If no module of the given name is found then None is returned. If no name 
        is passed, a dictionary of all imported system modules is returned.
        """
        if modName is None:
            return self.system_modules
        elif self.system_modules.has_key(modName):
            return self.system_modules[modName]
        else:
            return self._ImportSystemModule(modName)

    
    def GetTabModules(self, frameName=None):
        """
        Retrieves a list of tab modules that fall under a specified frame specified in 
        modules.txt.
        
        @param frameName: The name of the frame that you wish to get the tabs for.
        @type frameName: string
        
        @return: A dictionary of all tab modules contained under the specified frame.
        If no frame of the given name is found then None is returned. If no name 
        is passed, a dictionary of all frames and their associated tab modules is
        returned.
        """        
        if frameName is None:
            return self.tab_modules
        elif self.tab_modules.has_key(frameName):
            return self.tab_modules[frameName]
        else:
            return None

   
    def GetFrameParameters(self, frameName=None):
        """
        Retrieves a dictionary containing initialization settings for the given
        frame.
        
        @param frameName: The frame name you wish to get parameters for.
        @type frameName: string
        
        @return: A dictionary of the initialization settings for the specified frame.
        If the frame is not found, None is returned. If no frame name is specified, then
        a dictionary containing all parameters for all frames is returned.
        """
        if frameName is None:
            return self.frame_parameters
        elif self.frame_parameters.has_key(frameName):
            return self.frame_parameters[frameName]
        else:
            return None

    
    def AddFrameObj(self, name, frame):
        """
        Adds a frame to the Master object's frame_objects dictionary.
        
        @param name: The name of the frame.
        @type name: string
        
        @param frame: The frame to be added.
        @type frame: wx.Frame object
        """
        if not self.frame_objects.has_key(name):
            self.frame_objects[name] = frame
        else:
            print("A frame named \"{}\" already exists!".format(name))

    
    def GetFrameObj(self, frameName=None):
        """
        Retrieves the frame object of the given name.
        
        @param frameName: The name of the frame you wish to retrieve
        @type frameName: string
        
        @return: A wx.Frame object with the given name. If the name is not found then None is 
        returned. If no frame name is given, then a list of all frame objects is returned.
        """
        if frameName is None:
            return self.frame_objects
        elif self.frame_objects.has_key(frameName):
            return self.frame_objects[frameName]
        else:
            return None


    def RemoveFrameObj(self, frameName):
        """
        Removes the frame of the given name from the Master object's frame_objects dictionary.
        This should be called when a frame is being deleted.
        
        @param frameName: The name of the frame to remove from the dictionary.
        @type frameName: string
        """
        if self.frame_objects.has_key(frameName):
            self.frame_objects.pop(frameName)


    ###########################################################################
    #   Below here are public functions that are designed for use outside of  #
    #   the Master object.                                                    #
    ###########################################################################


    def MakeFrame(self, name, parent=None, pos=None, size=(900,700), style=wx.DEFAULT_FRAME_STYLE, visible = True):
        """
        Creates a wxWidgets frame and stores the instance in frame_objects. 
        
        @param name: The name of the frame. This name will be displayed on the title bar and 
        be used to reference the frame.
        @type name: string
        
        @param parent: The parent frame object.
        @type parent: wx.Frame object
        
        @param pos: Sets the position of the frame. If left as None the frame's location will 
        be chosen automatically.
        @type pos: tuple
        
        @param size: Sets the starting size of the frame in pixels.
        @type size: tuple
        
        @param style: Sets the frame style. For most cases this should be left as it's default value.
        @type style: int
        
        @param visible: Sets the frame visibility after its creation.
        @type visible: boolean
        
        @return: Returns the created frame object.
        """
        if pos is None:
            pos = self._CheckBoundaries(size)


        frame = self.mf.MainFrame(self, name, parent, pos, size, style, self.text_editor)
        self.frame_position = (pos[0] + 50,pos[1] + 50)
        self.AddFrameObj(name, frame)
        
        if os.name is not "posix":
            frame.Iconize()
            
        frame.Show(visible)
        return frame


    def MakeTab(self, modName, parentFrame, color = [200,200,200]):
        """
        Creates a new tab under the specified frame and configures it. If the specified parent frame 
        is not present then a new one of the given name will be created and the tab placed under it.
        
        @param modName: Name of tab module.
        @type modName: string
        
        @param parentFrame: The parent frame object.
        @type parentFrame: wx.Frame object
        
        @param color: The color of the tab window [red, green, blue]
        @type color: list
        
        @return: The tab object.
        """
        frame = self.GetFrameObj(parentFrame)

        if frame is None:
            frame = self.MakeFrame(parentFrame)
        
        return frame.MakeTab(self,  modName,  color = color)



#-----------------------------------------------------------------------
if __name__ == '__main__' :
    print('This is not the module you want. Execute control.py.')
