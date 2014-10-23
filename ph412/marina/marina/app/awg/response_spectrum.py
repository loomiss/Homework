
import wx.lib.dialogs as wd	# Not the same a importing as a system module for some unknown reason.

required_modules = ['waveform_generators', 'awg_devices', 'tek_scopes', 'tek1012b', 'notebook_plots_base', 'notebook_plots_graph','wx.lib.dialogs']
required_modules.append('response_plot_files')

# Description --------------------------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------------------------------

class Generic() :

	def __init__(self, dock) :
		self.dock = dock
		self.wx = dock.wx
		self.version = '1'
		self.name = 'response_spectrum'
		self.display_name = 'Response Spectrum'
		self.content = 'This module will scan the frequency of an arbitrary waveform generator, acquire waveforms from a specified oscilloscope and determine the response function A(frequency).'
		self.about = "Module: response_spectrum \n" \
			+ "Purpose: Response spectrum using an AWG and an oscilloscope.\n"\
			+ "Authors:\t W. Hetherington\n" \
			+ "Created:\t 2011/10/17\n" \
			+ "Copyright:\t (c) 2011\n" \
			+ "License:\t No restrictions\n"
		self.help = 'response_spectrum_help.txt'
		self.save_file = 'data.csv'
		self.save_directory = 'data'
		self.read_directory = ''
		self.read_file = ''
		self.read_file_ext = '*'#'|*.csv|*.dat|*.txt|'	#'csv files (*.csv)|*.csv |'	# txt files (*.txt)|*.txt | dat files (*.dat)|*.dat |'
		# Define the controls.  The order in which they are defined determines the placement on the grid.
		self.controls = {}
		self.ctl_count = 0
		self.DefineControl('setup', {'format':'control_2', 'tab':'yes', 'rows':4, 'columns':4})
		self.DefineControl('selected_scope', {'type':'text_area','dimensions':[200,40],'label':'Oscilloscope Identity'})
		self.DefineControl('selected_awg', {'type':'text_area','dimensions':[200,40],'label':'Waveform Generator Identity'})
		self.DefineControl('scan_parameters_file',  {'type':'text_and_button','dimensions':[250,30],'label':'Scan Parameters File','button_label':'Select','function':self.OnRead})
		self.DefineControl('scan_button', {'type':'button', 'label':'Scan', 'function':self.OnScan})
		self.DefineControl('fft_plot_buttons', {'type':'two_buttons_vertical', 'label_1':r'Power Spectrum vs Log(Freq)', 'function_1':self.OnPowerSpectrumLog, \
			'label_2':r'Power Spectrum vs Freq', 'function_2':self.OnPowerSpectrumLinear})
		self.DefineControl('plot_xy_button', {'type':'button', 'label':'Plot XY Mode', 'function':self.OnPlotXY})
		#self.DefineControl('decadic_frequency_range', {'type':'text_area', 'dimensions':[100, 30], 'read_only':False, 'scroll':False, 'multiline':False, 'label':'Frequency\n(used only for the plot title)'})
		self.DefineControl('blank_1', {'type':'blank'})
		#self.DefineControl('simple_plot_buttons', {'type':'two_buttons_vertical', 'label_1':'Plot Channels(t)', 'function_1':self.OnPlotChannels, \
		#	'label_2':'Plot XY Mode', 'function_2':self.OnPlotXY})
		#self.DefineControl('fft_plot_buttons', {'type':'two_buttons_vertical', 'label_1':r'Power Spectrum vs Log(Freq)', 'function_1':self.OnPowerSpectrumLog, \
		#	'label_2':r'Power Spectrum vs Freq', 'function_2':self.OnPowerSpectrumLinear})
		#self.DefineControl('plot_xy_button', {'type':'button', 'label':'Plot XY Mode', 'function':self.OnPlotXY})
		#self.DefineControl('save_button', {'type':'button', 'label':'Save File', 'function':self.OnSave})
		#self.DefineControl('open_spreadsheet', {'type':'button', 'label':'Open Spreadsheet', 'function':self.OnSpreadsheet})
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
		self.np = self.dock.system_modules['numpy']
		self.time = self.dock.system_modules['time']
		self.rpf = self.dock.system_modules['response_plot_files']
		self.io = self.dock.system_modules['scan_2_io']
		self.scope_tab = self.dock.tabs['tek_scopes']	#self.dock.frame_modules['Oscilloscope Signals']['tek_scopes']
		self.scope_module = self.scope_tab.module_object
		print dir(self.scope_module)
		self.awg_tab = self.dock.tabs['waveform_generators']	#self.dock.frame_modules['Waveform Generation and Response Scans']['waveform_generators']
		self.awg_module = self.awg_tab.module_object
		self.scan_parameters_box = self.tab.controls['scan_parameters_file']
		self.x = self.np.array([])
		self.ys = []
		self.chans = ['1', '2']
		#self.SetChannelsString()
		self.filein = ''	# Will be replaced by a filein object.
		# Define the control boxes AFTER the controls have been created.  Place references to other modules at the end of this list.
		self.selected_scope_box = self.dock.tabs[self.name].controls['selected_scope']
		self.selected_awg_box = self.dock.tabs[self.name].controls['selected_awg']
		#self.parameters_box = self.dock.tabs[self.name].controls['scope_parameters']
		# Refer to attributes in another module object which is an attribute of the associated tab.  Tricky.
		#self.active_scope = self.dock.tabs['tek_scopes'].module_object.active_scope
		self.scopes = self.dock.tabs['tek_scopes'].module_object.scopes
		#self.active_scope_obj = self.dock.tabs['tek_scopes'].module_object.scopes[self.active_scope]

	def SetChannelsString(self) :
		channels_string = self.chans[0]
		for ch in self.chans[1:] :
			channels_string += ', ' + ch
		self.tab.controls['channels'].SetValue(channels_string)

	def OnAbout(self, event):
		d = self.wx.MessageDialog( self.tab.tab, self.about, "About Response Spectrum", self.wx.ICON_INFORMATION)  # Create a message dialog box
		d.ShowModal() # Show it.
		d.Destroy() # Destroy it when finished.

	def OnHelp(self, event):
		#d = self.wx.MessageDialog( self.dock.modules[self.name]['tab'], self.about, "About Scope", self.wx.ICON_INFORMATION)  # Create a message dialog box
		try :
			help = self.dock.dirs['app/awg'] + '/' + self.help		#self.dock.dirs['help'] + '/' + self.help
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

	def OnError(self, error) :
		d = self.wx.MessageDialog( self.dock.tabs[self.name].tab, error, "You made a mistake.", self.wx.ICON_ERROR)  # Create a message dialog box
		d.ShowModal() # Show it.
		d.Destroy() # Destroy it when finished.

	def Notify(self, message) :
		d = self.wx.MessageDialog( self.dock.tabs[self.name].tab, message, "There is a problem.", self.wx.ICON_INFORMATION)  # Create a message dialog box
		d.ShowModal() # Show it.
		d.Destroy() # Destroy it when finished.

	def OnScan(self, event) :
		#self.active_scope = self.selected_scope_box.GetValue()
		#self.active_awg = self.selected_awg_box.GetValue()
		#if (self.active_scope.strip() == '') :
			#self.OnError('Find and select an oscilloscope first.')
			#return
		try :
			self.active_scope = self.dock.tabs['tek_scopes'].module_object.active_device
			self.active_scope_obj = self.dock.tabs['tek_scopes'].module_object.device
			self.active_awg = self.dock.tabs['waveform_generators'].module_object.active_device
			self.active_awg_obj = self.dock.tabs['waveform_generators'].module_object.device
		except :
			self.OnError('Active oscilloscope and/or waveform generator object(s) are/is not defined.')
			return
		self.scan_parameters_file = self.scan_parameters_box.GetValue().strip()
		if self.scan_parameters_file == '' :
			OnError('Scan parameters file has not been specified')
			return
		#self.tab.frame.Hide() # not a good idea.
		busy = self.wx.BusyInfo("Data acquisition in progress ... ", self.tab.frame)
		self.Scan(self.active_awg_obj, self.active_scope_obj, self.scan_parameters_file)
		busy.Destroy()
		return
		self.wx.Yield()		# necessary, otherwise busyinfo display is empty on Linux.
		self.dock.tabs['tek_scopes'].module_object.ScopeParameters(None)	# Update parameters.
		error = ''
		error, self.x, y1 = self.active_scope_obj.GetWaveform(self.active_scope_obj.ch1, 'binary')
		if error :
			self.OnError(error)
			return
		error, self.x, y2 = self.active_scope_obj.GetWaveform(self.active_scope_obj.ch2, 'binary')
		if error :
			self.OnError(error)
			return
		self.ys = [y1, self.np.power(y2, 2)]
		#print len(y1), len(y2)
		#print self.ys
		#self.d.system_modules['time'].sleep(3)
		busy.Destroy()
		#self.tab.frame.Show()
		return

	def SendCommandString(self, device, delay, command_list) :
		for m in command_list :
			commands = m.split('\n')
			for c in commands :
				d = c.split('#')[0].strip()
				if len(d) > 0 :
					device.Write(d)
					self.time.sleep(delay)
		return

	def Scan(self, fg, scope, parameters_file) :
		#FGScopeScan('C031180')
		#fg, scope = InitializeDevices('C031180', 'C055976')
		#fg, scope = FindDevices('C031180', 'C055976')

		#inst, op, error, warning = ReadParametersFile('scan_2_parameters.txt', 'scan_2.py')
		#inst, op, error, warning = ReadParametersFile('scan_2_parameters_bjt_ce_amplifier.txt', 'scan_2.py')
		#inst, op, error, warning = ReadParametersFile('scan_2_parameters_jfet_cd_amplifier.txt', 'scan_2.py')
		inst, op, error, warning = self.io.ReadParametersFile(parameters_file, 'scan_2.py')
		if error : print error
		if warning : print warning
		#print inst
		#print op
		# initialize instruments
		self.scope_delay_box = self.scope_tab.controls['delay']
		self.awg_delay_box = self.awg_tab.controls['delay']
		self.scope_delay = float(self.scope_delay_box.GetValue())
		self.awg_delay = float(self.awg_delay_box.GetValue())
		self.awg_protocol = self.active_awg_obj.protocol
		self.scope_protocol =  self.active_scope_obj.protocol
		self.awg_module.SendCommands(self.active_scope_obj, self.scope_delay, inst['scope']['com'])
		self.awg_module.SendCommands(self.active_awg_obj, self.awg_delay, inst['fg']['com'])
		return
		fg, error = FindTekInstrument(inst['fg']['id'])
		scope, error = FindTekInstrument(inst['scope']['id'])
		if op.has_key('scan variable') :
			if op['scan variable'][0] == 'frequency' :
				FrequencyScanAndPlot(fg, scope, inst, op)
		else :
			print 'Scan variable not specified. Frequency is assumed.'
			FrequencyScanAndPlot(fg, scope, inst, op)

	def OnRead(self, event) :
		self.error = ''
		d = self.wx.FileDialog(self.tab.frame, 'Read Scan Parameter File', self.read_directory, self.read_file, self.read_file_ext, self.wx.FD_OPEN, self.wx.DefaultPosition)
		if d.ShowModal() != self.wx.ID_OK : # Show it.
			return self.error
		self.read_directory = d.GetDirectory()
		self.read_file = d.GetFilename()
		self.read_path = d.GetPath()
		f = open(self.read_path, 'r')
		self.scan_parameters = f.readlines()	#self.rpf.DataFromFile(self.read_path, ',')
		f.close()
		self.scan_parameters_box.SetValue(self.read_file)
		return self.error


	def OnSave(self, event) :
		#self.wd.saveFileDialog(parent, title, directory, filename, wildcard, style)
		d = self.wx.FileDialog(self.tab.frame, 'Save File', self.save_directory, self.save_file, '*', self.wx.FD_SAVE | self.wx.FD_OVERWRITE_PROMPT, self.wx.DefaultPosition)
		if d.ShowModal() == self.wx.ID_OK : # Show it.
			self.save_directory = d.GetDirectory()
			self.save_file = d.GetFilename()
			self.save_path = d.GetPath()
			o = open(self.save_path, 'w')
			o.write('# Channel information:\n')
			for i in range(len(self.chans)) :
				o.write('#\tChannel '+str(self.chans[i])+' : '+self.scope_chans[i].xunit+', '+self.scope_chans[i].yunit+'\n')
			o.write('\n# x value followed by y for each channel:\n')
			for i in range(len(self.x)) :
				dat = str(self.x[i])
				for y in self.ys:
					dat += ',' + str(y[i])
				dat += '\n'
				o.write(dat)
			o.close()
		d.Destroy() # Destroy it when finished.

	def OnSpreadsheet(self, event) :
		if self.dock.os == 'win' :
			#self.Notify('Accessing Excel via PyWin32 is not yet implemented.')
			spread = []		# Index will be spreadsheet row.
			spread.append(['Channel information:'])
			for i in range(len(self.chans)) :
				spread.append(['Channel '+str(self.chans[i])+' : '+self.scope_chans[i].xunit+', '+self.scope_chans[i].yunit])
			spread.append(['x value followed by y for each channel:'])
			for i in range(len(self.x)) :
				temp = []
				temp.append(self.x[i])
				for y in self.ys:
					temp.append(y[i])
				spread.append(temp)
			self.dock.system_modules['excel'].MakeSheet(self.wx, self.tab, spread)
		else :
			self.Notify('This control is not yet functional')

	def OnPlotChannels(self, event) :
		if len(self.chans) == 0 :
			self.OnError('Nothing to plot.  Channel list is empty.')
			return
		b = self.dock.system_modules['notebook_plots_base']
		g = self.dock.system_modules['notebook_plots_graph']
		f = b.PlotFrame(title='Channels versus Time', size=(800,800))
		plist = []
		legends = []
		for i in range(len(self.chans)) :
			if int(self.chans[i]) == 1 :
				xunit = self.active_scope_obj.ch1.xunit
				yunit = self.active_scope_obj.ch1.yunit
			else :
				xunit = self.active_scope_obj.ch2.xunit
				yunit = self.active_scope_obj.ch2.yunit
			yunit = yunit.strip()[0]
			chvt = g.Graph('plot', [[self.x, self.ys[i]]], symbols=['b','g'], grid=False, title = 'Ch '+self.chans[i]+' vs Time', titlesize=24,\
				background='w', xlabel=r'Time ('+xunit+')', ylabel=r'Signal ('+yunit+')', labelsize=18, ticklabelsize=14, customize=None)#, legend=[r'1', r'2'])
			g.DefineTab(f, [chvt], name='Channel '+self.chans[i]+' vs Time')
			plist.append([self.x, self.ys[i]])
			legends.append(self.chans[i])
		allchvt = g.Graph('plot', plist, symbols=['','', '', ''], grid=False, title = 'All Channels vs Time', background='w', \
			xlabel=r'Time ('+xunit+')', ylabel=r'Signal ('+yunit+')', labelsize=18, ticklabelsize=14, customize=None)#, legend=['1','2'])
		g.DefineTab(f, [allchvt], name='All Channels vs Time')
		f.Show()

	def OnPlotXY(self, event) :
		b = self.dock.system_modules['notebook_plots_base']
		g = self.dock.system_modules['notebook_plots_graph']
		f = b.PlotFrame(title='XY Mode Plots', size=(800,800))
		yunit = self.active_scope_obj.ch1.yunit
		#yunit = self.active_scope_obj.ch2.yunit
		yunit = yunit.strip()[0]
		for i in range(2) :
			for j in range(i+1, len(self.chans)) :
				chjvchi = g.Graph('plot', [[self.ys[i], self.ys[j]]], symbols=['b','g'], grid=True, \
					title = 'Ch '+self.chans[j]+' vs Ch '+self.chans[i], background='w', xlabel=r'Ch '+self.chans[i]+' ('+yunit+')', \
					ylabel=r'Ch '+self.chans[j]+' ('+yunit+')', labelsize=25, customize=None)	#, legend=[r'1', r'2']
				g.DefineTab(f, [chjvchi], name='Channel '+self.chans[j]+' vs Channel '+self.chans[i])
		f.Show()

	def OnPowerSpectrumLog(self, event) :
		self.PowerSpectrum(self.np.log10)
		return

	def OnPowerSpectrumLinear(self, event) :
		self.PowerSpectrum(None)
		return

	def PowerSpectrum(self, x_axis_transform) :
		#self.Notify('Not yet functional.')
		tp = []
		if len(self.ys) == 0 :
			self.OnError('There is no data to transform.')
			return
		b = self.dock.system_modules['notebook_plots_base']
		g = self.dock.system_modules['notebook_plots_graph']
		f = b.PlotFrame(title='Power Spectra', size=(800,800))
		symbols = ['', '', '', '', '']
		grid = True
		titlesize = 24
		background = 'w'
		if x_axis_transform == None :
			xlabel = r'$\nu$ (Hz)'
		else :	# assume log10
			xlabel = r'Log($\nu$)'
		ylabel = r'Power Density'
		labelsize = 18
		ticklabelsize = 14
		customize = None
		#legend=[r'1', r'2']
		#for i in range(len(self.chans)) :
		tp = []
		for i in range(len(self.ys)) :
			t = self.dock.system_modules['response_plot'].PowerSpectrum(self.x, self.ys[i])
			if x_axis_transform :
				t[0] = x_axis_transform(t[0])
			title = 'Power spectrum for Ch ' + self.chans[i]
			tab_name = title
			chps = g.Graph('plot', [t], symbols=symbols, grid=grid, title=title, titlesize=titlesize, background=background, \
				xlabel=xlabel, ylabel=ylabel, labelsize=labelsize, ticklabelsize=ticklabelsize, customize=customize)
			g.DefineTab(f, [chps], name=tab_name)
			tp.append(t)
			#legends.append(self.chans[i])
		title = 'Power Spectrum for all Channels'
		tab_name = title
		allchps = g.Graph('plot', tp, symbols=symbols, grid=grid, title=title, titlesize=titlesize, background=background, \
				xlabel=xlabel, ylabel=ylabel, labelsize=labelsize, ticklabelsize=ticklabelsize, customize=customize)
		g.DefineTab(f, [allchps], name=tab_name)
		f.Show()


	def OnNothing(self, event) :
		return

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
