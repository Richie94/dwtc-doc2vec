# coding=UTF-8
from gensim.models.doc2vec import TaggedDocument

# General notice: if algorithm dbow us used, there should be no difference between both approaches

#Approach 1: 1 table = 1 document
# 	Pro: 	easy, fast
# 	Contra: maybe wrong orientation -> column/line, no information use from lines
class OneDocOneLine(object):
	def __init__(self, filename):
		self.filename = filename
		with open(self.filename, "r") as f:
			self.lines = f.read().split("\n")

	def __iter__(self):
		for line in self.lines:
			yield transformTableToOneDoc(line)

#Approach 2: 1 table = x lines + y columns
# 	Pro: 	complete information use
#	Contra: slower
class OneDocMultiLine(object):
	def __init__(self, filename):
		self.filename = filename
		with open(self.filename, "r") as f:
			self.lines = f.read().split("\n")

	def __iter__(self):
		for line in self.lines:
			rowsAndCols = transformTableToRowsAndCols(line)
			for (uid, text) in rowsAndCols:
				yield TaggedDocument(words=text.lower().split(), tags=['SENT_%s' % uid])

def transformTableToOneDoc(table):
	splittedLine = table.split("\t")
	uid = splittedLine[0]
	text = (' _' * config.WINDOW_SIZE).join(splittedLine[1:])
	return TaggedDocument(words=text.lower().split(), tags=['SENT_%s' % uid])

def transformTableToRowsAndCols(table):
	rowsAndCols = []
	uid = table.split("\t")[0]
	for s in table.split("\t")[1:]:
		rowsAndCols.append((uid,s))
	#transform rawtext to tablelike structure from json 
	tableLike = [i.strip().split(" ") for i in table.split("\t")[1:]]
	transpose = [' '.join(i) for i in zip(*tableLike)]
	for s in transpose:
		rowsAndCols.append((uid,s))
	return rowsAndCols