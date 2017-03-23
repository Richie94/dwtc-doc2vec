import config
import enchant
from collections import defaultdict
from guess_headers import guessHeaders
import ujson as json
from re import split
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

def checkDomain(url):
	domainEnding = url.split("/")[2].split(".")[-1]
	if domainEnding in config.ALLOWED_DOMAINS:
		return True
	else:
		return False

def checkLanguage(header):
	d = enchant.Dict("en_US")
	englishCount, foreignCount = 0, 0
	header = [word.encode('utf-8') for word in header if len(word) > 4]
	header = [str(word) for word in header if not word.isdigit()]
	
	for word in header:
		# check if it is a word or multi-word
		wordSplit = split(" |-|(|)|:", word)
		wordSplit = [w.replace("-", "").replace("(", "").replace(")","").replace(":", "") for w in wordSplit if w != None]
		wordSplit = [w for w in wordSplit if len(w) > 3]

		if len(wordSplit) == 1:
			# had unspecified error, therefore i catch it
			try:
				if d.check(word):
					englishCount += 1
				else:
					foreignCount += 1
			except:
				pass
		elif len(wordSplit) > 1:
			#idea: maybe there is an english word with a number behind 
			#so give english word more value than splits behind
			for splittedWord in wordSplit:
				try:
					if d.check(splittedWord):
						englishCount += 1
					else:
						foreignCount += 0.5
				except:
					pass

	if englishCount + foreignCount == 0:
		return False

	if float(englishCount)/(foreignCount+englishCount) > 0.45:
		return True
	else:
		return False

def checkHeader(cleanedTable):
	return guessHeaders(cleanedTable)

# returns if the check was positive, headertype and headerindex
def checkTable(table):
	if 	checkDomain(table["url"]) == False:
		return False, 0, []
	elif checkSize(table["relation"]) == False:
		return False, 0, []
	else:
		headerType, indexHeader = checkHeader(table["relation"])

		# Just domain check right now
		#check for language, need to transform headers into one array
		headerText = []
		if headerType == 1 or headerType == 3:
			for pos in indexHeader[0]:
				headerText.extend([col[pos] for col in table["relation"]])
		elif headerType == 2 or headerType == 3:
			for pos in indexHeader[1]:
				headerText.extend(table["relation"][pos])

		if len(headerText) > 0:
			if checkLanguage(headerText) == False:
				return False, headerType, indexHeader 


		return (headerType != 0 and headerType != 3), headerType, indexHeader