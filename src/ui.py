import wx
import files
from filters import *
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin


class MainFrame(wx.Frame):
    def __init__(self, parent, title, width, height):
        wx.Frame.__init__(self, parent, title=title, size=(width, height), style=wx.DEFAULT_FRAME_STYLE)
        self.Center()
        self.SetMinSize((width - 250, height - 200))
        self.initializeMenuBar()
        self.initializeContents()

    def initializeMenuBar(self):
        ''' Initializes the important Menu Bar.'''
        # File Menu entries.
        fileMenu = wx.Menu()
        menuOpen = fileMenu.Append(wx.ID_OPEN, '&Open', '')
        fileMenu.AppendSeparator()
        menuExit = fileMenu.Append(wx.ID_EXIT, 'E&xit', '')

        # Help Menu entries.
        helpMenu = wx.Menu()
        menuAbout = helpMenu.Append(wx.ID_ABOUT, '&About', '')

        # Creates the Menu Bar and adds the top-level menu entries.
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, '&File')
        menuBar.Append(helpMenu, '&Help')
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

        self.generalButton = wx.ToggleButton(self, label='General', size=(100, 40))
        self.musicButton = wx.ToggleButton(self, label='Music', size=(100, 40))
        self.videoButton = wx.ToggleButton(self, label='Videos', size=(100, 40))

        categorySizer.AddMany([(self.generalButton, 0, wx.SHAPED),
                               (self.musicButton, 0, wx.SHAPED),
                               (self.videoButton, 0, wx.SHAPED)])

        self.generalButton.Bind(wx.EVT_TOGGLEBUTTON, self.selectGeneralButton)
        self.musicButton.Bind(wx.EVT_TOGGLEBUTTON, self.selectMusicButton)
        self.videoButton.Bind(wx.EVT_TOGGLEBUTTON, self.selectVideoButton)

        categorySplitter.Add(categorySizer, 0, wx.EXPAND)

        # Sets up a new Work Area panel that's linked to the Work Area Sizer.
        workAreaSizer = wx.BoxSizer(wx.HORIZONTAL)
        workAreaPanel = wx.Panel(self, -1)
        self.workArea = WorkArea(workAreaPanel, -1)

        splitterSizer.Add(workAreaPanel, 1, flag=wx.EXPAND)

        # The Work Area columns.
        self.workArea.InsertColumn(0, 'Name', width=280)
        self.workArea.InsertColumn(1, 'Preview', width=280)

        workAreaSizer.Add(self.workArea, 1, wx.EXPAND)
        workAreaPanel.SetSizer(workAreaSizer)

        # Sets up File Drop Area.

        self.fileManager = files.FileManager(self, self.workArea)
        fileDropArea = FileDrop(self, self.workArea, self.fileManager)
        self.workArea.SetDropTarget(fileDropArea)

        # Set up tabs and default to General.
        self.tabs = wx.Notebook(self)
        self.tabs.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.onTabChanging)
        self.tabs.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.onTabChanged)

        self.generalButton.SetValue(True)
        self.displayTabs("general", self.tabs)

        categorySplitter.Add(self.tabs, 1, wx.EXPAND)

        # Rename button.
        self.renameButton = wx.Button(self, label='Rename', size=(300, 80))
        categorySplitter.Add(self.renameButton, 0, wx.ALIGN_BOTTOM)
        self.renameButton.Bind(wx.EVT_BUTTON, self.selectRenameButton)

        # Rename button's font.
        self.renameButtonFont = wx.Font(pointSize=24, family=wx.FONTFAMILY_SWISS, style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_BOLD)
        self.renameButton.SetFont(self.renameButtonFont)

        # Adds a few variables to the Work Area.
        self.workArea.SetVariables(self.fileManager, self.tabs)

    def selectGeneralButton(self, e):
        ''' Turns all buttons but General off and displays the correct tabs.'''
        self.selectCategoryButton(self.generalButton, 'general')

    def selectMusicButton(self, e):
        ''' Turns all buttons but Music off and displays the correct tabs.'''
        self.selectCategoryButton(self.musicButton, 'music')

    def selectVideoButton(self, e):
        ''' Turns all buttons but Video off and displays the correct tabs.'''
        self.selectCategoryButton(self.videoButton, 'video')

    def selectCategoryButton(self, category, button):
        ''' Cleans up the current tab, resets all category buttons to unpressed, then sets the correct one to pressed and displays the correct tab content.'''
        currentTab = self.getCurrentTab()
        currentTab.cleanUpTab()

        # Unpresses everything.
        self.generalButton.SetValue(False)
        self.videoButton.SetValue(False)
        self.musicButton.SetValue(False)

        # Press correct button and shows the correct tab information.
        category.SetValue(True)
        self.displayTabs(button, self.tabs)

    def displayTabs(self, button, notebook):
        ''' Controls which tabs are displayed when certain buttons are pressed.'''
        notebook.DeleteAllPages()

        fileManager = self.fileManager
        if button is "general":
            notebook.AddPage(replace.Replace(notebook, fileManager), "Replace")
            notebook.AddPage(add.Add(notebook, fileManager), "Add")
            notebook.AddPage(remove.Remove(notebook, fileManager), "Remove")
            notebook.AddPage(casing.Casing(notebook, fileManager), "Casing")
        elif button is "music":
            notebook.AddPage(replace.Replace(notebook, fileManager), "Music 1")
            notebook.AddPage(add.Add(notebook, fileManager), "Music 2")
            notebook.AddPage(casing.Casing(notebook, fileManager), "Music 3")
        elif button is "video":
            notebook.AddPage(replace.Replace(notebook, fileManager), "Video 1")
            notebook.AddPage(add.Add(notebook, fileManager), "Video 2")
            notebook.AddPage(casing.Casing(notebook, fileManager), "Video 3")

    def getCurrentTab(self):
        ''' Returns the current tab.'''
        return self.tabs.GetCurrentPage()

    def setCurrentTab(self, tabNumber):
        ''' Sets the current tab to the inputted tab number.'''
        self.tabs.ChangeSelection(tabNumber)

    def onTabChanging(self, e):
        '''Cleans up the current tab contents when the tab is changed.'''
        try:
            oldPage = self.tabs.GetCurrentPage()
            oldPage.cleanUpTab()
        except:
            pass
        e.Skip()

    def onTabChanged(self, e):
        ''' Does a preview refresh after changing tabs.'''
        currentPageNumber = e.GetSelection()
        self.setCurrentTab(currentPageNumber)
        self.fileManager.previewRefresh()
        e.Skip()

    def selectRenameButton(self, e):
        ''' Renames the files with the file Previews.'''
        self.fileManager.renameFiles()

    def openFolder(self, e):
        ''' Brings up the file browser window to find a folder with files in it.'''
        pass

    def aboutProgram(self, e):
        ''' Displays author information.'''
        prompt = wx.MessageDialog(self, 'Created by Jordan Barnes\nrjordanbarnes@gmail.com', 'About', wx.OK)
        prompt.ShowModal()
        prompt.Destroy()

    def exitProgram(self, e):
        ''' Exits the program.'''
        self.Close()


