#import needed tools - test if it allows multiple imports.
import pandas as pd
import os, glob, time, datetime
#used to find ints
import re

#FileManager Class
class FileManager(object): #Note to self - have to inheret from object in 2.7
	
	#Constructor
	def __init__(self):
		self.dataFolder = os.getcwd() + "\\data\\"
		self.outputFolder = os.getcwd() + "\\output\\"
		self.toClassifyFolder = os.getcwd() + "\\toClassify\\"
		self.outputTextFile = self.outputFolder + self.__genOutputFileName("txt")
		open(self.outputTextFile, "w+")
		#Output file name format: TIMESTAMP_FILE.type

	#Acquires data folder, gets the file names, and returns the file names as a list.
	def getDataFolderContent(self):
		files = os.listdir(self.dataFolder)
		return files
	
	#Imports all .csv files held within the data folder and imports them as python - assumes seperated by , and CSV.
	def getAllDataFiles(self):
		files = glob.glob(self.dataFolder + "/*.csv")
		fileData = []
		for thisFile in files:
			df = pd.read_csv(thisFile, sep = ',', index_col = False)
			fileData.append(df)
		return fileData
		
	#Acquires toClassify folder, gets file names, returns file names as a list.
	def getClassifyFolderContent(self):
		files = os.listdir(self.toClassifyFolder)
		return files
	
	#Imports all .csv files held within the toClassify folder and imports them as pandas - assumes seperated by m and CSV.
	def getAllToClassifyFiles(self):
		files = glob.glob(self.toClassifyFolder + "/*.csv")
		fileData = []
		for thisFile in files:
			df = pd.read_csv(thisFile, sep = ',', index_col = False)
			fileData.append(df)
		return fileData
	
	
	#Used to get output file names - used internally to avoid overwriting previous output files.
	def __getOutputFolderContent(self):
		files = os.listdir(self.outputFolder)
		return files
	
	#Generates a timestamp and returns it as a String formatted as YEAR-MONTH-DAY_HOUR-MIN-SEC
	def __genTimestamp(self):
		ts = time.time()
		timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
		return str(timeStamp)
	
	#Generates a filename when given the filetype. provides file name as a string.
	def __genOutputFileName(self, filetype):
		#now, generate the output file name.
		timestamp = self.__genTimestamp()
		filename = timestamp + "OUTPUT." + filetype
		return filename
	
	#Save the designated dataframe as a new file
	def saveDF(self, df):
		saveName = self.outputFolder + self.__genOutputFileName("csv")
		df.to_csv(saveName, index=True)
	
	def updateOutputTextFile(self, newText):
		with open(self.outputTextFile, 'a') as theFile:
			theFile.write(newText)
			