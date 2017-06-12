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

def checkHeader(cleanedTable):
	return guessHeaders(cleanedTable)

# returns: if the check was positive, headertype and headerindex
def checkTable(table):
	if checkSize(table["relation"]) == False:
		return False
	else:
		return True