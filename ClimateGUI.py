import wx
import wx.lib.filebrowsebutton as filebrowse
import time
import ClimateGUIcheck
import download_csv_files
import shelve

class MainWindow(wx.Frame):
    
    def __init__(self, parent, title):
        
        super(MainWindow, self).__init__(parent, title=title, size=(800, 600))
        
        self.CreateStatusBar()
        
        # Panel used for all Control items (Buttons, Text, Lists, etc)
        self.panel = wx.Panel(self, wx.ID_ANY)
        
        # Main BoxSizer for Main Window
        self.topsizer = wx.BoxSizer(wx.VERTICAL)
        
        # GridSizer for Input fields for Station Name and Station ID (as well as buttons)
        self.boxes = wx.FlexGridSizer(1, 3)
        
        # Top entry field. Station Name:Text Entry:Go Button (Bound to onGo function)
        self.stat_text = wx.StaticText(self.panel, -1, "Station Name:")
        self.stat_txt_field = wx.TextCtrl(self.panel, -1, "Station Name here")        
        self.stat_text_go = wx.Button(self.panel, -1, "Go")
        self.Bind(wx.EVT_BUTTON, self.onGo, self.stat_text_go)
        
        # Adding all items created to the FlexGridSizer
        self.boxes.AddMany([ 
                            (self.stat_text, 0, wx.ALL|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 3),
                            (self.stat_txt_field, 1, wx.ALL|wx.EXPAND, 3),
                            (self.stat_text_go, 0, wx.ALL|wx.ALIGN_RIGHT, 3),
                          ])
        
        self.boxes.AddGrowableCol(1) # Allows the text fields (Station Name and Station ID) to be stretchable
        
        # Creating the Choose File Directory box
        self.dirbox = wx.BoxSizer(wx.VERTICAL)
    
        self.dbb = filebrowse.DirBrowseButton(self.panel, -1)
        self.dbb.SetValue("Choose Directory To Save Files")
        self.dirbox.Add(self.dbb, 1, wx.ALL|wx.EXPAND|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
   
        self.text_to_screen = '' # Placeholder for creating dialogue box.
        self.dlgbox = wx.TextCtrl(self.panel, -1, self.text_to_screen, style=wx.TE_READONLY|wx.TE_MULTILINE)
   
        # Add the FlexGrid (Station Name and Station ID)/Top
        # Adds another BoxSizer for displaying feedback and instructions to the User/Bottom
        self.topsizer.Add(self.boxes, 0, wx.EXPAND)
        self.topsizer.Add(self.dirbox, 0, wx.EXPAND)
        self.topsizer.Add(self.dlgbox, 1, wx.EXPAND)
        
        self.panel.SetSizerAndFit(self.topsizer) 
        
    def onGo(self, e):
    
        station_name, station_ids = self.check_valid_name()

        if station_ids:
            if len(station_ids) > 1:
                self.multipleStations(station_name, station_ids)
            elif len(station_ids) == 1: 
                print "Just one Station Id"
            else: 
                print "Something went wrong at onGo"
        else: 
            print "Station ID not found."

        
        # self.test_case()
    
            
    def check_valid_name(self):
        station_name = str(self.stat_txt_field.GetValue())
        return station_name, ClimateGUIcheck.checkStationName(station_name)
        
        
    def multipleStations(self, station_name, station_ids):
    
        db = shelve.open("climate_data.dat", 'r')
        
        db_list = db.get(station_name)
        
        print db_list

        # Dialog Window for selecting Station Name from list of Stations with same name.
        dlg = wx.Dialog(self.panel, -1, "Choose Station From List", size=(400, 300))
        
        # Main BoxSizer
        self.topbox = wx.BoxSizer(wx.VERTICAL)
  
        # Creation of Window Objects, and adding them to the Dialog Window
        self.dlg_text = wx.StaticText(dlg, -1, "There are multiple stations by the name of {}.\nPlease select the Weather Station from the list below.".format(station_name))   
        self.placeholder = wx.StaticText(dlg, -1, "PlaceHolder Text")
        
        self.dlg_list = wx.ListCtrl(dlg, -1, style=wx.LC_REPORT)
        
        self.dlg_list.InsertColumn(0, "Station")
        self.dlg_list.InsertColumn(1, "Hourly")
        self.dlg_list.InsertColumn(2, "Daily")
        self.dlg_list.InsertColumn(3, "Monthly")
        self.dlg_list.InsertColumn(4, "Station ID")
        self.dlg_list.InsertColumn(5, "Province")

        for num in range(len(db_list)):
            value = db_list[num]
            self.dlg_list.InsertStringItem(num, station_name)
            hly, dly, mly, stat_id, prov = value

            self.dlg_list.SetStringItem(num, 1, hly)
            self.dlg_list.SetStringItem(num, 2, dly)
            self.dlg_list.SetStringItem(num, 3, mly)
            self.dlg_list.SetStringItem(num, 4, stat_id)
            self.dlg_list.SetStringItem(num, 5, prov)          
        
        self.buttonbox = wx.BoxSizer(wx.HORIZONTAL)
        self.dlg_OK = wx.Button(dlg, wx.ID_OK)
        self.dlg_Cancel = wx.Button(dlg, wx.ID_CANCEL)
        
        self.buttonbox.Add(self.dlg_OK, 0, wx.ALL, 5)
        self.buttonbox.Add(self.dlg_Cancel, 0, wx.ALL, 5)
        
        self.topbox.AddMany([
                           (self.dlg_text, 1, wx.ALL|wx.ALIGN_CENTER, 10),
                           (self.placeholder, 1, wx.ALL|wx.ALIGN_CENTER, 5),                           
                           (self.dlg_list, 2, wx.ALL|wx.ALIGN_CENTER, 5),                           
                           (self.buttonbox, 1, wx.ALL|wx.ALIGN_CENTER, 5),
                           ])
        
        dlg.SetSizerAndFit(self.topbox)
        
        dlg.Centre()
        
        # Show the Dialog window as Modal(), which means user MUST hit OK or Cancel.
        # If user hit ok...
        if dlg.ShowModal() == wx.ID_OK:
            print 'Hello'
            
        dlg.Centre()
            
        dlg.Destroy()
        
        db.close()
        
    def test_case(self):
    
        db = shelve.open("climate_data.dat", 'r')
        
        db_list = db.items()
    
        # Dialog Window for selecting Station Name from list of Stations with same name.
        dlg = wx.Dialog(self.panel, -1, "Choose Station From List", size=(600, 400))
        
        # Main BoxSizer
        self.topbox = wx.BoxSizer(wx.VERTICAL)
  
        # Creation of Window Objects, and adding them to the Dialog Window
        self.dlg_text = wx.StaticText(dlg, -1, "Testing")   
        
        self.dlg_list = wx.ListCtrl(dlg, -1, style=wx.LC_REPORT)
        
        self.dlg_list.InsertColumn(0, "Station")
        self.dlg_list.InsertColumn(1, "Hourly")
        self.dlg_list.InsertColumn(2, "Daily")
        self.dlg_list.InsertColumn(3, "Monthly")
        self.dlg_list.InsertColumn(4, "Station ID")
        self.dlg_list.InsertColumn(5, "Province")

        for num in range(len(db_list)):
            key, value = db_list[num]
                    
            self.dlg_list.InsertStringItem(num, key)
            hly, dly, mly, stat_id, prov = value[0]

            self.dlg_list.SetStringItem(num, 1, hly)
            self.dlg_list.SetStringItem(num, 2, dly)
            self.dlg_list.SetStringItem(num, 3, mly)
            self.dlg_list.SetStringItem(num, 4, stat_id)
            self.dlg_list.SetStringItem(num, 5, prov)  
            
        self.topbox.AddMany([
                           (self.dlg_text, 1, wx.ALL|wx.ALIGN_CENTER, 5),
                           (self.dlg_list, 3, wx.ALL|wx.EXPAND, 5)
                           ])
        
        # dlg.SetSizerAndFit(self.topbox)

        dlg.SetSizer(self.topbox)
        
        dlg.Centre()
        
        db.close()
        
        # Show the Dialog window as Modal(), which means user MUST hit OK or Cancel.
        # If user hit ok...
        if dlg.ShowModal() == wx.ID_OK:
            print 'Hello'
            
        dlg.Destroy()
        
        
        
app = wx.App()

frame = MainWindow(None, "Climate Canada GUI").Show()

app.MainLoop()