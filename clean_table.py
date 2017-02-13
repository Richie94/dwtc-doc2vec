import config

def laterCleanTable(table):
	# What we dont need:
	# 1. Columns/Rows Consisting primarily of numbers
	return deleteSpecificFromTable(table, config.RE_NO_NUMBER)

def initialCleanTable(table):
	# What we dont need:
	# 1. Empty Columns (and/or rows)
	return deleteSpecificFromTable(table, config.RE_NO_RUBBISH)

def deleteSpecificColumns(table, regex):
	tableWithoutEmptyColumns = [] 
	for column in table:
		nonEmptyEntrys = 0
		for element in column:
			if regex.match(element):
				nonEmptyEntrys += 1
			if float(nonEmptyEntrys)/len(column) > 0.5:
				tableWithoutEmptyColumns.append(column)
				break
	return tableWithoutEmptyColumns

def deleteSpecificFromTable(table, regex):
	tableWithoutSpecificColumns = deleteSpecificColumns(table, regex)
	transpose = [list(i) for i in zip(*tableWithoutSpecificColumns[:])]
	tableWithoutSpecificRows = deleteSpecificColumns(transpose, regex)
	return [list(i) for i in zip(*tableWithoutSpecificRows[:])]


