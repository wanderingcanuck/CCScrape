import wx
import wx.lib.filebrowsebutton as filebrowse

class MainWindow(wx.Frame):
    
    def __init__(self, parent, title):
        
        super(MainWindow, self).__init__(parent, title=title, size=(600, 400))
        
        self.CreateStatusBar()
        
        # Panel used for all Control items (Buttons, Text, Lists, etc)
        self.panel = wx.Panel(self, wx.ID_ANY)
        
        # Main BoxSizer for Main Window
        self.topsizer = wx.BoxSizer(wx.VERTICAL)
        
        # GridSizer for Input fields for Station Name and Station ID (as well as buttons)
        self.boxes = wx.FlexGridSizer(2, 3)
        
        self.stat_text = wx.StaticText(self.panel, -1, "Station Name:")
        self.stat_txt_field = wx.TextCtrl(self.panel, -1, "Station Name here")
        self.stat_text_go = wx.Button(self.panel, -1, "Go")

        self.stat_id_text = wx.StaticText(self.panel, -1, "Station ID:")
        self.stat_id_txt_field = wx.TextCtrl(self.panel, -1, "Station ID here")
        self.stat_id_text_go = wx.Button(self.panel, -1, "Go")
        
        self.boxes.AddMany([ 
                            (self.stat_text, 0, wx.ALL|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 5),
                            (self.stat_txt_field, 1, wx.ALL|wx.EXPAND, 5),
                            (self.stat_text_go, 0, wx.ALL|wx.ALIGN_RIGHT, 5),
                            (self.stat_id_text, 0, wx.ALL|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 5),
                            (self.stat_id_txt_field, 1, wx.EXPAND|wx.ALL, 5),
                            (self.stat_id_text_go, 0, wx.ALIGN_RIGHT|wx.ALL, 5)
                          ])
        
        self.boxes.AddGrowableCol(1) # Allows the text fields (Station Name and Station ID) to be stretchable
        
        # Creating the Choose File Directory box

        self.dirbox = wx.BoxSizer(wx.HORIZONTAL)
    
        self.dbb = filebrowse.DirBrowseButton(self.panel, -1)
        self.dbb.SetValue("Choose Directory To Save Files")
        self.dirbox.Add(self.dbb, 1, wx.ALL|wx.EXPAND|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
   
        # Add the FlexGrid (Station Name and Station ID)/Top
        # Adds another BoxSizer for displaying feedback and instructions to the User/Bottom
        self.topsizer.Add(self.boxes, 0, wx.EXPAND)
        self.topsizer.Add(self.dirbox, 0, wx.EXPAND)
        self.topsizer.Add(wx.TextCtrl(self.panel, -1, '', style=wx.TE_READONLY|wx.TE_MULTILINE), 1, wx.EXPAND)
        
        self.panel.SetSizerAndFit(self.topsizer) 

        self.Show()
        
app = wx.App()

frame = MainWindow(None, "Climate Canada GUI")

app.MainLoop()