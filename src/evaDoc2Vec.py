import config
from glob import glob
from gensim.models.doc2vec import Doc2Vec
from collections import defaultdict

def getReaTableDict():
	tableDict = defaultdict(lambda:set())
	with open(config.REA_OUTPUT, "rb") as f:
		lines = f.read().split("\n")
		for line in lines:
			if len(line.split("\t")) == 5:
				tableUrl1, tableNum1, tableUrl2, tableNum2, score = line.split("\t")
				table1Name = "SENT_" + str(tableUrl1) + "-" + str(tableNum1)
				table2Name = "SENT_" + str(tableUrl2) + "-" + str(tableNum2)
				
				tableDict[table1Name].add((table2Name, score))
				tableDict[table2Name].add((table1Name, score))
	return tableDict

def findMostSimilarTables(table, model, topn=10, processed=False):
	if processed == False:
		#TODO: consider MULTI/SINGLE
		#table has to be in style uid \t row \t row ...
		vec = model.infer_vector(transformTableToOneDoc(table))
	else:
		vec = table
	return model.docvecs.most_similar(positive=[vec], topn=topn)

# multiple variants:
# a) transform rea picks to scale 1,-1 and then look for similiar scores
# b) take reaPicks > 0.3 score as relatively okay 
def getModelScore(model, reaTables):
	#1. pick some random tables
	
	scores, allPositions = [], []
	for table in reaTables:
		positions = []
		notInCorpus = 0
		#2. see which ones REA is picking
		reaPicks = reaTables[table]
		#3. look in TOP1000 where these ones are findable and return position
		try:
			top1000table2Vec = [x[0] for x in findMostSimilarTables(table, model, topn=1000, processed=True)]
			for (table2, score) in reaPicks:
				print table2, score
				# variant b
				if score < 0.3:
					continue
				try:
					print("Search "+str(table2))
					positions.append(top1000table2Vec.index(table2))
					print("\tFound")
				except Exception, e:
					#print str(e)
					# TO CHECK
					if table2 not in model.docvecs:
						notInCorpus += 1
					pass
			#4. calc some score: the more are in top1000 the better, the closer to top 10 the better
			# -> amount found in top1000/ average position of index
			allPositions.append(positions)
			averagePosition = sum(positions)/len(positions)
			amountFound = len(positions)/(len(reaPicks)-notInCorpus)
			scores.append(amountFound/averagePosition)
		except Exception, e:
			#print str(e)
			pass
		
	return sum(scores)/len(scores), scores, notInCorpus
			
reaTables = getReaTableDict()
print(len(reaTables.keys()))
s = 0
for entry in reaTables:
	s += len(reaTables[entry])
print(s)
for modelname in glob(config.MODELS+"*.doc2vec"):
	model = Doc2Vec.load(modelname)
	print getModelScore(model,reaTables)
