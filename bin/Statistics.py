import numpy as np
import pandas as pd


class Statistics:

	#Constructor
	def __init__(self, cleanedData):
		#store the data locally and get each group.
		self.data = cleanedData
		self.groupPositions = self.data.groupby("LeagueIndex")
		
	#Returns statistics on the dataset given, grouped by LeagueIndex
	def getStatistics(self):
		#For each league...
		pd.set_option('display.max_columns', 500)
		groupData = list()
		for league, group in self.groupPositions:
			print("League: ", league)
			print(group.describe())
			
			groupData.append([league, group.describe(include = "all")])
		return groupData