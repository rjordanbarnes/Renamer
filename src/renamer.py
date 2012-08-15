import wx
import os
import unicodedata

TITLE = "Renaming Tool"
WIDTH = 900
HEIGHT = 600


class MainFrame(wx.Frame):
    def __init__(self, parent, title, width, height):
        wx.Frame.__init__(self, parent, title=title, size=(width, height), style=wx.DEFAULT_FRAME_STYLE)
        self.Center()
        self.SetMinSize((WIDTH - 250, HEIGHT - 200))
        self.initializeMenuBar()
        self.initializeContents()

    def initializeMenuBar(self):
        ''' Initializes the important Menu Bar.'''
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

        # The Work Area columns.
        self.workArea.InsertColumn(0, 'Name', width=280)
        self.workArea.InsertColumn(1, 'Preview', width=280)

        workAreaSizer.Add(self.workArea, 1, wx.EXPAND)
        workAreaPanel.SetSizer(workAreaSizer)

        splitterSizer.Add(workAreaPanel, 1, flag=wx.EXPAND)

        # Sets up File Drop Area.

        self.groupOfFiles = GroupOfFiles(self, self.workArea)
        fileDropArea = FileDrop(self, self.workArea, self.groupOfFiles)
        self.workArea.SetDropTarget(fileDropArea)

        # Set up tabs and default to General.
        self.tabs = wx.Notebook(self)
        self.tabs.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.onTabChanging)

        self.generalButton.SetValue(True)
        self.displayTabs("general", self.tabs)

        categorySplitter.Add(self.tabs, 1, wx.EXPAND)

        # Rename button.
        self.renameButton = wx.Button(self, label='Rename', size=(300, 80))
        categorySplitter.Add(self.renameButton, 0, wx.ALIGN_BOTTOM)
        self.renameButton.Bind(wx.EVT_BUTTON, self.selectRenameButton)

        # Adds a few variables to the Work Area.
        self.workArea.SetVariables(self.groupOfFiles, self.tabs)

    def selectGeneralButton(self, e):
        ''' Turns all buttons but General off and displays the correct tabs.'''
        isPressed = self.generalButton.GetValue()

        currentPage = self.tabs.GetCurrentPage()
        currentPage.cleanUpTab()

        if isPressed:
            self.musicButton.SetValue(False)
            self.videoButton.SetValue(False)
        else:
            self.generalButton.SetValue(True)

        self.displayTabs("general", self.tabs)

    def selectMusicButton(self, e):
        ''' Turns all buttons but Music off and displays the correct tabs.'''
        isPressed = self.musicButton.GetValue()

        currentPage = self.tabs.GetCurrentPage()
        currentPage.cleanUpTab()

        if isPressed:
            self.generalButton.SetValue(False)
            self.videoButton.SetValue(False)
        else:
            self.musicButton.SetValue(True)

        self.displayTabs("music", self.tabs)

    def selectVideoButton(self, e):
        ''' Turns all buttons but Video off and displays the correct tabs.'''
        isPressed = self.videoButton.GetValue()

        currentPage = self.tabs.GetCurrentPage()
        currentPage.cleanUpTab()

        if isPressed:
            self.generalButton.SetValue(False)
            self.musicButton.SetValue(False)
        else:
            self.videoButton.SetValue(True)

        self.displayTabs("video", self.tabs)

    def displayTabs(self, button, notebook):
        ''' Controls which tabs are displayed when certain buttons are pressed.'''
        notebook.DeleteAllPages()

        files = self.groupOfFiles
        if button is "general":
            notebook.AddPage(Replace(notebook, files), "Replace")
            notebook.AddPage(Add(notebook, files), "Add")
            notebook.AddPage(Remove(notebook, files), "Remove")
            notebook.AddPage(Casing(notebook, files), "Casing")
        elif button is "music":
            notebook.AddPage(Replace(notebook, files), "Music 1")
            notebook.AddPage(Add(notebook, files), "Music 2")
            notebook.AddPage(Casing(notebook, files), "Music 3")
        elif button is "video":
            notebook.AddPage(Replace(notebook, files), "Video 1")
            notebook.AddPage(Add(notebook, files), "Video 2")
            notebook.AddPage(Casing(notebook, files), "Video 3")

    def onTabChanging(self, e):
        '''Cleans up the current tab contents when the tab is changed.'''
        try:
            currentPage = self.tabs.GetCurrentPage()
            currentPage.cleanUpTab()
        except:
            pass

    def selectRenameButton(self, e):
        ''' Renames the files with the file Previews.'''
        self.groupOfFiles.renameFiles()

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


