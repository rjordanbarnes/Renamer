import wx
import os
import sys
import unicodedata

TITLE = "Renaming Tool"
WIDTH = 900
HEIGHT = 600

class MainFrame(wx.Frame):
    def __init__(self, parent, title, width, height):
        wx.Frame.__init__(self, parent, title=title, size=(width, height), style=wx.DEFAULT_FRAME_STYLE)
        self.Center()
        self.SetMinSize((WIDTH-250, HEIGHT-200))
        self.initializeMenuBar()
        self.initializeContents()
        
    def initializeMenuBar(self):
        '''Initializes the important Menu Bar.'''
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
        ''' Initializes the contents of the window.'''
        # Splits controls from work area.
        splitterSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(splitterSizer)
        
        # Splits Main buttons from Tabs.
        categorySplitter = wx.BoxSizer(wx.VERTICAL)
        splitterSizer.Add(categorySplitter, flag=wx.EXPAND)
        
        # General, Music, and Videos buttons.
        categorySizer = wx.GridSizer(rows=1, cols=3, vgap=0, hgap=1)
        
        self.generalButton = wx.ToggleButton(self, label='General', size=(100,40))
        self.musicButton = wx.ToggleButton(self, label='Music', size=(100,40))
        self.videoButton = wx.ToggleButton(self, label='Videos', size=(100,40))
        
        categorySizer.AddMany( [(self.generalButton, 0, wx.SHAPED),
                                (self.musicButton, 0, wx.SHAPED),
                                (self.videoButton, 0, wx.SHAPED) ])
        
        self.generalButton.Bind(wx.EVT_TOGGLEBUTTON, self.selectGeneralButton)
        self.musicButton.Bind(wx.EVT_TOGGLEBUTTON, self.selectMusicButton)
        self.videoButton.Bind(wx.EVT_TOGGLEBUTTON, self.selectVideoButton)
        
        categorySplitter.Add(categorySizer, 0, wx.EXPAND)
        
        # Sets up a new Work Area panel that's linked to the Work Area Sizer.
        workAreaSizer = wx.BoxSizer(wx.HORIZONTAL)
        workAreaPanel = wx.Panel(self, -1)
        self.workArea = wx.ListCtrl(workAreaPanel, -1, style=wx.LC_REPORT)
        
        # The Work Area columns.
        self.workArea.InsertColumn(0, 'Name', width=280)
        self.workArea.InsertColumn(1, 'Preview',width=280)
        
        workAreaSizer.Add(self.workArea, 1, wx.EXPAND)
        workAreaPanel.SetSizer(workAreaSizer)
        
        splitterSizer.Add(workAreaPanel, 1, flag=wx.EXPAND)
        
        # Sets up File Drop Area.
        
        self.groupOfFiles = GroupOfFiles(self.workArea)
        fileDropArea = FileDrop(self.workArea, self.groupOfFiles)
        self.workArea.SetDropTarget(fileDropArea)
        
        # Set up tabs and default to General.
        self.tabs = wx.Notebook(self)
        
        self.generalButton.SetValue(True)
        self.displayTabs("general", self.tabs)
        
        categorySplitter.Add(self.tabs, 1, wx.EXPAND)
        
        # Rename button.
        categorySplitter.Add(wx.Button(self, label='Rename',size=(300,80)), 0, wx.ALIGN_BOTTOM)
        
    def selectGeneralButton(self, e):
        '''Turns all buttons but General off and displays the correct tabs.'''
        isPressed = self.generalButton.GetValue()
        
        if isPressed:
            self.musicButton.SetValue(False)
            self.videoButton.SetValue(False)
        else:
            self.generalButton.SetValue(True)
            
        self.displayTabs("general", self.tabs)
            
    def selectMusicButton(self, e):
        '''Turns all buttons but Music off and displays the correct tabs.'''
        isPressed = self.musicButton.GetValue()
        
        if isPressed:
            self.generalButton.SetValue(False)
            self.videoButton.SetValue(False)
        else:
            self.musicButton.SetValue(True)
            
        self.displayTabs("music", self.tabs)
        
    def selectVideoButton(self, e):
        '''Turns all buttons but Video off and displays the correct tabs.'''
        isPressed = self.videoButton.GetValue()
        
        if isPressed:
            self.generalButton.SetValue(False)
            self.musicButton.SetValue(False)
        else:
            self.videoButton.SetValue(True)
            
        self.displayTabs("video", self.tabs)
    
    def displayTabs(self, button, notebook):
        '''Controls which tabs are displayed when certain buttons are pressed.'''
        notebook.DeleteAllPages()
        
        files = self.groupOfFiles
        if button is "general":
            notebook.AddPage(Replace(notebook, files), "Replace")
            notebook.AddPage(AddAndRemove(notebook, files), "Add/Remove")
            notebook.AddPage(Casing(notebook, files), "Casing")
        elif button is "music":
            notebook.AddPage(Replace(notebook, files), "Music 1")
            notebook.AddPage(AddAndRemove(notebook, files), "Music 2")
            notebook.AddPage(Casing(notebook, files), "Music 3")
        elif button is "video":
            notebook.AddPage(Replace(notebook, files), "Video 1")
            notebook.AddPage(AddAndRemove(notebook, files), "Video 2")
            notebook.AddPage(Casing(notebook, files), "Video 3")
            
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

