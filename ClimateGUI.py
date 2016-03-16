import wx


class MainWindow(wx.Frame):
    
    def __init__(self, parent, title):
        
        super(MainWindow, self).__init__(parent, title=title)
        
        self.CreateStatusBar()
        
        # Panel used for all Control items (Buttons, Text, Lists, etc)
        self.panel = wx.Panel(self, wx.ID_ANY)
        
        self.topsizer = wx.BoxSizer(wx.VERTICAL)
        
        self.boxes = wx.FlexGridSizer(2, 3)
        
        self.stat_text = wx.StaticText(self.panel, -1, "Station Name")
        self.stat_txt_field = wx.TextCtrl(self.panel, -1, "Enter Station Name here")
        self.stat_text_go = wx.Button(self.panel, -1, "Go")
      
        self.boxes.AddMany([ 
                            (self.stat_text, 0, wx.ALL|wx.ALIGN_CENTER, 5),
                            (self.stat_txt_field, 1, wx.ALL|wx.EXPAND, 5),
                            (self.stat_text_go, 0, wx.ALL|wx.ALIGN_RIGHT, 5)
                          ])
        
        self.stat_id_text = wx.StaticText(self.panel, -1, "Station ID")
        self.stat_id_txt_field = wx.TextCtrl(self.panel, -1, "Enter Station ID here")
        self.stat_id_text_go = wx.Button(self.panel, -1, "Go")
        
        self.boxes.AddMany([ 
                            (self.stat_id_text, 0, wx.ALL|wx.ALIGN_CENTER, 5),
                            (self.stat_id_txt_field, 1, wx.EXPAND|wx.ALL, 5),
                            (self.stat_id_text_go, 0, wx.ALIGN_RIGHT|wx.ALL, 5)
                          ])
        
        self.boxes.AddGrowableCol(1)
        
        self.topsizer.Add(self.boxes, 0, wx.EXPAND)
        self.topsizer.Add(wx.TextCtrl(self.panel, -1, '', style=wx.TE_MULTILINE), 1, wx.EXPAND)
        
        self.panel.SetSizerAndFit(self.topsizer)

        self.Show()
        
app = wx.App()

frame = MainWindow(None, "Sample GUI")

app.MainLoop()