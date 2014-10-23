
# Add control-generating functions below.  Modify TranslateControls to include the string to be used to translate to a new control.
# All the controls on a tab will be within a single sizer, which is passed in the function call as sizer.
# Each control lies in a subsizer which is added to the sizer.  Each control can consist of sub controls in subsubsizers.

def TranslateControls(tab, sizer, control_list) :
	error = ''
	for key in control_list :
		try:
			con = tab.controls[key]
		except :
			error = 'Error in controls_def list.  A control name is probably used twice.'
			print error
			return error
		print '\t\t\t'+ key + ' --> ' + con['type']
		if con['type'] == 'button' :
			Button(tab.GetDock(), tab.GetParent(), tab, sizer, key, con)
		elif con['type'] == 'two_buttons_vertical' :
			TwoButtonsVertical(tab.GetDock(), tab.GetParent(), tab, sizer, key, con)
		elif con['type'] == 'two_buttons_horizontal' :
			TwoButtonsHorizontal(tab.GetDock(), tab.GetParent(), tab, sizer, key, con)
		elif con['type'] == 'four_buttons_square' :
			FourButtonsSquare(tab.GetDock(), tab.GetParent(), tab, sizer, key, con)
		elif con['type'] == 'text_area' :
			TextArea(tab.GetDock(), tab.GetParent(), tab, sizer, key, con)
		elif con['type'] == 'text_and_button' :
			TextAndButton(tab.GetDock(), tab.GetParent(), tab, sizer, key, con)
		elif con['type'] == 'text_over_two_buttons' :
			TextOverTwoButtons(tab.GetDock(), tab.GetParent(), tab, sizer, key, con)
		elif con['type'] == 'static_text' :
			StaticText(tab.GetDock(), tab.GetParent(), tab, sizer, key, con)
		elif con['type'] == 'combo_box' :
			ComboBox(tab.GetDock(), tab.GetParent(), tab, sizer, key, con)
		elif con['type'] == 'blank' :
			Blank(tab.GetDock(), tab.GetParent(), tab, sizer, key, con)
	return error



