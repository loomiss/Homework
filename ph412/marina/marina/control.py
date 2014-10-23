#! /usr/bin/env python
"""
Use this module to start Marina.
"""

# Set the path to marina, either absolute or relative to your application directory.
core_path = ''

# Do not change anything below this line.
core_path.strip()
if core_path.endswith('/') :
    dock_path = core_path + 'dock'
else :
    if len(core_path) > 0 :
        core_path += '/'
        dock_path = core_path + 'dock'
    else :
        dock_path = 'dock'
from sys import path
path.append(dock_path)
import dock

#-----------------------------------------------------------------------
if __name__ == '__main__' :
    d = dock.Master('modules.txt', core_path)
    
