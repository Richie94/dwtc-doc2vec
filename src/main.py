# coding=UTF-8
import config, glob
from tableToDoc import *
from gensim.models.doc2vec import Doc2Vec
from gensim.utils import RULE_KEEP, RULE_DISCARD
import time


def findMostSimilarTable(table, model, topn=10):
	# table has to be in style uid \t row \t row ...
	vec = model.infer_vector(transformTableToOneDoc(table))
	return model.docvecs.most_similar(positive=[vec], topn=topn)


def trimCorpus(word, count, min_count):
	if count < min_count:
		return RULE_DISCARD
	else:
		#check for Valid WordStructure
		if config.RE_NO_NUMBER.match(word):
			return RULE_KEEP
		else:
			return RULE_DISCARD

def getModelName(lines):
	modelname = config.MODELS + "_" 
	modelname += config.METHOD + "_"
	modelname += str(config.DM) + "_" 
	modelname += str(config.ITER) + "_"
	modelname += str(config.MINCOUNT) + "_"
	modelname += str(config.HS) + "_"
	modelname += str(config.DM_MEAN) + "_"
	modelname += str(config.DBOW_WORDS) + "_"
	modelname += str(lines) + "_" 
	modelname += str(config.WINDOW_SIZE) + "_"
	modelname += str(config.DIMENSIONS) + '.doc2vec'
	return modelname



if __name__ == "__main__":
	t1 = time.time()
	#1. combine all subfiles to a new one
	lines = 0
	with open("all_together.txt", "w") as f:
		for filename in glob.glob(config.KEEP + "*.txt"):
			with open(filename, "r") as g:
				text = g.read()
				f.write(text)
				lines += len(text.split("\n"))
				print("Current file:" + str(filename) + " - total lines: " + str(lines))

	#2. feed combined document into our TaggedDocumentGenerator
	if config.METHOD == "MULTI":
		documents = OneDocMultiLine("all_together.txt")
	else:
		documents = OneDocOneLine("all_together.txt")

	modelname = getModelName(lines)

	print("Processed Documents")

	t2 = time.time()
	model = Doc2Vec(documents, dm=config.DM, hs = config.HS, dm_mean = config.DM_MEAN, dbow_words=config.DBOW_WORDS, size=config.DIMENSIONS, window=config.WINDOW_SIZE, min_count=config.MINCOUNT, workers=2, iter=config.ITER, trim_rule=trimCorpus)
	t3 = time.time()
	model.save(modelname)

	print("Took: %f for preprocess and %f for modelbuilding" % (t2-t1, t3-t2))

	testWords = ["richard", "melanie", "berlin", "obama", "internet", "car", "city"]
	for word in testWords:
		print model.most_similar(word)