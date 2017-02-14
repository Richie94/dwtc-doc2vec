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

# returns: boolean headerBroken, int headerType (nothing = 0, row=1, col=2, mixed=3), array header [[rowHeaders],[colHeaders]]
def guessHeaders(table):
	# TODO: For Mixed headers
	# Idea 1: run same again with cutted header (while loop) -> need for threshhold (10, 15?)
	# Idea 2: look for both stddev and have a threshhold of mb 2x min stddev
	# idea: loop it until no stddev is below threshhold
	# if e.g. rowstddev is below add the next top row to headers
	rowOffset, colOffset = 0, 0
	indexHeader = ([],[])
	headerType = 0
	_table = table[:]
	while True:
		print rowOffset, colOffset

		headers = []
		transpose = [list(i) for i in zip(*_table)]
		patternTable = table2Pattern(_table)
		transposePattern = [list(i) for i in zip(*patternTable)]
		
		totalRowDivDict = getTableDivergencyDict(patternTable)
		totalColDivDict = getTableDivergencyDict(transposePattern)

		# calculate standard deviation, normally where is less stddev should be the right orientation
		rowVals = sorted([totalRowDivDict[key] for key in totalRowDivDict])
		colVals = sorted([totalColDivDict[key] for key in totalColDivDict])

		#print "VALS:", rowVals, colVals
		rowStd = np.std(rowVals[:-1])
		colStd = np.std(colVals[:-1])

		if math.isnan(rowStd) or rowStd == 0.0:
			rowStd = 1000
		if math.isnan(colStd) or colStd == 0.0:
			colStd = 1000

		print "STD:", rowStd, colStd


		# threshhold for maximum stddev
		if (rowStd > config.MAX_STD_DEV and colStd > config.MAX_STD_DEV) or (rowStd < 1 and colStd < 1):
			print "Table too high stddev"
			break 
		if len(table) < config.MIN_COL_AMOUNT or len(table[0]) < config. MIN_ROW_AMOUNT:
			print "Table too small "
			break

		if rowStd < colStd:
			print "Row Chosen as Header"
			# assume rows are headers
			# MAXVAL vs First Etry?!
			#maxRowEntry, maxRowValue = max(totalRowDivDict.iteritems(), key=operator.itemgetter(1))
			if headerType == 0 or headerType == 2:
				headerType += 1
			indexHeader[0].append(rowOffset)
			rowOffset += 1
			_table = [entry[1:] for entry in _table]
		else:
			print "COl Chosen as Header"
			# assume cols are headers
			# MAXVAL vs First Etry?!
			if headerType == 0 or headerType == 1:
				headerType += 2
			indexHeader[1].append(colOffset)
			colOffset += 1
			_table = _table[1:]
	
	return headerType, indexHeader

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
	if len(defDict) > 0:
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