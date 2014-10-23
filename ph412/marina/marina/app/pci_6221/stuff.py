
import nidaqmx as mx

class TranslatedStuff() :
	def __init__(self, dll) :
		#The dll will be the nidaqmx dll.
		#self.Val_RSE = dll.DAQmx_Val_RSE		# 10083 = 10083
		self.CreateTask = dll.DAQmxCreateTask          	# (const char taskName[], TaskHandle *taskHandle);

def Test() :
	dll, message = mx.LoadDLL()
	print dll.DAQmxCreateTask
	print dll.DAQmx_Val_RSE
	t = TranslatedStuff(dll)
	print t.CreateTask

#------------------------------------------------------------------

if __name__ == '__main__' :
	Test()
