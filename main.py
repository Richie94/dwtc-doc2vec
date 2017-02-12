# coding=UTF-8
import ujson as json
import sys, re, string, math
from table_reader import TableReader
import enchant
from collections import defaultdict
from gensim import corpora, models, similarities

MIN_ROW_AMOUNT = 4
MIN_COL_AMOUNT = 4

RE_NUMBER = re.compile('^[\-]?([0-9]*,?)*[0-9]*\.?[0-9]*$')
# TODO: check this regex, still not fure because regexes are aweful
RE_VALID = re.compile('.*[a-z,A-Z,0-9].*')


def initReprDict():
	reprDict = defaultdict(lambda: "X")
	for char in string.ascii_lowercase:
		reprDict[char] = "S"
	for char in string.ascii_uppercase:
		reprDict[char] = "S"
	for number in range(10):
		reprDict[str(number)] = "N"
	reprDict["."] = "P"
	reprDict["_"] = "U"
	reprDict[" "] = "E"
	return reprDict

reprDict = initReprDict()

def checkSize(table):
	rowAmount = len(table["relation"])
	colAmount = len(table["relation"][0])
	if colAmount >= MIN_COL_AMOUNT and rowAmount >= MIN_ROW_AMOUNT:
		return True
	else:
		return False

def checkLanguage(header):
	d = enchant.Dict("en_US")
	englishCount, foreignCount = 0, 0
	header = [word for word in header if len(word) > 3]
	for word in header:
		# check if it is a word or multi-word
		wordSplit = word.split(" |-")
		if len(wordSplit) == 1:
			if d.check(word):
				englishCount += 1
			else:
				foreignCount += 1
		else:
			#idea: maybe there is and englisch word with a number behind 
			#so give englisch word more value than splits behind
			for splittedWord in wordSplit:
				if d.check(splittedWord):
					englishCount += 1
				else:
					foreignCount += 0.5
	if float(englishCount)/(foreignCount+englishCount) > 0.7:
		return True
	else:
		return False

def word2Repr(word):
	representation = ""
	for char in word:
		representation += reprDict[char]
	return representation

def table2Repr(table):
	newTable = table[:]
	for i, column in enumerate(table):
		for j, row in enumerate(column):
			newTable[i][j] = word2Repr(table[i][j])
	return newTable

def mostDivergentEntry(column):
	#print column
	# Idea: 1st count occurencys from our patternized table
	# Then normalize it and calculate distance for every word and return the one with highest distance
	colOcc = {}
	for word in column:
		for char in word:
			if char in colOcc:
				colOcc[char] += 1
			else:
				colOcc[char] = 1

	print colOcc
	# Normalization
	for entry in colOcc:
		colOcc[entry] /= len(column)
	
	print colOcc
	maxDiv, maxDivIndex = 0, -1

	for i, word in enumerate(column):
		wordOcc = defaultdict(lambda: 0)
		wordDiv = 0
		for char in word:
			wordOcc[char] += 1
			

		for entry in colOcc:
			wordDiv += abs(wordOcc[entry]-colOcc[entry])

		if wordDiv > maxDiv:
			maxDiv = wordDiv
			maxDivIndex = i

	print maxDivIndex
	return maxDivIndex



# returns: boolean headerBroken, boolean rowHeader (row vs col), array header
def checkSpecialRows(table):
	rowHeader = True
	headers = []
	reprTable = table2Repr(table)
	# 1st run: check rowHeaders
	# transpose = [list(i) for i in zip(*table)]
	divergentLines = []
	for column in reprTable:
		divergentLines.append(mostDivergentEntry(column))
	print divergentLines
		




	return False, headers, rowHeader

# returns: boolean headerBroken, boolean rowHeader (row vs col), array header
def checkHeader(table):
	# header direction
	rowHeader = True
	headers = []

	if table["headerPosition"] == "FIRST_ROW":
		rowHeader = True
		headers = [h[0] for h in table["relation"]]
	elif table["headerPosition"] == "FIRST_COLUMN":
		rowHeader = False
		headers = table["relation"][0]
	elif table["headerPosition"] == "MIXED":
		#relatively dirty header, so not keep him
		return True, rowHeader, headers
	elif table["headerPosition"] == "NONE":
		return checkSpecialRows(table)
	return False, rowHeader, headers

def checkTable(table):
	if checkSize(table) == False:
		return False
	else:
		headersBroken, rowHeader, headers = checkHeader(table)
		if headersBroken == False:
			return False
		elif checkLanguage(headers) == False:
			return False
		return True

def cleanTable(table):
	return table

def keepTable(table):
	table = cleanTable(table)
	pass

if __name__ == "__main__":
	print checkSpecialRows([["Wer", "Hans", "Peter", "Klaus", "Bernhard"],["Wann wird gekocht ", "18:30","18:30","18:30","18:30"], ["Wie viele?", "2", "2","2", "2"]])
	if (len(sys.argv) > 1):
		for arg in sys.argv[1:]:
			reader = TableReader(arg)
			table = reader.get_next_table()
			while (table):
				if reader.line_count == 1:
					print(table)
				if checkTable(table):
					keepTable(table)
				table = reader.get_next_table()