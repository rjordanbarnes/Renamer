import wx


class Casing(wx.Panel):
    def __init__(self, parent, fileManager):
        wx.Panel.__init__(self, parent)

        self.fileManager = fileManager

        self.everyWordButton = wx.RadioButton(self, label='Capitalize Every Word', pos=(40, 50), style=wx.RB_GROUP)
        self.lowercaseButton = wx.RadioButton(self, label='all lowercase', pos=(40, 80))
        self.uppercaseButton = wx.RadioButton(self, label='ALL UPPERCASE', pos=(40, 110))

        self.Bind(wx.EVT_RADIOBUTTON, self.onRadioButton, self.everyWordButton)
        self.Bind(wx.EVT_RADIOBUTTON, self.onRadioButton, self.lowercaseButton)
        self.Bind(wx.EVT_RADIOBUTTON, self.onRadioButton, self.uppercaseButton)

    def onRadioButton(self, e):
        self.fileManager.previewRefresh()

    def refresh(self, previews):
        '''Edits the preview directly.'''
        counter = 0
        for currentFile in previews:
            if self.everyWordButton.GetValue():
                # Capitalizes every word in the filename.

                # First lowercases every letter and capitalizes the first letter of the filename.
                currentFile = currentFile.lower()
                currentFile = currentFile.capitalize()

                # Splits the string into a list.
                fileAsList = list(currentFile)

                # Finds the spaces in the filename and uppcases the letter directly after it.
                letterCounter = 1
                for letter in fileAsList:
                    if letter == ' ':
                        fileAsList[letterCounter] = fileAsList[letterCounter].upper()
                    letterCounter += 1

                # Repacks the list into a string and sends it to the preview.
                fileAsString = ''.join(fileAsList)
                previews[counter] = fileAsString

            elif self.lowercaseButton.GetValue():
                # Set the entire filename to lowercase.
                previews[counter] = currentFile.lower()
            elif self.uppercaseButton.GetValue():
                # Set the entire filename to uppercase.
                previews[counter] = currentFile.upper()
            counter += 1

    def cleanUpTab(self):
        self.everyWordButton.SetValue(True)
