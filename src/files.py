import os


class FileManager:
    def __init__(self, mainFrame, workArea):
        self.files = []             # Actual files.
        self.previews = []          # Shortened file names (no path)
        self.originalNames = []     # Shortened file names that never change
        self.fullPaths = []         # Full file names including path
        self.mainFrame = mainFrame
        self.workArea = workArea

    def addFile(self, inputFile):
        ''' Adds a new file to the Files and the name to the Original Names and Previews.'''
        # Put actual file in File array.
        self.files.append(inputFile)

        # Put file name in the originalNames and previews.
        fileName = self.getFileName(inputFile)
        self.originalNames.append(fileName)
        self.previews.append(fileName)

        # Put full path of file in fullPaths.
        self.fullPaths.append(inputFile.name)

        # Creates new row for the file.
        self.workArea.displayFile(self.files, fileName)

        self.previewRefresh()

    def removeFile(self, fileIndex):
        ''' Removes a file from the arrays.'''
        self.files.pop(fileIndex)
        self.previews.pop(fileIndex)
        self.originalNames.pop(fileIndex)
        self.fullPaths.pop(fileIndex)

    def renameFiles(self):
        '''Renames the files to the previews.'''
        counter = 0
        for currentFile in self.originalNames:
            os.chdir(self.getPath(self.files[counter]))
            # Changes the current file name to the string found in the preview array.
            os.rename(currentFile, self.previews[counter])

            # Finds the file's new path and opens it to fill up the arrays.
            newFile = self.getPath(self.files[counter]) + self.previews[counter]
            self.files[counter] = open(newFile, 'r')

            # Fills the arrays up with the new file.
            shortName = self.getFileName(self.files[counter])
            self.previews[counter] = shortName
            self.originalNames[counter] = shortName
            self.fullPaths[counter] = self.files[counter].name

            # Updates the Work Space and closes file.
            self.workArea.changeName(counter, shortName)
            self.workArea.changePreview(counter, shortName)
            self.files[counter].close()

            counter += 1

    def previewRefresh(self):
        ''' Refreshes the previews.'''
        # Reverts previews to the original names.
        counter = 0
        for currentFileName in self.previews:
            self.previews[counter] = self.originalNames[counter]
            counter += 1

        # Gets the current tab and applies the filter to the newly reverted previews.
        currentTab = self.mainFrame.getCurrentTab()
        currentTab.refresh(self.previews)

        # Displays the newly changed previews.
        counter = 0
        for currentFileName in self.previews:
            self.workArea.changePreview(counter, currentFileName)
            counter += 1

    def getFileName(self, inputFile):
        ''' Finds the first backslash from the end of the file name and gets rid of everything but the file's name.'''
        shortenedFileName = inputFile.name[(inputFile.name.rindex('\\') + 1):]
        return shortenedFileName

    def getPath(self, inputFile):
        ''' Returns the path of the inputfile.'''
        filePath = inputFile.name[:(inputFile.name.rindex('\\') + 1)]
        return filePath
