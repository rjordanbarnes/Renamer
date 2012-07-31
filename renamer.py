import wx
import os
import socket
import threading
import random

TITLE = "Renaming Tool"
WIDTH = 800
HEIGHT = 600

class MainFrame(wx.Frame):
    def __init__(self, parent, title, width, height):
        wx.Frame.__init__(self, parent, title=title, size=(width, height), style=wx.DEFAULT_FRAME_STYLE)
        self.Center()
        self.initializeMenuBar()
        self.initializeContents()
        
    def initializeMenuBar(self):
        '''Initializes the important UI stuff.'''
        # File Menu entries.
        fileMenu = wx.Menu()
        menuOpen = fileMenu.Append(wx.ID_OPEN, 'Open', '')
        fileMenu.AppendSeparator()
        menuExit = fileMenu.Append(wx.ID_EXIT, 'Exit', '')
        
        # Help Menu entries.
        helpMenu = wx.Menu()
        menuAbout = helpMenu.Append(wx.ID_ABOUT, 'About', '')
        
        # Creates the Menu Bar and adds the top-level menu entries.
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, 'File')
        menuBar.Append(helpMenu, 'Help')
        self.SetMenuBar(menuBar)
        
        # Binds events to buttons on the Menu Bar.
        self.Bind(wx.EVT_MENU, self.openFolder, menuOpen)
        self.Bind(wx.EVT_MENU, self.exitProgram, menuExit)
        self.Bind(wx.EVT_MENU, self.aboutProgram, menuAbout)
        
    def initializeContents(self):
        # Splits controls from work area.
        splitterSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(splitterSizer)
        
        # Splits Main buttons from Tabs.
        categorySplitter = wx.BoxSizer(wx.VERTICAL)
        splitterSizer.Add(categorySplitter, flag=wx.EXPAND)
        
        # General, Music, and Videos buttons.
        categorySizer = wx.GridSizer(rows=1, cols=3, vgap=0, hgap=1)
        
        categorySizer.AddMany( [(wx.Button(self, label='General', size=(100,40)), 0, wx.SHAPED),
                                (wx.Button(self, label='Music', size=(100,40)), 0, wx.SHAPED),
                                (wx.Button(self, label='Videos', size=(100,40)), 0, wx.SHAPED) ])
                                
        categorySplitter.Add(categorySizer, 0, wx.EXPAND)
        
        # The tabs.
        tabs = wx.Notebook(self)
        
        tabs.AddPage(Replace(tabs), "Replace")
        tabs.AddPage(AddAndRemove(tabs), "Add/Remove")
        tabs.AddPage(Casing(tabs), "Casing")
        
        categorySplitter.Add(tabs, 1, wx.EXPAND)
        
        # Rename button.
        categorySplitter.Add(wx.Button(self, label='Rename',size=(300,80)), 0, wx.ALIGN_BOTTOM)
        
        # Work Area (temp)
        self.display = wx.TextCtrl(self)
        splitterSizer.Add(self.display, proportion=2, flag=wx.EXPAND)
        splitterSizer.SetItemMinSize(self.display, (400,400))

    def openFolder(self, e):
        '''Brings up the file browser window to find a folder with files in it.'''
        pass

    def aboutProgram(self, e):
        '''Displays author information.'''
        prompt = wx.MessageDialog(self, 'Created by Jordan Barnes\nrjordanbarnes@gmail.com', 'About', wx.OK)
        prompt.ShowModal()
        prompt.Destroy()

    def exitProgram(self, e):
        ''' Exits the program.'''
        self.Close()

class Replace(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "Replace text", (20,20))

class AddAndRemove(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "Add/Remove text", (40,40))

class Casing(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "Change Casing of text", (60,60))
        
        
def getFiles():
    '''Retrieves all files in current directory and puts them in an array.'''
    arrayOfFiles = []
    for filename in os.listdir("."):
        if filename.lower() != __file__.lower():
            arrayOfFiles.append(filename)
    return arrayOfFiles
	
def main():
    app = wx.App(False)
    frame = MainFrame(None, TITLE, WIDTH, HEIGHT)
    frame.Show()
    app.MainLoop()

main()