class WorkArea(wx.ListCtrl, ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID=wx.ID_ANY):
        ''' The right side of the program where files are added.'''
        wx.ListCtrl.__init__(self, parent, ID)
        ListCtrlAutoWidthMixin.__init__(self)

        self.SetSingleStyle(wx.LC_REPORT)
        self.parent = parent

        self.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
        self.Bind(wx.EVT_LEFT_DOWN, self.onLeftDown)
        self.Bind(wx.EVT_RIGHT_DOWN, self.onRightDown)

        # Currently selected rows
        self.selectedItems = []

    def SetVariables(self, fileManager, tabs):
        ''' Sets up the FileManager.'''
        self.fileManager = fileManager
        self.tabs = tabs

    def displayFile(self, arrayOfFiles, filename):
        ''' Displays the filename in a new row.'''
        self.InsertStringItem((len(arrayOfFiles) - 1), filename)
        self.SetStringItem((len(arrayOfFiles) - 1), 1, filename)

    def changeName(self, row, newName):
        ''' Sets the name in the specified row to the newName.'''
        self.SetStringItem(row, 0, newName)

    def changePreview(self, row, newPreview):
        ''' Sets the preview in the specified row to the newPreview.'''
        self.SetStringItem(row, 1, newPreview)

    def onKeyDown(self, event):
        ''' Adds keyboard shortcuts to the Work Area.'''
        key = event.GetKeyCode()

        if key == wx.WXK_DELETE:
            self.onDelete(event)
        if key == 65 and event.ControlDown():
            for item in range(self.GetItemCount()):
                self.Select(item)
                if self.selectedItems.count(item) < 1:
                    self.selectedItems.append(item)

    def onLeftDown(self, event):
        ''' Selects an entry in the Work Area.'''
        self.SetFocus()  # Gives the work area focus

        for item in self.selectedItems:
            self.Select(item, 0)  # Deselects all selected items

        # Figure out what row was clicked.
        x, y = event.GetPosition()
        row, flags = self.HitTest((x, y))

        # If a valid row is clicked and Control is held down,
        # add row onto the array. Otherwise clear the array
        # and then add the row.
        if row >= 0:
            if event.ControlDown():
                if self.selectedItems.count(row) < 1:
                    self.selectedItems.append(row)
            else:
                self.selectedItems = []
                self.selectedItems.append(row)
        else:
            self.selectedItems = []

        for item in self.selectedItems:
            self.Select(item)   # Select all new items in the array

    def onRightDown(self, event):
        ''' Brings up the context menu in the Work Area.'''
        menu = wx.Menu()
        delete = menu.Append(wx.ID_ANY, 'Remove')

        self.Bind(wx.EVT_MENU, self.onDelete, delete)

        if len(self.selectedItems) < 1:
            self.onLeftDown(event)  # Select row if no rows are already selected

        self.PopupMenu(menu, event.GetPosition())

    def onDelete(self, event):
        ''' Removes the row in the Work Area and gets rid of the item from the arrays.'''
        for item in reversed(sorted(self.selectedItems)):  # Sorts and then reverses the array to correspond with indexes
            self.fileManager.removeFile(item)   # Removes file from arrays in FileManager
            self.DeleteItem(item)               # Removes file from work area
            self.Select(item, 0)                # Deselects all files

        self.selectedItems = []

        self.fileManager.previewRefresh()


class FileDrop(wx.FileDropTarget):
    ''' The File Drop Area object.'''
    def __init__(self, parent, workArea, fileManager):
        wx.FileDropTarget.__init__(self)
        self.parent = parent
        self.workArea = workArea
        self.fileManager = fileManager

    def OnDropFiles(self, x, y, filenames):
        ''' Whenever a file is dropped on the area.'''
        for name in filenames:
            # No duplicates.
            if self.fileManager.fullPaths.count(name) == 0:
                try:
                    # Open file, add it to the file array, then close it.
                    openedFile = open(name, 'r')
                    self.fileManager.addFile(openedFile)
                    openedFile.close()
                except IOError, error:
                    dlg = wx.MessageDialog(None, 'Error opening file\n' + str(error))
                    dlg.ShowModal()
                except UnicodeDecodeError, error:
                    dlg = wx.MessageDialog(None, 'Cannot open non ascii files\n' + str(error))
                    dlg.ShowModal()
