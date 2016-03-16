import wx
import wx.lib.filebrowsebutton as filebrowse
import time
import check_station_info
import download_csv_files

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
        
        # Top entry field. Station Name:Text Entry:Go Button (Bound to onGo function)
        self.stat_text = wx.StaticText(self.panel, -1, "Station Name:")
        self.stat_txt_field = wx.TextCtrl(self.panel, -1, "Station Name here")        
        self.stat_text_go = wx.Button(self.panel, -1, "Go")
        self.Bind(wx.EVT_BUTTON, self.onGo, self.stat_text_go)
        
        # Second entry field. Station ID:Text Entry:Go Button (Bound to onGo function)
        self.stat_id_text = wx.StaticText(self.panel, -1, "Station ID:")
        self.stat_id_txt_field = wx.TextCtrl(self.panel, -1, "Station ID here")
        self.stat_id_text_go = wx.Button(self.panel, -1, "Go")
        self.Bind(wx.EVT_BUTTON, self.onGo, self.stat_id_text_go)
        
        # Adding all items created to the FlexGridSizer
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
        self.dirbox = wx.BoxSizer(wx.VERTICAL)
    
        self.dbb = filebrowse.DirBrowseButton(self.panel, -1)
        self.dbb.SetValue("Choose Directory To Save Files")
        self.dirbox.Add(self.dbb, 1, wx.ALL|wx.EXPAND|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
   
        self.text_to_screen = '' # Placeholder for creating dialogue box.
        self.dlgbox = wx.TextCtrl(self.panel, -1, self.text_to_screen, style=wx.TE_READONLY|wx.TE_MULTILINE)
   
        # Add the FlexGrid (Station Name and Station ID)/Top
        # Adds another BoxSizer for displaying feedback and instructions to the User/Bottom
        self.topsizer.Add(self.boxes, 0, wx.EXPAND)
        self.topsizer.Add(self.dirbox, 0, wx.EXPAND)
        self.topsizer.Add(self.dlgbox, 1, wx.EXPAND)
        
        self.panel.SetSizerAndFit(self.topsizer) 
        
    def onGo(self, e):
        # On click of Go button, get directory adn station name and check database.
        name = self.stat_txt_field.GetValue()
        dirname = self.dbb.GetValue()
        station_name, station_id = check_station_info.GUI_test(name, dirname)
        print station_name, station_id, dirname
        
    def dlg_test(self):
        

        
app = wx.App()

frame = MainWindow(None, "Climate Canada GUI").Show()

app.MainLoop()