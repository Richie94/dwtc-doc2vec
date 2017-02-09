import ujson as json
import sys
from table_reader import TableReader

MIN_ROW_AMOUNT = 4
MIN_COL_AMOUNT = 4

def checkSize(table):
	rowAmount = len(table["relation"])
	colAmount = len(table["relation"][0])
	if colAmount >= MIN_COL_AMOUNT and rowAmount >= MIN_ROW_AMOUNT:
		return True
	else:
		return False

def checkLanguage(table):
	return False

def checkHeader(table):
	# header direction
	rowHeader = True
	headers = []

	if table["headerPosition"] == "FIRST_ROW":
		rowHeader = True
	elif table["headerPosition"] == "FIRST_COLUMN":
		rowHeader = False
	elif table["headerPosition"] == "MIXED":
		#relatively dirty header, so not keep him
		return True, rowHeader, headers

	

	return False, rowHeader, headers

def checkTable(table):
	if checkSize(table) == False:
		return False
	elif checkLanguage(table) == False:
		return False
	else:
		headersBroken, rowHeader, headers = checkHeader(table)
		if headersBroken == False:
			return False
		return True

def cleanTable(table):
	return table

def keepTable(table):
	table = cleanTable(table)
	pass

if __name__ == "__main__":
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