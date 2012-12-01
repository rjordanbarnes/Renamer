import wx


class Remove(wx.Panel):
    def __init__(self, parent, fileManager):
        wx.Panel.__init__(self, parent)

        self.fileManager = fileManager

        wx.StaticText(self, -1, "Remove", (40, 30))
        self.removeBox = wx.TextCtrl(self, pos=(40, 50), size=(30, 20))
        self.removeBox.SetMaxLength(3)
        wx.StaticText(self, -1, "characters", (80, 53))

        wx.StaticText(self, -1, "From The", (40, 90))
        self.startButton = wx.RadioButton(self, label='Start', pos=(40, 114), style=wx.RB_GROUP)
        self.endButton = wx.RadioButton(self, label='End', pos=(100, 114))

        wx.StaticText(self, -1, "At Position", (40, 150))
        self.positionSlider = wx.Slider(self, value=0, minValue=0, maxValue=10, pos=(80, 170), size=(170, -1), style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS)

        self.positionBox = wx.TextCtrl(self, pos=(40, 170), size=(30, 20))
        self.positionBox.SetMaxLength(3)
        self.positionBox.ChangeValue(str(self.positionSlider.GetValue()))

        self.Bind(wx.EVT_TEXT, self.onEditBox, self.removeBox)
        self.Bind(wx.EVT_TEXT, self.onEditBox, self.positionBox)
        self.Bind(wx.EVT_SCROLL, self.onMovePositionSlider, self.positionSlider)
        self.Bind(wx.EVT_RADIOBUTTON, self.onRadioButton, self.startButton)
        self.Bind(wx.EVT_RADIOBUTTON, self.onRadioButton, self.endButton)

    def onMovePositionSlider(self, e):
        self.positionBox.ChangeValue(str(self.positionSlider.GetValue()))
        self.fileManager.previewRefresh()

    def onEditBox(self, e):
        self.fileManager.previewRefresh()

    def onRadioButton(self, e):
        self.fileManager.previewRefresh()

    def refresh(self, previews):
        '''Edits the preview directly.'''
        # Determines which way to display the slider.
        if self.endButton.GetValue():
            self.positionSlider.SetWindowStyle(wx.SL_INVERSE | wx.SL_AUTOTICKS)
        else:
            self.positionSlider.SetWindowStyle(wx.SL_HORIZONTAL | wx.SL_AUTOTICKS)

        # First finds the longest name in the files and sets the Max Slider value to that.
        longestName = 0
        for currentFile in previews:
            if len(currentFile) > longestName:
                longestName = len(currentFile)
        self.positionSlider.SetMax(longestName)
        self.checkPositionBoxValidity()
        self.checkRemoveBoxValidity()

        # Then performs the actual preview change.
        positionBoxValue = int(self.positionBox.GetValue())
        removeBoxValue = int(self.removeBox.GetValue()) + positionBoxValue
        radioEnd = self.endButton.GetValue()

        counter = 0
        for selectedFile in previews:
            # Splits the file into a list, deletes a part of the list, and then returns the entire thing to a string to display in the Preview pane.
            fileAsList = list(selectedFile)

            if radioEnd:
                fileAsList.reverse()  # Reverses the list if the End button is pressed.

            del fileAsList[positionBoxValue:removeBoxValue]

            if radioEnd:
                fileAsList.reverse()  # Reverts the reversal.

            fileAsString = ''.join(fileAsList)
            previews[counter] = fileAsString
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

    def checkRemoveBoxValidity(self):
        ''' Makes sure that the Remove Box stays within the Min/Max of the slider.'''
        try:
            # If the Box is greater than the Max Slider, set the box to the Max Slider.
            if int(self.removeBox.GetValue()) > self.positionSlider.GetMax():
                self.removeBox.ChangeValue(str(self.positionSlider.GetMax()))
        except:
            # Sets everything to the minimum if a non-int is entered.
            self.removeBox.ChangeValue(str(self.positionSlider.GetMin()))

    def cleanUpTab(self):
        self.removeBox.Clear()
        self.positionSlider.SetWindowStyle(wx.SL_HORIZONTAL | wx.SL_AUTOTICKS)
        self.positionBox.ChangeValue('0')
        self.positionSlider.SetValue(0)
        self.checkPositionBoxValidity()
        self.checkRemoveBoxValidity()
        self.startButton.SetValue(True)
