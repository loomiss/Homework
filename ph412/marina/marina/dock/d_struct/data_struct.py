
import wx.lib.dialogs as wd	# Not the same a importing as a system module for some unknown reason.
import time
from datetime import datetime
import numpy

required_modules = ['numpy']

# Description --------------------------------------------------------------------------------------------------------------

# Data structure management module.

#---------------------------------------------------------------------------------------------------------------------------



class DataStructureManager() :

	def __init__(self, dock) :
		self.dock = dock
		self.version = '1'
		self.name = 'data_struct'
		self.version = '1'
		self.cds = []	# The central data structure

class DataSet() :
	
	def __init__(self, dsm) :
		dsm.cds.append(self)	# Add this data set objec to the central data structure.
		self.name = ''
		self.date = datetime.now().isoformat()
		self.title = ''
		self.description = ''
		self.dims = 0	# number of dimensions
		self.vectors = 0	# number of data points
		self.dim_defs = []	# A dimension can be time, potential, distance, position, current, ... .
		self.dim_units = []
		self.np = numpy		#dsm.dock.system_modules['numpy']
		self.data = self.np.array([])	# Example: array([x, y1, y2])
		
		self.options = {}
		self.options['author'] = ''
		self.graph_objs = []		# List of graph objects that have provided useful graphs.
		"""
		# Example of the graph objec self.
        self.data = data			# list of [x,y] pairs.
        self.graph = graph
        self.symbols = symbols      # a list of symbols: ['o', ''] for default color circles and lines,  or ['bo, 'go'] for blue and green circles
        self.styles = styles
        self.colors = colors
        self.grid = grid
        self.title = title
        self.titlesize = titlesize
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.labelsize = labelsize
        self.ticklabelsize = ticklabelsize
        self.colorbar = colorbar
        self.background = background
        self.text = text
        self.textsize = textsize
        self.legend = legend
        self.customize = customize
        """
		

def Test():
	dsm = DataStructureManager('dock')
	dset = DataSet(dsm)
	print dset.date
	print dsm.cds
	
#-----------------------------------------------------------------------

if __name__ == '__main__' :
	Test()