class WorkArea(wx.ListCtrl):
    def __init__(self, parent, ID=wx.ID_ANY):
        ''' The right side of the program where files are added.'''
        wx.ListCtrl.__init__(self, parent, ID)

        self.SetSingleStyle(wx.LC_REPORT)
        self.parent = parent

        self.Bind(wx.EVT_LEFT_DOWN, self.onLeftDown)
        self.Bind(wx.EVT_RIGHT_DOWN, self.onRightDown)

        # Currently selected row
        self.cur = None

    def SetVariables(self, groupOfFiles, tabs):
        ''' Sets up the GroupOfFiles.'''
        self.groupOfFiles = groupOfFiles
        self.tabs = tabs

    def onLeftDown(self, event):
        ''' Selects an entry in the Work Area.'''
        if self.cur != None:
            self.Select(self.cur, 0)  # Deselect currently selected item

        x, y = event.GetPosition()
        row, flags = self.HitTest((x, y))

        self.Select(row)
        self.cur = row

    def onRightDown(self, event):
        ''' Brings up the context menu in the Work Area.'''
        menu = wx.Menu()
        delete = menu.Append(wx.ID_ANY, 'Remove')

        self.Bind(wx.EVT_MENU, self.onDelete, delete)

        # Select row
        self.onLeftDown(event)

        self.PopupMenu(menu, event.GetPosition())

    def onDelete(self, event):
        ''' Removes the row in the Work Area and gets rid of the item from the arrays.'''
        if self.cur >= 0:
            self.DeleteItem(self.cur)
            self.groupOfFiles.arrayOfFiles.pop(self.cur)
            self.groupOfFiles.arrayOfPreviews.pop(self.cur)
            self.groupOfFiles.arrayOfOriginals.pop(self.cur)
            self.groupOfFiles.arrayOfShorter.pop(self.cur)

        currentTab = self.tabs.GetCurrentPage()
        currentTab.refresh()


class FileDrop(wx.FileDropTarget):
    ''' The File Drop Area object.'''
    def __init__(self, parent, workArea, groupOfFiles):
        wx.FileDropTarget.__init__(self)
        self.parent = parent
        self.workArea = workArea
        self.groupOfFiles = groupOfFiles

    def OnDropFiles(self, x, y, filenames):
        ''' Whenever a file is dropped on the area.'''
        for name in filenames:
            # No duplicates.
            if self.groupOfFiles.arrayOfOriginals.count(name) == 0:
                try:
                    # Open file, add it to the file array, then close it.
                    openedFile = open(name, 'r')
                    self.groupOfFiles.addFile(openedFile)
                    openedFile.close()
                except IOError, error:
                    dlg = wx.MessageDialog(None, 'Error opening file\n' + str(error))
                    dlg.ShowModal()
                except UnicodeDecodeError, error:
                    dlg = wx.MessageDialog(None, 'Cannot open non ascii files\n' + str(error))
                    dlg.ShowModal()

        # Refresh Work Area when new file is added.
        currentTab = self.parent.tabs.GetCurrentPage()
        currentTab.refresh()


