# coding=UTF-8

def parseTableToHTML(table, filename):
	transpose = [list(i) for i in zip(*table)]
	html = "<table>"
	for row in transpose:
		html += "<tr>"
		for entry in row:
			html += "<td>"
			html += entry.encode('utf-8').strip() + "</td>"
		html += "</tr>"
	html += "</table><hr>"

	with open(filename, "a") as f:
		f.write(html + "\n")
