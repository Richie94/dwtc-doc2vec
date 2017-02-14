# coding=UTF-8

def generateHeaderPositions(table, headerType, indexHeader):
	positions = []
	colAmount = len(table)
	rowAmount = len(table[0])
	if headerType > 0:
		if headerType == 1 or headerType == 3:
			#some rows are headers
			for i in indexHeader[0]:
				for j in range(colAmount):
					positions.append((i,j))

		if headerType == 2 or headerType == 3:
			#some cols are headers
			for i in indexHeader[1]:
				for j in range(rowAmount):
					positions.append((j,i))
	return positions
	



def parseTableToHTML(table, filename, headerType, indexHeader):
	# 1. generate all (i,j) which are headers
	positions = generateHeaderPositions(table["relation"], headerType, indexHeader)
	html = "<table>"
	if headerType:
		transpose = [list(i) for i in zip(*table["relation"])]
		for i, row in enumerate(transpose):
			html += "<tr>"
			for j, entry in enumerate(row):
				if (i,j) in positions:
					html += '<td style="color:red">'
				else:
					html += "<td>"
				html += entry.encode('utf-8').strip() + "</td>"
			html += "</tr>"
	html += "</table><hr>"

	with open(filename, "a") as f:
		f.write(html + "\n")
