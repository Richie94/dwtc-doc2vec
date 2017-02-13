# coding=UTF-8
from collections import defaultdict
import string, math, operator
import config
import numpy as np


def initPatternDict():
	patternDict = defaultdict(lambda: "X")
	for char in string.ascii_lowercase:
		patternDict[char] = "s"
	for char in string.ascii_uppercase:
		patternDict[char] = "S"
	for number in range(10):
		patternDict[str(number)] = "N"
	patternDict["."] = "P"
	patternDict[","] = "P"
	patternDict[";"] = "P"
	patternDict[":"] = "P"
	patternDict["_"] = "U"
	patternDict["/"] = "U"
	patternDict["\\"] = "U"
	patternDict["-"] = "U"
	patternDict[" "] = "E"
	patternDict["€"] = "D"
	patternDict["$"] = "D"
	return patternDict

patternDict = initPatternDict()
impactFactor = {"S": 1,
				"s": 1,
				"N": 7,
				"P": 10,
				"U": 10,
				"E": 10,
				"X": 10,
				"D": 10}

# returns: boolean headerBroken, boolean rowHeader (row vs col), array header
def guessHeaders(table):
	headers = []
	transpose = [list(i) for i in zip(*table)]
	patternTable = table2Pattern(table)
	transposePattern = [list(i) for i in zip(*patternTable)]
	
	#print "Row"
	totalRowDivDict = getTableDivergencyDict(patternTable)
	#print "COl"
	totalColDivDict = getTableDivergencyDict(transposePattern)
	
	indexHeader, textHeader = [], []

	# calculate standard deviation, normally where is less stddev should be the right orientation
	rowVals = sorted([totalRowDivDict[key] for key in totalRowDivDict])
	colVals = sorted([totalColDivDict[key] for key in totalColDivDict])
	

	#print rowVals
	#print colVals


	rowStd = np.std(rowVals[:-1])
	colStd = np.std(colVals[:-1])
	
	#print rowStd, colStd
	

	if rowStd < colStd:
		# assume rows are headers
		rowHeader = True
		maxRowEntry, maxRowValue = max(totalRowDivDict.iteritems(), key=operator.itemgetter(1))
		indexHeader = [maxRowEntry]
		textHeader = transpose[indexHeader[0]]
		
		#TODO: Multiple headers? Possible but does not occur too often
		#headerRows = [item for item in totalRowDivDict if totalRowDivDict[item] > math.ceil(maxRowValue*0.80)]
		
	else:
		# assume cols are headers
		rowHeader = False
		maxColEntry, maxColValue = max(totalColDivDict.iteritems(), key=operator.itemgetter(1))
		indexHeader = [maxColEntry]
		textHeader = table[indexHeader[0]]

	
	return False, rowHeader, indexHeader, textHeader

def word2Pattern(word):
	pattern = ""
	for char in word:
		pattern += patternDict[char]
	return pattern

def table2Pattern(table):
	newTable = []
	for i, column in enumerate(table):
		newCol = []
		for j, row in enumerate(column):
			newCol.append(word2Pattern(row))
		newTable.append(newCol)
	return newTable

def getColumnDivergencyDict(column):
	# Idea: 1st count occurencys from our patternized table
	# Then normalize it and calculate distance for every word
	colOcc = {}
	for word in column:
		# Entrys like --- or empty entrys could exists which we skip here
		if config.RE_NO_RUBBISH.match(word):
			for char in word:
				if char in colOcc:
					colOcc[char] += 1
				else:
					colOcc[char] = 1

	# Normalization
	for entry in colOcc:
		colOcc[entry] = math.ceil(float(colOcc[entry])/len(column))
	#print colOcc
	divDict = {}

	for i, word in enumerate(column):
		if config.RE_NO_RUBBISH.match(word):
			wordOcc = defaultdict(lambda: 0)
			wordDiv = 0
			for char in word:
				wordOcc[char] += 1
				
			for entry in colOcc:
				wordDiv += abs(wordOcc[entry]-colOcc[entry])*impactFactor[entry]

			divDict[i] = float(wordDiv)/len(column)
	
	return divDict

def normalizeDefDict(defDict):
	maxEntry, maxValue = max(defDict.iteritems(), key=operator.itemgetter(1))
	minEntry, minValue = min(defDict.iteritems(), key=operator.itemgetter(1))
	if maxValue != minValue:
		for entry in defDict:
			defDict[entry] = 100*((defDict[entry])-minValue)/(maxValue-minValue)
	return defDict


def getTableDivergencyDict(table):
	totalDivDict = {}
	for column in table:
		columnDivDict = getColumnDivergencyDict(column)
		#print columnDivDict
		for key in columnDivDict:
			if key in totalDivDict:
				totalDivDict[key] += columnDivDict[key]
			else:
				totalDivDict[key] = columnDivDict[key]

	return normalizeDefDict(totalDivDict)

# returns the maximum distance to average
def maxDistToAverage(divDict):
	average = sum([divDict[entry] for entry in divDict])/len(divDict)
	maxDist = 0
	for entry in divDict:
		currentDist = abs(divDict[entry]-average)
		if maxDist < currentDist:
			maxDist = currentDist
	return maxDist