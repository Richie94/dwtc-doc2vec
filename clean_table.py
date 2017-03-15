import config

def laterCleanTable(table):
	# What we dont need:
	# 1. Columns/Rows Consisting primarily of numbers
	numberLess = deleteSpecificFromTable(table, config.RE_NO_NUMBER, thresh = 0.5)
	#moreThenOneSign = deleteSpecificFromTable(numberLess, config.RE_MULT_CHAR, thresh = 0.5)
	return numberLess

def initialCleanTable(table):
	# What we dont need:
	# 1. Empty Columns (and/or rows)
	# 2. Where is nearly no variance - TODO
	no_rubbish = deleteSpecificFromTable(table, config.RE_NO_RUBBISH, thresh=0.5)
	return deleteSpecificFromTable(no_rubbish, config.RE_NO_NUMBER, thresh=0.00001)

def removeHeaderAndOrientate(table, indexHeader):
	if len(indexHeader[0]) > 0:
		transpose = [list(i) for i in zip(*table)]
		return transpose[indexHeader[0][-1]+1:]
	elif len(indexHeader[1]) > 0:
		return table[indexHeader[1][-1]+1:]

def deleteSpecificColumns(table, regex, thresh=0.5):
	tableWithoutEmptyColumns = [] 
	for column in table:
		nonEmptyEntrys = 0
		for element in column:
			if regex.match(element):
				nonEmptyEntrys += 1
			if float(nonEmptyEntrys)/len(column) >= thresh:
				tableWithoutEmptyColumns.append(column)
				break
	return tableWithoutEmptyColumns

def deleteSpecificFromTable(table, regex, thresh=0.5):
	tableWithoutSpecificColumns = deleteSpecificColumns(table, regex, thresh = thresh)
	transpose = [list(i) for i in zip(*tableWithoutSpecificColumns)]
	tableWithoutSpecificRows = deleteSpecificColumns(transpose, regex, thresh = thresh)
	return [list(i) for i in zip(*tableWithoutSpecificRows)]