def TextArea(d, f, tab, sizer, key, con) :
		# d is the dock master object, f is the frame object.
		# tab is the tab object in a frame. sizer is the sizer within the tab to which the control will be added.
		# key is the control name.  con is the list of control specifications.
		wx = d.wx
		dim = con['dimensions']
		style = 0
		if  ('read_only' in con) and con['read_only'] :
			style = style | wx.TE_READONLY
		if  ('scroll' in con) and con['scroll'] :
			style = style | wx.HSCROLL
		if  ('multiline' in con) and con['multiline'] :
			style = style | wx.TE_MULTILINE
		text_area = wx.TextCtrl(tab,-1,size=(dim[0],dim[1]),style=style)
		tab.controls[key] = text_area
		text_area_label = wx.StaticText(tab,-1,con['label'])  #, pos=plot_numbers_label_loc
		subsizer = wx.BoxSizer(wx.VERTICAL)
		subsizer.AddStretchSpacer(10)   # add a vertical spacer
		subsizer.Add(text_area_label, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10)    # border = 5, all around
		subsizer.Add(text_area, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
		#sizer.AddStretchSpacer(10)  # add a horizontal spacer to the left of subsizer
		sizer.Add(subsizer, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 0)

def StaticText(d, f, tab, sizer, key, con) :
		wx = d.wx
		dim = con['dimensions']
		text_area = wx.StaticText(tab,-1, con['content'], size=(dim[0],dim[1]))
		tab.controls[key]= text_area
		text_area_label = wx.StaticText(tab,-1,con['label'])  #, pos=plot_numbers_label_loc
		subsizer = wx.BoxSizer(wx.VERTICAL)
		subsizer.AddStretchSpacer(10)   # add a vertical spacer
		subsizer.Add(text_area_label, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 2)    # border = 5, all around
		subsizer.Add(text_area, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
		subsizer.AddStretchSpacer(10)  # add a horizontal spacer to the left of subsizer
		sizer.Add(subsizer, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10)

def Button(d, f, tab, sizer, key, con) :
		wx = d.wx
		demo_plot_button = wx.Button(tab,label = con['label'])
		demo_plot_button.Bind(wx.EVT_BUTTON,con['function'])
		#sizer.AddStretchSpacer(10)  # add a horizontal spacer to the left of subsizer
		sizer.Add(demo_plot_button, 1, wx.ALL,25 )

def TwoButtonsVertical(d, f, tab, sizer, key, con) :
		wx = d.wx
		button_1 = wx.Button(tab,label = con['label_1'])
		button_1.Bind(wx.EVT_BUTTON,con['function_1'])
		button_2 = wx.Button(tab,label = con['label_2'])
		button_2.Bind(wx.EVT_BUTTON,con['function_2'])
		subsizer = wx.BoxSizer(wx.VERTICAL)
		subsizer.Add(button_1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
		subsizer.Add(button_2, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
		#sizer.AddStretchSpacer(10)  # add a horizontal spacer to the left of subsizer
		sizer.Add(subsizer, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 10 )

def TwoButtonsHorizontal(d, f, tab, sizer, key, con) :
		wx = d.wx
		button_1 = wx.Button(tab,label = con['label_1'])
		button_1.Bind(wx.EVT_BUTTON,con['function_1'])
		button_2 = wx.Button(tab,label = con['label_2'])
		button_2.Bind(wx.EVT_BUTTON,con['function_2'])
		subsizer = wx.BoxSizer(wx.HORIZONTAL)
		subsizer.Add(button_1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
		subsizer.Add(button_2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
		#sizer.AddStretchSpacer(10)  # add a horizontal spacer to the left of subsizer
		sizer.Add(subsizer, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10 )

def FourButtonsSquare(d, f, tab, sizer, key, con) :
		wx = d.wx
		for i in range(1, 5) :
			labl = 'label_'+str(i).strip()
			func = 'function_'+str(i).strip()
			if labl not in con :
				con[labl] = 'Undefined Action'
			if func not in con :
				con[func] = None
		button_1 = wx.Button(tab,label = con['label_1'])
		button_1.Bind(wx.EVT_BUTTON,con['function_1'])
		button_2 = wx.Button(tab,label = con['label_2'])
		button_2.Bind(wx.EVT_BUTTON,con['function_2'])
		button_3 = wx.Button(tab,label = con['label_3'])
		button_3.Bind(wx.EVT_BUTTON,con['function_3'])
		button_4 = wx.Button(tab,label = con['label_4'])
		button_4.Bind(wx.EVT_BUTTON,con['function_4'])
		subsizer = wx.FlexGridSizer(2,2,5,5)	# rows = 2, columns = 2
		#subsizer = wx.BoxSizer(wx.VERTICAL)
		#subsubsizer1 = wx.BoxSizer(wx.HORIZONTAL)
		subsizer.Add(button_1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
		subsizer.Add(button_2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
		subsizer.Add(button_3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
		subsizer.Add(button_4, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
		#sizer.AddStretchSpacer(10)  # add a horizontal spacer to the left of subsizer
		sizer.Add(subsizer, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10 )

def TextAndButton(d, f, tab, sizer, key, con) :
		wx = d.wx
		dim = con['dimensions']
		if ('hscroll' in con) and (con['hscroll'] == True) :
			hscroll = wx.HSCROLL
		else :
			hscroll = 0
		text_area = wx.TextCtrl(tab,-1,size=(dim[0],dim[1]),style=wx.TE_MULTILINE | hscroll)
		tab.controls[key]= text_area
		text_area_label = wx.StaticText(tab,-1,con['label'])  #, pos=plot_numbers_label_loc
		subsizer = wx.BoxSizer(wx.VERTICAL)
		subsizer.AddStretchSpacer(10)   # add a vertical spacer
		subsizer.Add(text_area_label, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 2)    # border = 5, all around
		subsizer.Add(text_area, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
		button = wx.Button(tab,label = con['button_label'])
		button.Bind(wx.EVT_BUTTON,con['function'])
		subsizer.Add(button, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
		#sizer.AddStretchSpacer(10)  # add a horizontal spacer to the left of subsizer
		sizer.Add(subsizer, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)

def TextOverTwoButtons(d, f, tab, sizer, key, con) :
		wx = d.wx
		dim = con['dimensions']
		if ('hscroll' in con) and (con['hscroll'] == True) :
			hscroll = wx.HSCROLL
		else :
			hscroll = 0
		text_area = wx.TextCtrl(tab,-1,size=(dim[0],dim[1]),style=wx.TE_MULTILINE | hscroll)
		tab.controls[key]= text_area
		text_area_label = wx.StaticText(tab,-1,con['label'])  #, pos=plot_numbers_label_loc
		subsizer = wx.BoxSizer(wx.VERTICAL)
		subsizer.AddStretchSpacer(10)   # add a vertical spacer
		subsizer.Add(text_area_label, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 2)    # border = 5, all around
		subsizer.Add(text_area, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
		subsubsizer = wx.BoxSizer(wx.HORIZONTAL)
		button_1 = wx.Button(tab,label = con['button_label_1'])
		button_1.Bind(wx.EVT_BUTTON,con['function_1'])
		subsubsizer.Add(button_1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
		button_2 = wx.Button(tab,label = con['button_label_2'])
		button_2.Bind(wx.EVT_BUTTON,con['function_2'])
		subsubsizer.Add(button_2, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
		subsizer.Add(subsubsizer, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
		#sizer.AddStretchSpacer(10)  # add a horizontal spacer to the left of subsizer
		sizer.Add(subsizer, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)

def Blank(d, f, tab, sizer, key, con) :
		wx = d.wx
		sizer.AddStretchSpacer(10)  # add a horizontal spacer to the subsizer

def ComboBox(d, f, tab, sizer, key, con) :
		wx = d.wx
		dim = con['dimensions']
		combo_box = wx.ComboBox(tab, size=(dim[0], dim[1]), name=con['label'], style=wx.CB_DROPDOWN)
		if 'function' in con :
			combo_box.Bind(wx.EVT_COMBOBOX, con['function'])
		tab.controls[key] = combo_box
		combo_box_label = wx.StaticText(tab,-1,con['label'])  #, pos=plot_numbers_label_loc
		subsizer = wx.BoxSizer(wx.VERTICAL)
		subsizer.AddStretchSpacer(10)   # add a vertical spacer
		subsizer.Add(combo_box_label, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)    # border = 5, all around
		subsizer.Add(combo_box, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10)
		sizer.Add(subsizer, 0, wx.ALL, 20)

