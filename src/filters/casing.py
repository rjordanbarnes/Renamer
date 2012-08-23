import wx


class Casing(wx.Panel):
    def __init__(self, parent, files):
        wx.Panel.__init__(self, parent)
        wx.StaticText(self, -1, "Change Casing of text", (60, 60))
