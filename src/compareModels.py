import config
from gensim.models.doc2vec import Doc2Vec
from table_to_html_parse import *
from glob import glob
from collections import defaultdict
from sklearn.cluster import KMeans, DBSCAN
import cPickle as pickle
import ujson as json

def ensembleClusters(results, threshhold=0.5):
	w = len(results[0])
	amount = len(results)
	matrix = [[0.0 for x in range(w)] for y in range(w)] 

	for result in results:
		for i, elem1 in enumerate(result):
			for j, elem2 in enumerate(result):
				if elem1 == elem2:
					matrix[i][j] = matrix[i][j] + (1.0/amount)

	clusters = defaultdict(lambda:set())
	for i, col in enumerate(matrix):
		for j, row in enumerate(col):
			if matrix[i][j] > threshhold:
				clusters[i].add(j)
				clusters[j].add(i)

	accepted = []
	for key in clusters:
		elem = clusters[key]
		if len(accepted) == 0:
			accepted.append(elem)
		else:
			ersetzt = False
			for i, x in enumerate(accepted):
				if elem.issubset(x):
					accepted[i] = elem
					ersetzt = True
					break
				elif x.issubset(elem):
					ersetzt = True
					break
			if not ersetzt:
				accepted.append(elem)

	for a in accepted:
		print(a)


def getSomeTestingTags(model):
	tagsToTest = []
	for i in range(len(model.docvecs)/10000):
		tagsToTest.append(model.docvecs.index_to_doctag(i*10000))
	return tagsToTest


def calcIntersection():
	allTags = defaultdict(lambda:set())
	pairwiseTags = defaultdict(lambda: {})

	testTags = []
	first = True

	for filename in glob(config.MODELS + "700112_*.doc2vec"):
		print("Load model " + filename)
		model = Doc2Vec.load(filename)
		if first:
			testTags = getSomeTestingTags(model)
		print("Done")
		for tag in testTags:
			try:
				model_output = set([x[0] for x in model.docvecs.most_similar([tag], topn=1000)])
				if first:
					allTags[tag] = model_output
				else:
					allTags[tag] = allTags[tag].intersection(model_output)

				pairwiseTags[tag][filename] = model_output
			except Exception,e: 
				print str(e)
		del model
		first = False

	print("Results from total intersection")
	zeroCounter = 0
	for tag in allTags:
		if len(allTags[tag]) > 0:
			print (tag, len(allTags[tag]))
		else:
			zeroCounter += 1	
	print(str(zeroCounter) + " entrys 0")	

	sumDict = defaultdict(lambda:0)
	print("Results from pairwise intersection")
	with open("intersection_dwtc.txt", "wb") as f:
		for tag in pairwiseTags:
			for modelname_a in pairwiseTags[tag]:
				for modelname_b in pairwiseTags[tag]:	
					if modelname_a < modelname_b:
						sumDict[modelname_a+"\t"+modelname_b] += len(pairwiseTags[tag][modelname_a].intersection(pairwiseTags[tag][modelname_b]))
		for entry in sumDict:
			f.write(entry + "\t"+ str(sumDict[entry]) + "\n") 

def tryToFindClusters(testingVectors):
	results = {}
	allTables = set()
	counter = 0
	# 1. get results for each vector for each model
	for filename in glob(config.MODELS + "700112_*.doc2vec"):
		print(counter, " of ", len(glob(config.MODELS + "700112_*.doc2vec")), " models checked")
		model = Doc2Vec.load(filename)
		model_results = {}

		for test in testingVectors:
			v = model.infer_vector(test, steps=15)
			ms = model.docvecs.most_similar([v], topn=100)
			model_results[' '.join(test)] = ms
			for table in ms:
				allTables.add(table[0])

		results[filename] = model_results
		counter += 1

	pickle.dump(results, open("results.p", "wb"))
	print("Dumped results")

	# 2. build feature vectors
	tableMapper, i = {}, 0
	for table in allTables:
		tableMapper[table] = i
		i += 1

	featureVectors = []
	for filename in results:
		vec = [-1]*len(allTables)
		for test in results[filename]:
			for table in results[filename][test]:
				tableId = tableMapper[table[0]]
				vec[tableId] = table[1]
				
		featureVectors.append((vec,filename))

	for a in featureVectors:
		for b in featureVectors:
			if a <= b:
				continue
			s = 0
			for i in range(len(a[0])):
				s += abs(a[0][i]-b[0][i])
			if a > b:
				print (a[1], b[1], s)


	pickle.dump(featureVectors, open("save_features.p", "wb" ) )
	print("Built feature vectors")

	kmeans = KMeans(n_clusters=8, random_state=0).fit_predict([x[0] for x in featureVectors])
	
	clusters = defaultdict(lambda:[])
	y = [x[1] for x in featureVectors]

	for i, prediction in enumerate(kmeans):
		clusters[prediction].append(y[i])

	print("Predicted clusters")
	return clusters, results

def printHTMLForModels(modelnames):
	testingVectors = [["rebounds", "germany", "basketball"],["gdp", "population", "country", "citizens"], ["salary", "country", "continent"]]
	for modelname in modelnames:
		print("Load Model" + modelname + " ...")
		model = Doc2Vec.load(modelname)
		print("Model loaded")
		for test in testingVectors:
			print("\tRun test " + str(test) + " ...")
			_vec = model.infer_vector(test)
			results = model.docvecs.most_similar([_vec])
			for result in results:
				jsonFile = json.loads(open(result[0], "rb").read())
				parseTableToHTML(jsonFile["relation"], modelname + "_"  + str(test) + ".html")
		del model

