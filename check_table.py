import config
import enchant
from collections import defaultdict
from guess_headers import guessHeaders
import ujson as json

def checkSize(table):
	try:
		rowAmount = len(table)
		colAmount = len(table[0])
	except:
		return False
	if colAmount >= config.MIN_COL_AMOUNT and rowAmount >= config.MIN_ROW_AMOUNT:
		return True
	else:
		return False

def checkLanguage(header):
	# Maybe TODO: check domain?
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
			#so give english word more value than splits behind
			for splittedWord in wordSplit:
				if d.check(splittedWord):
					englishCount += 1
				else:
					foreignCount += 0.5
	if float(englishCount)/(foreignCount+englishCount) > 0.7:
		return True
	else:
		return False

# returns: boolean headerBroken, boolean rowHeader (row vs col), array header
def checkHeader(table, cleanedTable):
	# header direction
	rowHeader = True
	indexHeader, textHeader = [0], []

	if table["headerPosition"] == "FIRST_ROW":
		rowHeader = True
		textHeader = [h[0] for h in table["relation"]]
	elif table["headerPosition"] == "FIRST_COLUMN":
		rowHeader = False
		textHeader = table["relation"][0]
	elif table["headerPosition"] == "MIXED":
		#relatively dirty header, so not keep him
		return True, rowHeader, indexHeader, textHeader
	elif table["headerPosition"] == "NONE":
		return guessHeaders(cleanedTable)

	return False, rowHeader, indexHeader, textHeader

def checkTable(table):
	cleanedTable = initialCleanTable(table["relation"])
	if checkSize(cleanedTable) == False:
		return False
	else:
		print table["url"]
		headersBroken, rowHeader, indexHeader, textHeader = checkHeader(table, cleanedTable)
		print headersBroken, rowHeader, indexHeader, textHeader
		if headersBroken == False or textHeader == []:
			return False
		elif checkLanguage(textHeader) == False:
			return False
		return True