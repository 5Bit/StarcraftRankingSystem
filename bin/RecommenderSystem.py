from itertools import izip
import numpy as np
import pandas as pd
import math
from numpy import linalg as linalg
#RecommenderSystem Class
class RecommenderSystem(object): #Note to self - have to inheret from object in 2.7


	#Constructor - handles importing normalization data for each column
	# for any classification attempts.
	#Also requires the dataframe of the cleaned, normalized data.
	def __init__(self, colData, df):
		self.columnData = colData
		self.rsDf = df
		#groupPositions
		self.groupPositions = self.rsDf.groupby("LeagueIndex")
		
		
	
	#Used to calculate the cosine similarity between two given arrays
	#Assumes array1 and array2 is given as an array.
	#array2 is the otheruser
	def cosSim(self, array1, array2):
		pureX, pureY, comboXY = 0, 0, 0
		for array1i, array2i in izip(array1, array2):
			pureX += array2i * array2i
			pureY += array1i * array1i
			comboXY += array1i*array2i
			
			if(pureX == 0 or pureY ==0):
				return 0
		return comboXY / math.sqrt(abs(pureX) * abs(pureY))
	
	
	# Classifies the user's league. 
	#Assumes the data is given to it without being normalized or having gameID
	#or Age removed.
	#Assumes data is complete, and does not contain any Nans.
	#assumed userdata given as an numpy array
	def classifyUser(self, userData, k):
		
		#finish normalization process
		myZScore = userData
		
		#for each column, calculate the user's Z-score for that val.
		#skip the first as that's league
		i = 1
		for colMean, colStddev in self.columnData:
			if (i != 0):
				myZScore[i] = (userData[i] - colMean)/colStddev
				
			i +=1
			
		
		#print userData
		
		#For each group, get it's K most similar
		topKPerGroup = list()
		avgPerGroup = list()
		for league, group in self.groupPositions:
			print "Analyzing similarity in Group ", league, "\n"
			#print group
			#For each player in this group, calculate the similarity
			simList = list()
			for i, otherUser in group.iterrows():
				playerWithoutLeague = userData[1:] #Skip league for the userdata
				simList.append([i, self.cosSim(playerWithoutLeague, otherUser)])

			#Once they are all calculated, sort them by the cosine similarity
			#print simList[:10]
			simList.sort(key = lambda j: j[1])
			
			#only retain K
			simList = simList[:k]
			#print simList
			#Get the top k simlists
			topKPerGroup.append(simList[:k])
			
			#Calculate the average for the group
			groupTotal = float(0)
			for player, simVal in simList:
				groupTotal += simVal
				
			groupTotal = groupTotal/(float(len(simList)))
			#print "group total", groupTotal
			#append it
			avgPerGroup.append(groupTotal)
			
		
		#Next, find league with largest similarity (1 is optimal)
		#First, sort the list and get the index (With the most similar at top)
		groupIndexes = self.groupPositions.groups.keys()
		#print avgPerGroup
		optimalIndex = sorted(range( len( avgPerGroup )), key = lambda i: avgPerGroup[i])
		print "Optimal Group index", optimalIndex

		
		#get the bestGroup
		groupNumber = groupIndexes[optimalIndex[0]]
		
		bestGroup = self.groupPositions.get_group(groupNumber)
		

		#return the optimal group number, it's avg distance, it's top K similar.
		returnList = [groupNumber, avgPerGroup[optimalIndex[0]], topKPerGroup[optimalIndex[0]]]
		
		return returnList
	