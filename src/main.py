# coding=UTF-8
import config
from collections import defaultdict
from glob import glob
from random import randint
from tableToDoc import *
from ParameterCombination import *
from gensim.models.doc2vec import Doc2Vec
from gensim.utils import RULE_KEEP, RULE_DISCARD
from time import time
import os


def trimCorpus(word, count, min_count):
	if count < min_count:
		#1. check for minamount as usual
		return RULE_DISCARD
	else:
		#2. check for Valid WordStructure (has been done in preprocessing already)
		#if config.RE_NO_NUMBER.match(word):
		return RULE_KEEP
		#else:
		#	return RULE_DISCARD

def checkIfExists(combi):
	_tmpname = combi.getModelName("multheader_"+str(" ")).split("_")
        del _tmpname[1]
        for otherModel in glob(config.MODELS+"*.doc2vec"):
        	_tmpsplit = otherModel.split("_")
                del _tmpsplit[1]   
                if _tmpname == _tmpsplit:
			print str(_tmpname) + str("already exists")
                	return True
	return False



if __name__ == "__main__":	

	for combi in targetCombinationsToParam("../targetCombinations.txt"):
	#for combi in getParameterCombinations():
		#so far there are pretty much combinations so make some randomized search instead of grid
		#if randint(0,100) > 50:
		#	with open("skipped_combinations.txt", "a") as f:
		#		f.write(combi.getModelName(0) + "\n")
		#	continue
		
		if checkIfExists(combi):
			continue				

		#1. feed combined document into our TaggedDocumentGenerator
		if combi.p["METHOD"] == "MULTI":
			documents = OneDocMultiLine(combi.p["WINDOW_SIZE"])
		else:
			documents = OneDocOneLine(combi.p["WINDOW_SIZE"])
		print("Processed Documents")		
		#2. calculate the model
		modelname = combi.getModelName("multheader_"+str(documents.lineAmount()))
		
		print("Calculate Model " + str(modelname))	

		t1 = time()
		model = Doc2Vec(documents,dm=combi.p["DM"],
			hs=combi.p["HS"],dm_mean=combi.p["DM_MEAN"],size=combi.p["DIMENSIONS"],
			window=combi.p["WINDOW_SIZE"],min_count=combi.p["MINCOUNT"],
			workers=2,iter=combi.p["ITER"],negative=combi.p["NEGATIVE"],
			sample=combi.p["SAMPLE"],trim_rule=trimCorpus)
		model.save(modelname)
		print("\tSaved Model  in " + str(time()-t1) + "s")
		del documents
		del model