class GroupOfFiles:
    def __init__(self, parent, workArea):
        self.arrayOfFiles = []
        self.arrayOfPreviews = []
        self.arrayOfOriginals = []
        self.arrayOfShorter = []
        self.workArea = workArea
        self.parent = parent

    def addFile(self, selectedFile):
        ''' Adds a file to the array of files and shows it on screen in its shortened form.'''
        # arrayOfFiles gets the actual file.
        self.arrayOfFiles.append(selectedFile)

        # arrayOfPreviews gets the shortened string form of the file.
        shortenedFileName = self.shortenFileName(selectedFile)
        self.arrayOfPreviews.append(shortenedFileName)

        # arrayOfOriginals gets the full unaltered name of the file.
        self.arrayOfOriginals.append(selectedFile.name)

        # arrayOfShorter gets the shortened string and never changes.
        self.arrayOfShorter.append(shortenedFileName)

        # Display the short file name in a new row.
        self.workArea.InsertStringItem((len(self.arrayOfFiles) - 1), shortenedFileName)
        self.workArea.SetStringItem((len(self.arrayOfPreviews) - 1), 1, shortenedFileName)

    def shortenFileName(self, selectedFile):
        ''' Finds the first backslash from the end of the file name and gets rid of everything but the file's name.'''
        shortenedFileName = selectedFile.name[(selectedFile.name.rindex('\\') + 1):]
        newShortFileName = unicodedata.normalize('NFKD', shortenedFileName).encode('ascii', 'ignore')
        return newShortFileName

    def displayPath(self, selectedFile):
        ''' Returns the path of the selected file.'''
        filePath = selectedFile.name[:(selectedFile.name.rindex('\\') + 1)]
        newFilePath = unicodedata.normalize('NFKD', filePath).encode('ascii', 'ignore')
        return newFilePath

    def renameFiles(self):
        ''' Renames each file to the name found in the Preview column.'''
        counter = 0
        for selectedFile in self.arrayOfFiles:
            os.chdir(self.displayPath(selectedFile))
            # Changes the current file name to the string found in the Preview column.
            os.rename(self.shortenFileName(selectedFile), self.workArea.GetItem(counter, 1).GetText())

            # Update all of the arrays to new name.
            # arrayOfFiles (the actual file)
            self.arrayOfFiles[counter] = open((self.displayPath(selectedFile) + self.workArea.GetItem(counter, 1).GetText()), 'r')
            shortenedCurrentName = self.shortenFileName(self.arrayOfFiles[counter])
            # arrayOfPreviews (shortened version)
            self.arrayOfPreviews[counter] = shortenedCurrentName
            # arrayOfOriginals (full path)
            self.arrayOfOriginals[counter] = (selectedFile.name)
            # arrayOfShorter (shortened version that never changes)
            self.arrayOfShorter[counter] = shortenedCurrentName

            # Updates the Work Space and close file.
            self.workArea.SetStringItem(counter, 0, shortenedCurrentName)
            self.workArea.SetStringItem(counter, 1, shortenedCurrentName)
            self.arrayOfFiles[counter].close()
            counter += 1

        currentTab = self.parent.tabs.GetCurrentPage()
        currentTab.refresh()


'''
Renaming Rules.
'''


class Replace(wx.Panel):
    def __init__(self, parent, files):
        ''' Replaces all instances of a string with another string.'''
        wx.Panel.__init__(self, parent)

        self.files = files

        wx.StaticText(self, -1, "Find", (40, 30))
        self.findBox = wx.TextCtrl(self, pos=(40, 50), size=(200, 20))
        wx.StaticText(self, -1, "Replace With", (40, 90))
        self.replaceBox = wx.TextCtrl(self, pos=(40, 110), size=(200, 20))

        self.Bind(wx.EVT_TEXT, self.updatePreview, self.findBox)
        self.Bind(wx.EVT_TEXT, self.updatePreview, self.replaceBox)

        self.currentFindContents = ''
        self.currentReplaceContents = ''

    def refresh(self):
        '''Refreshes the preview column with replaced letters.'''
        if (self.findBox.GetLineLength(0) > 0) and (self.replaceBox.GetLineLength(0) > 0):
            # If the boxes have something in it, edit the preview.
            counter = 0
            for selectedFile in self.files.arrayOfPreviews:
                newFile = selectedFile.replace(self.findBox.GetLineText(0), self.replaceBox.GetLineText(0))
                self.files.workArea.SetStringItem(counter, 1, newFile)
                counter += 1
        else:
            # If one of the boxes has nothing in it, return to the default.
            counter = 0
            for selectedFile in self.files.arrayOfPreviews:
                newFile = self.files.arrayOfShorter[counter]
                self.files.workArea.SetStringItem(counter, 1, newFile)
                counter += 1

    def cleanUpTab(self):
        self.findBox.Clear()
        self.replaceBox.Clear()

    def updatePreview(self, e):
        '''What happens when the Find box or Replace box is edited.'''
        self.refresh()