def printHTMLForModel(model, modelname, vector):
	#results = model.docvecs.most_similar([vector])
	for result in results:
		jsonFile = json.loads(open(result[0], "rb").read())
		parseTableToHTML(jsonFile["relation"], modelname + vector + ".html")


def testClusters():	
	testingVectors = [["rebounds", "germany", "basketball"],["gdp", "population", "country", "citizens"], ["salary", "country", "continent"]]
	clusters, results = tryToFindClusters(testingVectors)
	print("Start building html")
	# now pick one "representative" from cluster
	for cluster in clusters:
		representative = clusters[cluster][0]
		model_results = results[representative]
		for test in model_results:
			#generate html output for all tables in model_results[test]
			for similarTable in model_results[test]:
				tableData = json.loads(open(similarTable[0]).read())
				parseTableToHTML(tableData["relation"], representative + "_"  + test + ".html")

def vecDist(vecA, vecB):
	s = 0
	if len(vecA) != len(vecB):
		print("Wrong length")
	else:
		for i in range(len(vecA)):
			s += (vecA[i] - vecB[i]) * (vecA[i] - vecB[i])
	return s

def createSpread():
	with open("save_features.p", "rb") as f:
		featureVectors = pickle.load(f)
		kmeans = KMeans(n_clusters=8, random_state=0).fit_predict([x[0] for x in featureVectors])
		#db = DBSCAN(eps=0.05, min_samples=10).fit_predict([x[0] for x in featureVectors])
		
		clusters = defaultdict(lambda:[])
		nameToCluster = {}
		y = [x[1] for x in featureVectors]

		for i, prediction in enumerate(kmeans):
			clusters[prediction].append(y[i])
			nameToCluster[y[i]] = prediction

		allDist = defaultdict(lambda:0)
		mostCentral = defaultdict(lambda:("", 100000000))
		for fv1 in featureVectors:
			for fv2 in featureVectors:
				if fv1[1] >= fv2[1]:
					if nameToCluster[fv1[1]] == nameToCluster[fv2[1]]:
						allDist[fv1[1]] += vecDist(fv1[0], fv2[0])
						allDist[fv2[1]] += vecDist(fv1[0], fv2[0])

		for name in allDist:
			pred = nameToCluster[name]
			if mostCentral[pred][1] > allDist[name]:
				mostCentral[pred] = (name, allDist[name])

		for mc1 in mostCentral:
			for mc2 in mostCentral:
				for fv1 in featureVectors:
					if mostCentral[mc1][0] == fv1[1]:
						for fv2 in featureVectors:
							if mostCentral[mc2][0] == fv2[1]:
								print(mc1, mc2, vecDist(fv1[0], fv2[0]))


		print(clusters)
		print(mostCentral)
		
		with open("test.csv", "wb") as f:
			for cluster in clusters:
				for filename in clusters[cluster]:
					splittedName = filename.split("/")[-1].split("_")
					for s in splittedName:
						f.write(s + ",")
					f.write("\n")
				f.write("\n")

def compDWTC():
	querys = [["gdp", "country", "population", "continent"], ["country", "total", "forest", "area"], ["continent", "salary"]]
	#scoreDict = {}
	output = {}
	filenames = glob(config.MODELS + "700112_*.doc2vec")
	for i, modelname in enumerate(filenames):
		print("Load model " + str(modelname) + " (" + str(i) + "/" + str(len(filenames)) + ")")
		model = Doc2Vec.load(modelname)
		allSim = []
		for query in querys:
			v = model.infer_vector(query)
			allSim.extend([x[0] for x in model.docvecs.most_similar([v], topn=5)])
		#print allSim
		output[modelname] = allSim
		#score = raw_input("Score: ")
		#scoreDict[modelname] = int(score)

	pickle.dump(output, open("output.p", "w"))

def scoreOutput():
	with open("output.p", "rb") as f:
		output = pickle.load(f)
		scoreDict = {}
		for modelname in output:
			print output[modelname]
			score = raw_input("Score: ")
			scoreDict[modelname] = int(score)
	pickle.dump(scoreDict, open("scoreDict.p", "w"))



modelsToTest = ["../models/multheader_1910957_1_300_0_1_0_15_1e-05_20_20_SINGLE.doc2vec", 
				"../models/multheader_1910957_1_300_0_1_0_15_1e-05_10_20_SINGLE.doc2vec", 
				"../models/multheader_1910957_1_300_1_1_10_15_1e-05_20_20_SINGLE.doc2vec",
				"../models/multheader_1910957_1_300_1_0_10_15_1e-05_10_5_SINGLE.doc2vec",
				"../models/multheader_1910957_1_300_1_0_10_15_1e-05_20_20_SINGLE.doc2vec",
				"../models/multheader_1910957_1_300_0_0_0_15_1e-05_10_20_SINGLE.doc2vec",
				"../models/multheader_1910957_1_300_0_0_10_15_0_10_20_SINGLE.doc2vec"]

modelsOpen = ["../models/multheader_1910957_1_500_0_1_0_15_1e-05_10_20_SINGLE.doc2vec", "../models/multheader_1910957_1_800_0_1_0_15_1e-05_10_20_SINGLE.doc2vec"]
#printHTMLForModels(modelsOpen)
scoreOutput()
#calcIntersection()
# Good results for:
# multheader_1910957_1_300_0_1_0_15_1e-05_10_20_SINGLE.doc2vec
# multheader_1910957_1_300_0_1_0_15_1e-05_20_20_SINGLE.doc2vec

