import sys, ConfigParser
from bin import FileManager
from bin import Preprocessing
from bin import RecommenderSystem
from bin import Statistics
import pandas as pd


lineBreak = "-------------------------------------------------------------\n"



#Parent class for menus.
class menu(object): #Note to self - have to inheret from object in 2.7

	#DEFINE RUN IN THE SUBCLASSES, SINCE THEY ALL USE OTHER STUFF
	def promptUser(self, options):
		while True:
			try:
				for i, option in enumerate(options):
					print i, "|", option, "\n"
				self.choice = int( raw_input("Please choose an option by selecting it\'s number: "))
			except ValueError:
				print("Incorrect input. Please try again.")
				continue
			if self.choice < 0:
				print("Incorrect input. Please try again.")
				continue
			elif self.choice > len(options):
				print("Incorrect input. Please try again.")
				continue
			else:
				break
		return self.choice

#The Recommender System Menu
class RsMenu(menu):

	#Constructor
	def __init__(self):
		self.options = ['Request a recommendation for a player', 'Data Statistics', 'Return to Main Menu']
		#self.accLoss = 0.0
		self.Config = ConfigParser.ConfigParser()
		self.Config.read("preprocessing.ini")
		#print self.Config.sections()
		self.accLoss = float(self.ConfigSectionMap("SectionOne")['acceptableloss'])
		self.cleanedData = list()
		#Read the RS ini file
		self.Config.read("RecommenderSystem.ini")
		self.k = int(self.ConfigSectionMap("SectionOne")['k'])
		
		

	#Handles running for the RSMenu
	def run(self):
		pd.set_option('display.max_columns', 500)
		#First, load all data from the data folder.
		fileManager = FileManager.FileManager()
		print "Importing all files from the \"data\" Folder."
		print "Data Folder Contents:\n", fileManager.getDataFolderContent(), "\n\n"
		self.dataTables = fileManager.getAllDataFiles()
		
		print "Importing all files from the \"toClassify\" Folder."
		print "toClassify Folder Contents:\n", fileManager.getClassifyFolderContent(), "\n\n"
		self.toClassify = fileManager.getAllToClassifyFiles()
		#print type(self.toClassify[0])
		self.toClassify[0] = self.toClassify[0].drop("GameID", 1)
		self.toClassify[0] = self.toClassify[0].drop("Age", 1)
		#print self.toClassify[0]
		preprocessing = Preprocessing.Preprocessing(self.accLoss)
		#If there is more than one data file after preprocessing, then it will concat them
		#Together.
		self.dataTables = pd.concat(self.dataTables)
		
		#Clean the data...
		dt = preprocessing.CleanData(self.dataTables)
		dtNorm = preprocessing.Normalization(self.dataTables)
		self.cleanedData.append(dtNorm)
			
		#Save the self.cleanedData[0][0] - the normalized dataframe.
		fileManager.saveDF(self.cleanedData[0][0])
		
		print "Recommender System Menu--------------------------------------\n\n"
		running = True
		while(running):
			choice = self.promptUser(self.options)
			if(choice == 0):
				print '\n\"Data received, TACCOM.\" -Goliath \n'
				rs = RecommenderSystem.RecommenderSystem(self.cleanedData[0][1], self.cleanedData[0][0])
				#for each user in toClassify, send it to the RS system to be compared. Print results.
				userResults = list()
				for file in self.toClassify:
					for i, user in file.iterrows():
						tempClass = rs.classifyUser(user, self.k)
						userResults.append(tempClass)
						#Classify the user and return the results.

						#Print the user number
						tempPrint = "Results for user {}\n".format(i)
						tempPrint = str(tempPrint)
						print tempPrint
						fileManager.updateOutputTextFile(tempPrint)
						
						#Print the group it was grouped with and save it
						tempPrint = "Group {}\n".format(userResults[i][0])
						tempPrint = str(tempPrint)
						print tempPrint
						fileManager.updateOutputTextFile(tempPrint)
						
						#Print the avg distance and save it
						tempPrint = "Avg Distance the group: {}\n".format(userResults[i][1])
						tempPrint = str(tempPrint)
						print tempPrint
						fileManager.updateOutputTextFile(tempPrint)
						
						#Save the nearest neighbors
						fileManager.updateOutputTextFile("\nNearest Neighbors:\n{}\n".format(userResults[i][2]))
				
				print lineBreak
				
			elif(choice == 1): #Print Statistics
				print '\n\"Status report.\" -Nova \n'
				dataStats = Statistics.Statistics(self.dataTables)
				tempStats = dataStats.getStatistics()
				
				for league, tempData in tempStats:
					leagueTemp = "\nLeague {}\n".format(league)
					tempPrint = str(tempData)
					fileManager.updateOutputTextFile(leagueTemp)
					fileManager.updateOutputTextFile(tempPrint)
					
					
			elif(choice == 2):
				print 'Returning to the Main Menu.'
				return;
	
	#Used to acquire Configuration file INI data - based on stuff learned through the tutorial.
	def ConfigSectionMap(self, section):
		myDict = {}
		options = self.Config.options(section)
		for option in options:
			try:
				myDict[option] = self.Config.get(section, option)
				if myDict[option] == -1:
					DebugPrint("skip: %s" % option)
			except:
				print("exception on %s!" % option)
				myDict[option] = None
		return myDict

		
#main menu
class MainMenu(menu):
	def __init__(self):
		self.version = 1.0
		self.disclaimer = "\n\nStacraft 2 Player Recommender System\nDeveloped by Thomas S. Field, Version %.2f" % self.version
		print self.disclaimer
		self.options = ['Generate a new Recommender System', 'Quit']

	#Handles running of the menu.
	def run(self):
		while(True):
			print "\n\nMain Menu----------------------------------------------------"
			choice = self.promptUser(self.options)
			if(choice == 0): 
				print '\n\"Directive Confirmed.\" -Mothership \n'
				print lineBreak
				rsMenu = RsMenu()
				rsMenu.run()
				print lineBreak
			if(choice == 1): #quit
				print 'Exiting the program. GG EZ.'
				sys.exit()
			



