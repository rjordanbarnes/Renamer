import os

arrayOfFiles = []

def getFiles():
	'''Retrieves all files in current directory and puts them in an array.'''
	for filename in os.listdir("."):
		if filename.lower() != __file__.lower():
			arrayOfFiles.append(filename)

getFiles()

for file in arrayOfFiles:
	print files