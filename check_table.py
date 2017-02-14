import config
import enchant
from collections import defaultdict
from guess_headers import guessHeaders
import ujson as json
from clean_table import *

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
	if englishCount + foreignCount == 0:
		return False
	if float(englishCount)/(foreignCount+englishCount) > 0.7:
		return True
	else:
		return False

def checkHeader(cleanedTable):
	return guessHeaders(cleanedTable)


# returns if the check was positive, rowheader and headerindex
def checkTable(table):
	if checkSize(table["relation"]) == False:
		return False, 0, []
	else:
		print table["url"]
		headerType, indexHeader = checkHeader(table["relation"])
		print headerType, indexHeader
		#if headersBroken == True or textHeader == []:
		#	return False, rowHeader, indexHeader
		#elif checkLanguage(textHeader) == False:
		#	return False, rowHeader, indexHeader
		return True, headerType, indexHeader