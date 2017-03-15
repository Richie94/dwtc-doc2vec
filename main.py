# coding=UTF-8
import config, glob
from gensim import models
from gensim.utils import RULE_KEEP, RULE_DISCARD
import time

#Var 1: Tabelle = 1 Dokument, genug Trennsymbole zwischen Spalten lassen
# 	Pro: 	einfach, schnell
# 	Contra: eventuell falsche Orientierungen, Zeileninformation wird nicht genutzt
class OneDocOneLine(object):
	def __init__(self, filename):
		self.filename = filename
		with open(self.filename, "r") as f:
			self.lines = f.read().split("\n")

	def __iter__(self):
		for line in self.lines:
			yield transformTableToOneDoc(line)

#Var 2: Tabelle wird zerlegt in Spalten und Reihen als einzelne Dokumente, 
#       später ist dann ein aufsummieren nötig um das ähnlichste Dokument zu finden
# 	Pro: 	komplette Informationsnutzung
#	Contra: deutlich langsamer
class OneDocMultiLine(object):
	def __init__(self, filename):
		self.filename = filename
		with open(self.filename, "r") as f:
			self.lines = f.read().split("\n")

	def __iter__(self):
		for line in self.lines:
			rowsAndCols = transformTableToRowsAndCols(line)
			for (uid, text) in rowsAndCols:
				yield models.doc2vec.TaggedDocument(words=text.lower().split(), tags=['SENT_%s' % uid])

def transformTableToOneDoc(table):
	splittedLine = table.split("\t")
	uid = splittedLine[0]
	text = (' _' * config.WINDOW_SIZE).join(splittedLine[1:])
	return models.doc2vec.TaggedDocument(words=text.lower().split(), tags=['SENT_%s' % uid])

def transformTableToRowsAndCols(table):
	rowsAndCols = []
	uid = table.split("\t")[0]
	for s in table.split("\t")[1:]:
		rowsAndCols.append((uid,s))

	#transform rawtext in tablelike 
	tableLike = [i.strip().split(" ") for i in table.split("\t")[1:]]
	transpose = [' '.join(i) for i in zip(*tableLike)]
	for s in transpose:
		rowsAndCols.append((uid,s))

	return rowsAndCols

def findMostSimilarTable(table, model):
	# table has to be in style uid \t row \t row ...
	if config.METHOD == "MULTI":
		print table
		vecs = transformTableToRowsAndCols(table)
		print vecs
		scoreDict = {}
		for line in vecs:
			vec = model.infer_vector(line)
			for (tag, score) in model.docvecs.most_similar([vec]):
				if tag in scoreDict:
					scoreDict[tag] += score
				else:
					scoreDict[tag] = score
		return sorted(scoreDict.iteritems(), key=lambda (k,v): (v,k), reverse=True)
	else:
		vec = model.infer_vector(transformTableToOneDoc(table))
		return model.docvecs.most_similar([vec])


def trimCorpus(word, count, min_count):
	if count < min_count:
		return RULE_DISCARD
	else:
		#check for Valid WordStructure
		if config.RE_NO_NUMBER.match(word):
			return RULE_KEEP
		else:
			return RULE_DISCARD


if __name__ == "__main__":
	t1 = time.time()
	#1. combine all subfiles to a new one
	lines = 0
	docCount = 0
	with open("all_together.txt", "w") as f:
		for filename in glob.glob(config.KEEP+"*"):
			print filename
			docCount += 1
			if docCount > 18:
				continue
			with open(filename, "r") as g:
				text = g.read()
				f.write(text)
				lines += len(text.split("\n"))
				print lines

	if config.METHOD == "MULTI":
		documents = OneDocMultiLine("all_together.txt")
	else:
		documents = OneDocOneLine("all_together.txt")

	print("Processed Documents")
	t2 = time.time()
	model = models.doc2vec.Doc2Vec(documents, size=100, window=config.WINDOW_SIZE, min_count=5, workers=2, iter = 15, trim_rule=trimCorpus)
	t3 = time.time()
	model.save('my_model.doc2vec')
	print("Took: %f for preprocess and %f for modelbuilding" % (t2-t1, t3-t2))
	print model.most_similar("richard")
	print model.most_similar("melanie")
	print model.most_similar("berlin")
			

# Parameters for Doc2Vec
# dm: Different Algorithms ->  Options: 1, 2 	
# size: Dimension of feature vector
# window: window around each word
# alpha: initial learning rate
# min_count: ignores words with lower count
# sample: downsample high frequ word -> Options: 0, 1e-5
# workers: multicore
# iter: Number of epochs -> Std: 5, Pptions 10, 20 ..
# hs: hierachichal sampling (1: on, 0: off)  ???
# negative: amount of drawned noise words
# dm_mean: 0: sum of contect word 1: dm_mean
# dm_concat: 0: off 1:on -> results in pretty large corpus
# dbow_words: 0: faster 1: dbow training ???
# trim: zahlen, ():


# Document nachträglich testen mit:
# d = model_loaded.infer_vector("text")
# model_loaded.docvecs.most_similar([a]) -> Labels der Sätze komme raus