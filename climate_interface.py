# Climate Canada GUI interface

import wx

app = wx.App()
win = wx.Frame(None, title="Download Weather Station Records", size=(600, 400))

bkg = wx.Panel(win)

tx_stat_name = wx.StaticText(bkg, label="This is a test.")
tx_stat_id = wx.StaticText(bkg, label="This is another test.")

box = wx.BoxSizer(wx.HORIZONTAL)
box.Add(tx_stat_id, 0, border=5)

box.Add(tx_stat_name, -1, border=5)
# tx_stat_name = wx.StaticText(win, pos=(0,0), label="This is a test.").Wrap(10) # .Wrap(self, width) wraps the text


win.Show()
app.MainLoop()