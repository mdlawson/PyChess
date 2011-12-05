import wx

class mainGUI(wx.Frame):
	def __init__(self, *args, **kwargs):
		super(mainGUI, self).__init__(*args, **kwargs) 
		self.InitUI()
		
	def InitUI(self):    
		menubar = wx.MenuBar()
		fileMenu = wx.Menu()
		fitem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
		menubar.Append(fileMenu, '&File')
		self.SetMenuBar(menubar)
		self.Bind(wx.EVT_MENU, self.OnQuit, fitem)
		self.SetSize((300, 450))
		self.SetTitle('PyChess')
		self.Centre()
		self.Show(True)
	def OnQuit(self, e):
		self.Close()

pyChess = wx.App()
mainGUI(None)
pyChess.MainLoop()    
