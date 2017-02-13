from collections import defaultdict
import string, math, operator
import config
import numpy as np


def initPatternDict():
	patternDict = defaultdict(lambda: "X")
	for char in string.ascii_lowercase + string.ascii_uppercase:
		patternDict[char] = "S"
	for number in range(10):
		patternDict[str(number)] = "N"
	patternDict["."] = "P"
	patternDict[":"] = "P"
	patternDict["_"] = "U"
	patternDict["/"] = "U"
	patternDict["\\"] = "U"
	patternDict["-"] = "U"
	patternDict[" "] = "E"
	return patternDict

patternDict = initPatternDict()
impactFactor = {"S": 1,
				"N": 7,
				"P": 10,
				"U": 10,
				"E": 10,
				"X": 10}

# returns: boolean headerBroken, boolean rowHeader (row vs col), array header
def guessHeaders(table):
	headers = []
	transpose = [list(i) for i in zip(*table)]
	patternTable = table2Pattern(table)
	transposePattern = [list(i) for i in zip(*patternTable)]
		
	#colDist = float(maxDistToAverage(totalColDivDict))/len(totalColDivDict)
	#rowDist = float(maxDistToAverage(totalRowDivDict))/len(totalRowDivDict)
	
	totalRowDivDict, maxRows = getTableDivergencyDict(patternTable)
	totalColDivDict, maxCols = getTableDivergencyDict(transposePattern)
	
	indexHeader, textHeader = [], []

	# calculate standard deviation, normally where is less stddev should be the right orientation
	rowVals = [totalRowDivDict[key] for key in totalRowDivDict]
	colVals = [totalColDivDict[key] for key in totalColDivDict]

	rowStd = np.std(rowVals)
	colStd = np.std(colVals)
	print rowVals
	print colVals
	print rowStd, colStd
	

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
	# Then normalize it and calculate distance for every word and return the one with highest distance
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

def getTableDivergencyDict(table):
	totalDivDict = {}
	maxLines = {}
	for column in table:
		columnDivDict = getColumnDivergencyDict(column)

		#get Max Entry
		maxEntry, maxValue = max(columnDivDict.iteritems(), key=operator.itemgetter(1))
		if maxEntry in maxLines:
			maxLines[maxEntry] += 1
		else:
			maxLines[maxEntry] = 1

		for key in columnDivDict:
			if key in totalDivDict:
				totalDivDict[key] += columnDivDict[key]
			else:
				totalDivDict[key] = columnDivDict[key]

	# normalize dict
	maxEntry, maxValue = max(totalDivDict.iteritems(), key=operator.itemgetter(1))
	if maxValue != 0:
		for entry in totalDivDict:
			totalDivDict[entry] = 100*float(totalDivDict[entry])/maxValue

	return totalDivDict, maxLines

# returns the maximum distance to average
def maxDistToAverage(divDict):
	average = sum([divDict[entry] for entry in divDict])/len(divDict)
	maxDist = 0
	for entry in divDict:
		currentDist = abs(divDict[entry]-average)
		if maxDist < currentDist:
			maxDist = currentDist
	return maxDist