class Add(wx.Panel):
    def __init__(self, parent, files):
        wx.Panel.__init__(self, parent)
        self.files = files

        wx.StaticText(self, -1, "Insert", (40, 30))
        self.insertBox = wx.TextCtrl(self, pos=(40, 50), size=(200, 20))

        wx.StaticText(self, -1, "At The", (40, 90))
        self.startButton = wx.RadioButton(self, label='Start', pos=(40, 114), style=wx.RB_GROUP)
        self.endButton = wx.RadioButton(self, label='End', pos=(100, 114))

        wx.StaticText(self, -1, "At Position", (40, 150))
        self.positionSlider = wx.Slider(self, value=0, minValue=0, maxValue=10, pos=(80, 170), size=(170, -1), style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS)

        self.positionBox = wx.TextCtrl(self, pos=(40, 170), size=(30, 20))
        self.positionBox.SetMaxLength(3)
        self.positionBox.ChangeValue(str(self.positionSlider.GetValue()))

        self.Bind(wx.EVT_TEXT, self.onEditBox, self.insertBox)
        self.Bind(wx.EVT_TEXT, self.onEditBox, self.positionBox)
        self.Bind(wx.EVT_SCROLL, self.onMovePositionSlider, self.positionSlider)
        self.Bind(wx.EVT_RADIOBUTTON, self.onRadioButton, self.startButton)
        self.Bind(wx.EVT_RADIOBUTTON, self.onRadioButton, self.endButton)

    def onMovePositionSlider(self, e):
        self.positionBox.ChangeValue(str(self.positionSlider.GetValue()))
        self.refresh()

    def onEditBox(self, e):
        self.refresh()

    def onRadioButton(self, e):
        self.refresh()

    def refresh(self):
        # First finds the longest name in the files and sets the Max Slider value to that.
        longestName = 0
        for currentFile in self.files.arrayOfPreviews:
            if len(currentFile) > longestName:
                longestName = len(currentFile)
        self.positionSlider.SetMax(longestName)
        self.checkPositionBoxValidity()

        # Then performs the actual preview change.
        insertBoxValue = unicodedata.normalize('NFKD', self.insertBox.GetValue()).encode('ascii', 'ignore')
        positionBoxValue = int(self.positionBox.GetValue())
        radioEnd = self.endButton.GetValue()

        counter = 0
        for selectedFile in self.files.arrayOfPreviews:
            # Splits the file into a list, adds in the new string, and then returns the entire thing to a string to display in the Preview pane.
            fileAsList = list(selectedFile)

            if radioEnd:
                fileAsList.reverse()  # Reverses the list if the End button is pressed.

            fileAsList.insert(positionBoxValue, insertBoxValue)

            if radioEnd:
                fileAsList.reverse()  # Reverts the reversal.

            fileAsString = ''.join(fileAsList)
            self.files.workArea.SetStringItem(counter, 1, fileAsString)
            counter += 1

    def checkPositionBoxValidity(self):
        ''' Makes sure that the Position Box stays within the Min/Max of the slider.'''
        try:
            # If the Box is greater than the Max Slider, set the box to the Max Slider.
            if int(self.positionBox.GetValue()) > self.positionSlider.GetMax():
                self.positionBox.ChangeValue(str(self.positionSlider.GetMax()))
            # The slider then updates to the Box.
            self.positionSlider.SetValue(int(self.positionBox.GetValue()))
        except:
            # Sets everything to the minimum if a non-int is entered.
            self.positionBox.ChangeValue(str(self.positionSlider.GetMin()))
            self.positionSlider.SetValue(self.positionSlider.GetMin())

    def cleanUpTab(self):
        self.insertBox.Clear()
        self.positionBox.ChangeValue('0')
        self.positionSlider.SetValue(0)
        self.checkPositionBoxValidity()


class Remove(wx.Panel):
    def __init__(self, parent, files):
        wx.Panel.__init__(self, parent)
        wx.StaticText(self, -1, "Remove", (40, 40))


class Casing(wx.Panel):
    def __init__(self, parent, files):
        wx.Panel.__init__(self, parent)
        wx.StaticText(self, -1, "Change Casing of text", (60, 60))


def main():
    app = wx.App(False)
    frame = MainFrame(None, TITLE, WIDTH, HEIGHT)
    frame.Show()
    app.MainLoop()

main()
