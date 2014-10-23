
# Add control classes below.  Modify TranslateControls to include the string to be used to translate to a new class.
# All the controls on a tab will be within a single sizer, which is passed in the function call as sizer.
# Each control lies in a subsizer which is added to the sizer.  Each control can consist of sub controls in subsubsizers.

def TranslateControls(mod_tab, tab, sizer, control_list) :
	error = ''
	for key in control_list :
		try:
			con = mod_tab.controls_defs[key]
		except :
			error = 'Error in controls_def list.  A control name is probably used twice.'
			print error
			return error
		print '\t\t\t'+ key + ' --> ' + con['type']
		if con['type'] == 'button' :
			tc = mod_tab.d.mc.Button(mod_tab.d, mod_tab.frame, mod_tab, tab, sizer, key, con)
		elif con['type'] == 'two_buttons_vertical' :
			tc = mod_tab.d.mc.TwoButtonsVertical(mod_tab.d, mod_tab.frame, mod_tab, tab, sizer, key, con)
		elif con['type'] == 'two_buttons_horizontal' :
			tc = mod_tab.d.mc.TwoButtonsHorizontal(mod_tab.d, mod_tab.frame, mod_tab, tab, sizer, key, con)
		elif con['type'] == 'text_area' :
			tc = mod_tab.d.mc.TextArea(mod_tab.d, mod_tab.frame, mod_tab, tab, sizer, key, con)
		elif con['type'] == 'text_and_button' :
			tc = mod_tab.d.mc.TextAndButton(mod_tab.d, mod_tab.frame, mod_tab, tab, sizer, key, con)
		elif con['type'] == 'text_over_two_buttons' :
			tc = mod_tab.d.mc.TextOverTwoButtons(mod_tab.d, mod_tab.frame, mod_tab, tab, sizer, key, con)
		elif con['type'] == 'static_text' :
			tc = mod_tab.d.mc.StaticText(mod_tab.d, mod_tab.frame, mod_tab, tab, sizer, key, con)
		elif con['type'] == 'combo_box' :
			tc = mod_tab.d.mc.ComboBox(mod_tab.d, mod_tab.frame, mod_tab, tab, sizer, key, con)
		elif con['type'] == 'blank' :
			tc = mod_tab.d.mc.Blank(mod_tab.d, mod_tab.frame, mod_tab, tab, sizer, key, con)
	return error



class TextArea() :
	def __init__(self, d, f, tab_obj, tab, sizer, key, con) :
		# d is the dock master object, f is the frame object.
		# tab is the tab object in a frame. sizer is the sizer within the tab to which the control will be added.
		# key is the control name.  con is the list of control specifications.
		wx = d.wx
		dim = con['dimensions']
		text_area = wx.TextCtrl(tab,-1,size=(dim[0],dim[1]),style=wx.TE_MULTILINE | wx.HSCROLL | wx.TE_READONLY)
		self.control= text_area
		tab_obj.controls[key] = text_area
		text_area_label = wx.StaticText(tab,-1,con['label'])  #, pos=plot_numbers_label_loc
		subsizer = wx.BoxSizer(wx.VERTICAL)
		subsizer.AddStretchSpacer(10)   # add a vertical spacer
		subsizer.Add(text_area_label, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10)    # border = 5, all around
		subsizer.Add(text_area, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
		#sizer.AddStretchSpacer(10)  # add a horizontal spacer to the left of subsizer
		sizer.Add(subsizer, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 0)

class StaticText():
	def __init__(self, d, f, tab_obj, tab, sizer, key, con) :
		wx = d.wx
		dim = con['dimensions']
		text_area = wx.StaticText(tab,-1, con['content'], size=(dim[0],dim[1]))
		tab_obj.controls[key]= text_area
		text_area_label = wx.StaticText(tab,-1,con['label'])  #, pos=plot_numbers_label_loc
		subsizer = wx.BoxSizer(wx.VERTICAL)
		subsizer.AddStretchSpacer(10)   # add a vertical spacer
		subsizer.Add(text_area_label, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 2)    # border = 5, all around
		subsizer.Add(text_area, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
		subsizer.AddStretchSpacer(10)  # add a horizontal spacer to the left of subsizer
		sizer.Add(subsizer, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10)

class Button() :
	def __init__(self, d, f, tab_obj, tab, sizer, key, con) :
		wx = d.wx
		demo_plot_button = wx.Button(tab,label = con['label'])
		demo_plot_button.Bind(wx.EVT_BUTTON,con['function'])
		#sizer.AddStretchSpacer(10)  # add a horizontal spacer to the left of subsizer
		sizer.Add(demo_plot_button, 1, wx.ALL,25 )

class TwoButtonsVertical() :
	def __init__(self, d, f, tab_obj, tab, sizer, key, con) :
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

class TwoButtonsHorizontal() :
	def __init__(self, d, f, tab_obj, tab, sizer, key, con) :
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

class TextAndButton() :
	def __init__(self, d, f, tab_obj, tab, sizer, key, con) :
		wx = d.wx
		dim = con['dimensions']
		if ('hscroll' in con) and (con['hscroll'] == True) :
			hscroll = wx.HSCROLL
		else :
			hscroll = 0
		text_area = wx.TextCtrl(tab,-1,size=(dim[0],dim[1]),style=wx.TE_MULTILINE | hscroll)
		tab_obj.controls[key]= text_area
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

class TextOverTwoButtons() :
	def __init__(self, d, f, tab_obj, tab, sizer, key, con) :
		wx = d.wx
		dim = con['dimensions']
		if ('hscroll' in con) and (con['hscroll'] == True) :
			hscroll = wx.HSCROLL
		else :
			hscroll = 0
		text_area = wx.TextCtrl(tab,-1,size=(dim[0],dim[1]),style=wx.TE_MULTILINE | hscroll)
		tab_obj.controls[key]= text_area
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

class Blank() :
	def __init__(self, d, f, tab_obj, tab, sizer, key, con) :
		wx = d.wx
		sizer.AddStretchSpacer(10)  # add a horizontal spacer to the subsizer

class ComboBox() :
	def __init__(self, d, f, tab_obj, tab, sizer, key, con) :
		wx = d.wx
		dim = con['dimensions']
		combo_box = wx.ComboBox(tab, size=(dim[0], dim[1]), name=con['label'], style=wx.CB_DROPDOWN)
		if 'function' in con :
			combo_box.Bind(wx.EVT_COMBOBOX, con['function'])
		tab_obj.controls[key] = combo_box
		combo_box_label = wx.StaticText(tab,-1,con['label'])  #, pos=plot_numbers_label_loc
		subsizer = wx.BoxSizer(wx.VERTICAL)
		subsizer.AddStretchSpacer(10)   # add a vertical spacer
		subsizer.Add(combo_box_label, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)    # border = 5, all around
		subsizer.Add(combo_box, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10)
		sizer.Add(subsizer, 0, wx.ALL, 20)

