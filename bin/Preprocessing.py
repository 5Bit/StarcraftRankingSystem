import sys
import math
import collections
import numpy as np

lineBreak = "-------------------------------------------------------------\n"



#Handles data preprocessing
class Preprocessing(object): #Note to self - have to inheret from object in 2.7

	#Constructor - Needs to know the 
	def __init__(self, acceptableLoss):
		self.accLoss = 1.00 - float(acceptableLoss)/float(100)
		self.colData = list()
			
			
	#Handles cleaning data it is given.
	#Data must be given as a pandas df.
	#Eliminates data and removes until it is at the acceptable loss percentage.
	#input: Dataframe
	#output: Cleaned dataframe that has removed as many Nans as it can while maintaining acceptable Loss percentage
	def CleanData(self, inData):
	
	
		#First, identify rows with nulls/NaNs.
		print("Data Cleaning in process.")
		print("Found nulls/NaNs in the following rows:")
		localData = inData
		colHasNulls = list()
		for column in localData:
			hasNull = localData[column].isnull().values.any()
			if(hasNull):
				print(column, ": ", hasNull)
			colHasNulls.append(hasNull)
			
		withNulls = [i for i, isNull in enumerate(colHasNulls) if isNull == True]
		
		#Next, figure out which rows have a NaN/Null
		#find the rows in each column that has a nan

		nullPositions = list()
		for i in withNulls:
			rowsWithNulls = list()
			for j, row in localData.iterrows():
				if(math.isnan(row[i])):
					rowsWithNulls.append(j)
			nullPositions.append(rowsWithNulls)
			
		#First, determine the number of rows with nan.
		#Now that we have a list of null positions, go through and determine the number of rows with multiple nans
		#do this by flattening the list and looking for doubles - if it equals the length of the parent list, consider removing.


		flatten = lambda lis: [i for sublist in lis for i in sublist]
		flattenedNullPos = flatten(nullPositions)
		#print flattenedNullPosNullPos
		
		nansPerRow = self.CountDuplicates(flattenedNullPos)
		#Get the min and max 
		maxNans = max(nansPerRow, key=nansPerRow.get)
		minNans = min(nansPerRow, key=nansPerRow.get)
		#print nansPerRow
		#maxNans = max(nansPerRow)
		#minNans = min(nansPerRow)
		originalDataSize = float(len(localData))
		
		
		if originalDataSize > 0: #if more rows than 0...
			#if length of duplicates is greater than the acceptable loss, then just drop them.
			print("Data is larger than 0")
			
			
			if(float(len(nansPerRow))/originalDataSize) < self.accLoss:
				print("Removing all rows with nans, as it will be still be meeting expectations.")
				positions = list(nansPerRow.keys())
				#print positions
				localData.drop(positions, inplace = True)
				print(len(localData))
				return localData
			else:
				#get the details about nan positions...
				detailedPos = self.nanPositionsPerRow(nansPerRow, localData)
				
				#drop all rows missing league, regardless of anything. These are useless.
				#Remove from both the local data and nansPerRow
				for i in detailedPos:
					if 1 in i[1]:
						localData.drop(i[0])
						nansPerRow.drop(i[0])
				
				
				currentDataSize = float(len(localData))
				nextDataSize =  currentDataSize - 1.0
				
				#if under the acceptable losses, suggest increasing acceptable losses and throw error.
				if(currentDataSize/originalDataSize < self.accLoss):
					print("The amount of data lost is more than the acceptable losses.")
					print("Adjust your expectations or gather more data and try again.")
					quit()
				#if at acceptable losses or just under it, return the localData
				elif(nextDataSize/originalDataSize <= self.accLoss):
					return localData
				
				#otherwise, cut rows with larger null counts. Check if just under acceptable
				#loss before every iteration.
				#for every nan count from top to bottom...
				breakFromLoop = False
				for i in range(maxNans,minNans, -1):
					#for every nansPerRow
					if breakFromLoop:
						break
					for key, val in nansPerRow.iteritems():
						#if the row exists 
						if(val == i): #if this value meets the removal criteria
							#drop it from the table and the dictionary
							localData.drop(key)
							nansPerRow.drop(key)
						
						#if we are just above the target percentage
						#calculate next percentage of originalDataSize
						nextPercent = (float(len(localData)) - 1.0)/ originalDataSize
						if nextPercent < self.accLoss:
							breakFromLoop = True
							break
							
				
		
				if len(localData) ==0: #nothing left after cleaning. Return error
					print("No data is left after cleaning.")
					print("Adjust your expectations or gather more data and try again.")
					quit()
				else:
					print(localData)
					return localData
		else:
			#return an error saying issue with Data - check if it meets specifications.
			print("The data did not meet the software's expectations.")
			print("Verify your data is A CSV and has data within it.")
			quit()

	#Handles normalizing the data as it is given, and estimating any NaNs left.
	#Also functions as some cleaning, removing gameID (as that has no relevance to a RS)
	#Data must be given as a pandas df.
	#input: Dataframe
	#output: Cleaned dataframe that has removed as many Nans as it can while maintaining acceptable Loss percentage
	#output: Also outputs a copy of the the column data (mean, stddev)
	def Normalization(self, inData):
	
		localData = inData
		#First, removes gameID and Age
		localData = localData.drop('GameID', 1)
		localData = localData.drop('Age', 1)
		print("Data Normalization in process.")

		
		#TODO if time permits , average based on group instead
		#Fill in nans with the avg...
		localData.fillna(localData.mean())
		
		
		
		#Finally, calculate Z-score for each item. Store the mean and standard deviation.
		newLocalData = self.ZScore(localData)
		

		return [newLocalData, self.colData]
		
		
		
	#Calculates the Z-score for a column. Returns the column, mean and standard deviation for later.
	def ZScore(self, inData):
		localData = inData
		
		for column in localData:
			if(column != "LeagueIndex"):
				colMean = localData[column].mean()
				colStd = localData[column].std()
				colInfo = list()
				colInfo.append(colMean)
				colInfo.append(colStd)
				localData[column] = (localData[column] - colMean)/colStd
				self.colData.append(colInfo)
		
		return localData
		
		
		
	#Function will count the number of duplicates. Requires the list to be flattened and sorted.
	def CountDuplicates(self, inList):
		inList = sorted(inList)
		#print inList
		nansPerRow = collections.Counter(inList)
		return nansPerRow
		
	#Takes in a a dictionary of locations of duplicates and their nans
	def nanPositionsPerRow(self, nanDict, dataframe):
		nanPosPerRow = list()
		for key, val in nanDict.iteritems():
			#go to the row, find the columns with null
			rowInfo = list()
			colsWithNan = list()
			count = 0
			#for each column in the row, count the nans and store them in a list.
			for column in dataframe.iloc[key]:
				if np.isnan(column):
					colsWithNan.append(count)
				count += 1
			#store each row's list of nan index positions and store that in rowInfo with the row position(key)
			rowInfo.append(key)
			rowInfo.append(colsWithNan)
			#store the row's info in nanPosPerRow
			nanPosPerRow.append(rowInfo)
		return nanPosPerRow		