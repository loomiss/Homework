
import constants

class FakeDLL():
	def __init__(self) :
		self.DAQmx_Buf_Input_BufSize = 6252
		self.DAQmx_Buf_Input_OnbrdBufSize = 8970

dll = FakeDLL()
d = constants.TranslatedConstants(dll)
print dir(d)
print d.Buf_Input_BufSize
