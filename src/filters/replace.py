import wx


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