class FileDrop(wx.FileDropTarget):
    '''The File Drop Area object.'''
    def __init__(self, workArea, groupOfFiles):
        wx.FileDropTarget.__init__(self)
        self.workArea = workArea
        self.groupOfFiles = groupOfFiles

    def OnDropFiles(self, x, y, filenames):
        '''Whenever a file is dropped on the area.'''
        for name in filenames:
            try:
                # Open file and add it to the file array.
                file = open(name, 'r')
                self.groupOfFiles.addFile(file)
            except IOError, error:
                dlg = wx.MessageDialog(None, 'Error opening file\n' + str(error))
                dlg.ShowModal()
            except UnicodeDecodeError, error:
                dlg = wx.MessageDialog(None, 'Cannot open non ascii files\n' + str(error))
                dlg.ShowModal()

class GroupOfFiles:
    def __init__(self, workArea):
        self.arrayOfFiles = []
        self.arrayOfPreviews = []
        self.arrayOfOriginals = []
        self.workArea = workArea
        
    def addFile(self, file):
        '''Adds a file to the array of files and shows it on screen in its shortened form.'''
        # arrayOfFiles gets the actual file.
        self.arrayOfFiles.append(file)
        
        # arrayOfPreviews gets the shortened string form of the file.
        shortenedFileName = self.shortenFileName(file)
        self.arrayOfPreviews.append(shortenedFileName)
        
        # arrayOfOriginals gets the shortened string form too, but is never altered.
        self.arrayOfOriginals.append(shortenedFileName)
        
        # Display the short file name in a new row.
        self.workArea.InsertStringItem((len(self.arrayOfFiles) - 1), shortenedFileName)
        self.workArea.SetStringItem((len(self.arrayOfPreviews) - 1), 1, shortenedFileName)
        
    def shortenFileName(self, file):
        '''Finds the first backslash from the end of the file name and gets rid of everything but the file's name.'''
        shortenedFileName = file.name[(file.name.rindex('\\') + 1):]
        newShortFileName = unicodedata.normalize('NFKD', shortenedFileName).encode('ascii','ignore')
        return newShortFileName
      



      
'''Renaming Rules.'''
        
class Replace(wx.Panel):
    def __init__(self, parent, files):
        wx.Panel.__init__(self, parent)
        
        self.files = files
        
        wx.StaticText(self, -1, "Find", (40,30))
        self.findBox = wx.TextCtrl(self, pos=(40,50), size=(200,20))
        wx.StaticText(self, -1, "Replace With", (40,80))
        self.replaceBox = wx.TextCtrl(self, pos=(40,100), size=(200,20))
        
        self.Bind(wx.EVT_TEXT, self.updatePreview, self.findBox)
        self.Bind(wx.EVT_TEXT, self.updatePreview, self.replaceBox)
        
        self.currentFindContents = ''
        self.currentReplaceContents = ''
    
    def refresh(self):
        '''Refreshes the preview column with replaced letters.'''
        if (self.findBox.GetLineLength(0) > 0) and (self.replaceBox.GetLineLength(0) > 0):
            # If the boxes have something in it, edit the preview.
            counter = 0
            for file in self.files.arrayOfPreviews:
                newFile = file.replace(self.findBox.GetLineText(0), self.replaceBox.GetLineText(0))
                self.files.workArea.SetStringItem(counter, 1, newFile)
                counter += 1
        else:
            # If one of the boxes has nothing in it, return to the default.
            counter = 0
            for file in self.files.arrayOfPreviews:
                newFile = self.files.arrayOfOriginals[counter]
                self.files.workArea.SetStringItem(counter, 1, newFile)
                counter += 1
            
    def updatePreview(self, e):
        '''What happens when the Find box or Replace box is edited.'''
        self.refresh()
        
class AddAndRemove(wx.Panel):
    def __init__(self, parent, files):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "Add/Remove text", (40,40))

class Casing(wx.Panel):
    def __init__(self, parent, files):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "Change Casing of text", (60,60))
	
def main():
    app = wx.App(False)
    frame = MainFrame(None, TITLE, WIDTH, HEIGHT)
    frame.Show()
    app.MainLoop()

main()