import wx.lib.dialogs as wd	# Not the same a importing as a system module for some unknown reason.
from datetime import datetime

required_modules = ['awg_devices']

# Description --------------------------------------------------------------------------------------------------------------

#test module

#---------------------------------------------------------------------------------------------------------------------------

class Generic() :

	def __init__(self, dock) :
		self.dock = dock
		self.wx = dock.wx
		self.version = '1'
		self.name = 'awg_devices'
		self.display_name = 'Arbitrary Waveform Generators'
		self.content = 'This module communicates via USB with arbitrary waveform generators (function generators).'
		self.about = "Module: awg_devices\n" \
		+ "Purpose: Basic waveform generator communication.\n"\
		+ "Authors:\t W. Hetherington\n" \
		+ "Created:\t 2011/10/17\n" \
		+ "Copyright:\t (c) 2011\n" \
		+ "License:\t No restrictions\n"
		self.active_device = ' '	# name of selected scope
		self.awg_list = []	# list of names
		self.awgs = {}		# (name : handle ) pairs
		self.this_dir = 'app/awg'
		self.syntax_file = 'awg_syntax.txt'
		self.help = 'waveform_generators_help.txt'
		self.save_file = 'data.csv'
		self.save_directory = 'data'
		self.delay_by_vendor = {'rig' : 0.3, 'tek' : 0.1}	# in seconds
		self.delay = 0.5
		# Define the controls.  The order in which they are defined determines the placement on the grid.
		self.controls = {}
		self.ctl_count = 0
		self.DefineControl('setup', {'format':'control_2', 'tab':'yes', 'rows':3, 'columns':3})
		self.DefineControl('find_devices', {'type':'text_and_button','dimensions':[175,70],'label':'Arbitrary Waveform Generators Found','button_label':'Find Instruments','function':self.FindDevices})
		self.DefineControl('select_device', {'type':'combo_box', 'dimensions':[200,25],'label':'Select Device', 'function':self.OnSelectDevice})
		self.DefineControl('device_properties', {'type':'text_area', 'dimensions':[200, 150], 'read_only':True, 'scroll':True, 'multiline':True, 'label':'Selected Instrument Properties'})
		self.DefineControl('delay', {'type':'text_area', 'dimensions':[50, 30], 'read_only':False, 'scroll':False, 'multiline':False, 'label':'Delay Between Instructions'})
		self.DefineControl('device_commands', {'type':'text_and_button','dimensions':[250,100],'hscroll':True,'label':'Command String','button_label':'Send','function':self.OnSendCommands})
		self.DefineControl('device_reply', {'type':'text_and_button','dimensions':[300,50],'hscroll':True,'label':'Instrument Reply','button_label':'Read', 'function':self.GetReply})
		self.DefineControl('blank_1', {'type':'blank'})
		#self.DefineControl('device_parameters', {'type':'text_and_button','dimensions':[200,70],'label':'Selected Device Parameters','button_label':'Get Parameters', 'function':self.DeviceParameters})
		#self.DefineControl('channels', {'type':'text_area', 'dimensions':[100, 30], 'read_only':False, 'scroll':False, 'multiline':False, 'label':'Specify Analog Input Channel\n\t\t(0-15)'})
		#self.DefineControl('sample_rate', {'type':'text_area', 'dimensions':[100, 30], 'read_only':False, 'scroll':False, 'multiline':False, 'label':'Specify Sample Rate\n(samples/second)'})
		#self.DefineControl('samples', {'type':'text_area', 'dimensions':[100, 30], 'read_only':False, 'scroll':False, 'multiline':False, 'label':'Specify Number of Samples\n\t to Acquire'})
		#self.DefineControl('adc_range', {'type':'text_area', 'dimensions':[100, 30], 'read_only':False, 'scroll':False, 'multiline':False, 'label':'Specify Analog Input Range\n(2, 5, 10, assumed bipolar)'})
		#self.DefineControl('frequency', {'type':'text_area', 'dimensions':[100, 30], 'read_only':False, 'scroll':False, 'multiline':False, 'label':'Input Signal Frequency\n(used only for the plot title)'})
		#self.DefineControl('button_block', {'type':'four_buttons_square', 'label_1':'Acquire and Plot', 'function_1':self.OnAcquire, 'label_2':'Autocorrelation', 'function_2':self.OnAutocorrelate, 'label_3':'Synchronous Detection', 'function_3':self.OnSynchronous, 'label_4':'Reset Device', 'function_4':self.OnResetDevice})
		##self.DefineControl('acquire', {'type':'button', 'label':'Acquire and Plot', 'function':self.OnAcquire})
		#self.DefineControl('save_button', {'type':'button', 'label':'Save File', 'function':self.OnSave})
		##self.DefineControl('blank_1', {'type':'blank'})
		##self.DefineControl('blank_2', {'type':'blank'})
		##self.DefineControl('blank_3', {'type':'blank'})
		##self.DefineControl('blank_4', {'type':'blank'})
		self.DefineControl('blank_2', {'type':'blank'})
		self.DefineControl('about_button', {'type':'button', 'label':'About This Module', 'function':self.OnAbout})
		self.DefineControl('help_button', {'type':'button', 'label':'Help', 'function':self.OnHelp})

	def DefineControl(self, ctl_name, c) :
		if ctl_name.lower() != 'setup' :
			c['order'] = self.ctl_count
			self.ctl_count += 1
		self.controls[ctl_name] = c

	def PostCreationConfigure(self) :
		# Label some system or tabbed modules which will be used.
		#self.wd = self.dock.system_modules['wx.lib.dialogs']	# This is a different module?
		self.tab = self.dock.tabs[self.name]
		self.wd = wd
		self.time = self.dock.system_modules['time']
		self.awg_devices = self.dock.system_modules['awg_devices']
		self.np = self.dock.system_modules['numpy']
		# Define the control boxes AFTER the controls have been created.
		self.find_devices_box = self.tab.controls['find_devices']
		self.select_device_box = self.tab.controls['select_device']
		self.device_properties = self.tab.controls['device_properties']
		self.delay_box = self.tab.controls['delay']
		self.commands_box = self.tab.controls['device_commands']
		self.reply_box = self.tab.controls['device_reply']
		self.response_spectrum_selected_awg = self.dock.tabs['response_spectrum'].controls['selected_awg']
		#self.parameters_box = self.tab.controls['device_parameters']
		#self.channels_box = self.tab.controls['channels']
		#self.sample_rate_box = self.tab.controls['sample_rate']
		#self.samples_box = self.tab.controls['samples']
		#self.adc_range_box = self.tab.controls['adc_range']
		#self.frequency_box = self.tab.controls['frequency']
		# Refer to attributes in another module object which is an attribute of the associated tab.  Tricky.
		# Default parameters
		#self.ain_channel = 0
		#self.channels_box.SetValue(str(self.ain_channel))
		#self.sample_rate = 200000	#float(self.tab.controls['sample_rate'].GetValue())
		#self.sample_rate_box.SetValue(str(self.sample_rate))
		#self.samples = 10000	#int(self.tab.controls['samples'].GetValue())
		#self.samples_box.SetValue(str(self.samples))
		#self.adc_range = 2.0	#float(self.tab.controls['adc_range'].GetValue())
		#self.adc_range_box.SetValue(str(self.adc_range))
		#self.applied_freq = 30000	#int(self.tab.controls['frequency'].GetValue())
		#self.frequency_box.SetValue(str(self.applied_freq))
		syntax_file = self.dock.dirs[self.this_dir] + '/' + self.syntax_file
		self.syntax = self.ParseSyntaxFile(syntax_file)
		print('\nSyntax dictionary:')
		print self.syntax


	def FindDevices(self, event) :
		#the_box = self.dock.modules[self.name]['find_instruments']
		message = ''
		self.device_list = []
		#self.scopes = {}
		try :
			self.devices = self.awg_devices.FindDevices(self.dock.usb_instruments)
			self.select_device_box.Clear()
			for key in self.devices :
				message += key + '\n'
				self.select_device_box.Append(key)
				self.device_list.append(key)
		except :
			message = 'FindDevices error.\nMissing import?\nMissing instruments?\n'
			#try :
				#self.scopes = self.tek_fake.FindTDS1012B()
				#self.select_scope_box.Clear()
				#for key in self.scopes :
					#message += key + '\n'
					#self.select_scope_box.Append(key)
					#self.scope_list.append(key)
			#except :
				#message += 'Simulation module is not functional.\n'
		self.find_devices_box.SetValue(message)

	def OnSelectDevice(self, event):
		self.selected_device_identity = self.select_device_box.GetCurrentSelection()
		self.active_device = self.device_list[self.selected_device_identity]
		#print self.active_device
		self.response_spectrum_selected_awg.SetValue(self.active_device)
		self.device = self.devices[self.active_device]
		device_properties = self.device.idn + '\n'
		self.device.protocol = self.device.device['vendor'].lower()[0:3]
		for p in self.device.device :
			#print p, self.device.device[p]
			if p != 'handle' :
				device_properties += p + ' : ' + str(self.device.device[p]) + '\n'
		self.device_properties.SetValue(device_properties)
		try :
			self.delay = self.delay_by_vendor[self.device.device['vendor'].lower()[0:3]]
		except :
			pass
		self.delay_box.SetValue(str(self.delay))
		self.commands_box.Clear()

	def ParseSyntaxFile(self, syntax_file) :
		infile = open(syntax_file, 'r')
		file_lines = infile.readlines()
		infile.close()
		syntax = {}
		protocol = '?'
		sub_syntax = {}
		for aline in file_lines :
			al = aline.split('#')[0].strip()     # Ignore comment fields.
			#print al
			if len(al) > 0 :    # Ignore comment lines.
				# Check for a change in category indicated by a leading >.
				if al.lower().startswith('protocol') :
					b = al.split('=')[1].strip().lower()
					if protocol != '?' :
						syntax[protocol] = sub_syntax
					protocol = b
					sub_syntax = {}
				else :
					c = al.split('=')
					sub_syntax[c[0].strip()] = c[1].strip()
		syntax[protocol] = sub_syntax
		return syntax

	def OnSendCommands(self, event) :
		commands = self.commands_box.GetValue().split('\n')
		self.delay = float(self.delay_box.GetValue())
		self.SendCommands(self.device, self.delay, commands)
		#for c in commands :
			#d = c.split('#')[0].strip()
			#if len(d) > 0 :
				#self.devices[self.active_device].Write(d)
				#self.time.sleep(self.delay)
		return

	def SendCommands(self, device, delay, command_list) :
		for m in command_list :
			commands = m.split('\n')
			for c in commands :
				d = c.split('#')[0].strip()
				if len(d) > 0 :
					device.Write(d)
					self.time.sleep(delay)
		return

	def GetReply(self, event) :
		reply = ''
		reply += self.devices[self.active_device].Read() + '\n'
		self.reply_box.SetValue(reply)
		return

	def OnAbout(self, event):
		#d = self.wx.MessageDialog( self.dock.modules[self.name]['tab'], self.about, "About Scope", self.wx.ICON_INFORMATION)  # Create a message dialog box
		#print self.name
		#print self.dock.tabs[self.name].tab
		d = self.wx.MessageDialog( self.tab.tab, self.about, "About " + self.display_name, self.wx.ICON_INFORMATION)  # Create a message dialog box
		d.ShowModal() # Show it.
		d.Destroy() # Destroy it when finished.

	def OnHelp(self, event):
		#d = self.wx.MessageDialog( self.dock.modules[self.name]['tab'], self.about, "About Scope", self.wx.ICON_INFORMATION)  # Create a message dialog box
		try :
			help = self.dock.dirs[self.this_dir] + '/' + self.help		#self.dock.dirs['help'] + '/' + self.help
			f = open(help)
			help_caption = self.name
			help_me = f.read()
			f.close()
			#d = self.wx.MessageDialog( self.dock.tabs[self.name].tab, help_me, "Scope Help", self.wx.ICON_INFORMATION)  # Create a message dialog box
			d = self.wd.ScrolledMessageDialog(self.tab.tab, help_me, caption=help_caption, pos=(100,100), size=(800,500))#, style=self.wx.HSCROLL)
			d.ShowModal() # Show it.
			d.Destroy() # Destroy it when finished.
		except :
			print('Help file error.')
			#help = self.dock.dirs['help'] + '/' + 'generic_help.txt'
			#f = open(help)
			#help_caption = 'generic_help.txt'

	def DeviceParameters(self, event) :
		self.parameters_box.SetValue('Working ... \n')
		message = ''
		message = self.mx.GetDeviceParameters(self.active_device)
		self.parameters_box.SetValue(message)
		return

	def OnAcquire(self, event) :
		ain_channel = int(self.channels_box.GetValue())
		sample_rate = float(self.sample_rate_box.GetValue())
		samples = int(self.samples_box.GetValue())
		adc_range = float(self.adc_range_box.GetValue())
		applied_freq = int(self.frequency_box.GetValue())
		# Call to simple returns [[t, signal], [freq, power]] and graphing lables, which might be useful when saving a file.
		self.data_arrays, self.graph_labels = self.simple(self, self.device, self.active_device, ain_channel, sample_rate, samples, adc_range, applied_freq)
		self.date = datetime.now().isoformat()

	def OnAutocorrelate(self, event) :
		return

	def OnSynchronous(self, event) :
		return

	def OnResetDevice(self, event) :
		self.mx.ResetDevice(self.active_device, self.device)
		print self.device, self.active_device

	def OnSave(self, event) :
		d = self.wx.FileDialog(self.tab.frame, 'Save File', self.save_directory, self.save_file, '*', self.wx.FD_SAVE | self.wx.FD_OVERWRITE_PROMPT, self.wx.DefaultPosition)
		if d.ShowModal() == self.wx.ID_OK : # Show it.
			self.save_directory = d.GetDirectory()
			self.save_file = d.GetFilename()
			self.save_path = d.GetPath()
			o = open(self.save_path, 'w')
			header = '# ' + self.date + '\n'
			header += '# Acquired by pci6221.py\n'
			for key in self.graph_labels :
				header += '# ' + key + '\n'
				for i in range(len(self.graph_labels[key])) :
					header += '#\t' + self.graph_labels[key][i] + '\n'
			header += '\n# Begin data: time '
			for i in range(1, len(self.data_arrays[0])) :
				header += 'signal, '
			header += '\n'
			o.write(header)
			#print 'j : ', len(self.data_arrays)
			#print 'k : ', len(self.data_arrays[0])
			#print 'i : ', len(self.data_arrays[0][0])
			for i in range(len(self.data_arrays[0][0])) :
				stuff = ''
				for k in range(len(self.data_arrays[0])) :
						stuff += str(self.data_arrays[0][k][i]) + ', '
				stuff = stuff[:-2] + '\n'
				o.write(stuff)
			#for i in range(len(self.data_arrays[0][0])) :
				#stuff = ''
				#for j in range(len(self.data_arrays)) :
					#for k in range(len(self.data_arrays[0])) :
						#try :
							#stuff += str(self.data_arrays[k][j][i]) + ', '
						#except :
							#pass
				#stuff = stuff[:-2] + '\n'
				#o.write(stuff)
			o.close()
		d.Destroy() # Destroy it when finished.

# The setup routine must be in each application module. --------------------------------------------

def setup(dock) :
    # Create the module object associated with a tab of a similar name.
	object = Generic(dock)	# The module object will be aware of dock.
	return object

# Optional test routines ---------------------------------------------------------------------------

def Test() :
	print 'This is not the module you want.  Execute control.py'

#---------------------------------------------------------------------------------------------------------------------------

#  Execute
if __name__ == '__main__':
    Test()



