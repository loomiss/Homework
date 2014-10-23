
import functions

class FakeDLL():
	def __init__(self) :
		self.DAQmxLoadTask = 1           		# DAQmxLoadTask(constchartaskName[],TaskHandle*taskHandle);
		self.DAQmxCreateTask  = 2         		# DAQmxCreateTask(constchartaskName[],TaskHandle*taskHandle);

dll = FakeDLL()
d = functions.TranslatedFunctions(dll)
print dir(d)
print d.LoadTask
