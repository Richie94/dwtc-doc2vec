import config

class ParameterCombination(object):
	def __init__(self, ITER, DM, WINDOW_SIZE, MINCOUNT, DM_MEAN, DIMENSIONS, SAMPLE, METHOD, HS, NEGATIVE):
		self.p = {}
		self.p["ITER"] = ITER
		self.p["DM"] = DM
		self.p["WINDOW_SIZE"] = WINDOW_SIZE
		self.p["MINCOUNT"] = MINCOUNT
		self.p["DM_MEAN"] = DM_MEAN
		self.p["DIMENSIONS"] = DIMENSIONS
		self.p["SAMPLE"] = SAMPLE
		self.p["METHOD"] = METHOD
		self.p["HS"] = HS
		self.p["NEGATIVE"] = NEGATIVE

	def getModelName(self, lines):
		modelname = config.MODELS + str(lines)
		for key in self.p:
			modelname += "_" + str(self.p[key]) 
		modelname += '.doc2vec'
		return modelname

	def toString(self):
		return self.getModelName(0)

def targetCombinationsToParam(filename):
	combis = []
	with open(filename, "rb") as f:
		lines = f.read().split("\n")
		for line in lines:
			splittedLine = line.split("_")
			if len(splittedLine) > 9:
				it = int(splittedLine[6])
				dm = int(splittedLine[1])
				win = int(splittedLine[8])
				mincount = int(splittedLine[9])
				dmmean = int(splittedLine[3])
				dimension = int(splittedLine[2])
				sample = float(splittedLine[7])
				method = splittedLine[10].split(".")[0]
				hs = int(splittedLine[4])
				neg = int(splittedLine[5])
				combis.append(ParameterCombination(it, dm, win, mincount, dmmean, dimension, sample, method, hs, neg))
	return combis

def getParameterCombinations():
	combis = []
	for paramDict in [config.paramsDM, config.paramsDBOW]:
		for it in paramDict["ITER"]:
			for dm in paramDict["DM"]:
				for win in paramDict["WINDOW_SIZE"]:
					for mincount in paramDict["MINCOUNT"]:
						for dmmean in paramDict["DM_MEAN"]:
							for dimension in paramDict["DIMENSIONS"]:
								for sample in paramDict["SAMPLE"]:
									for method in paramDict["METHOD"]:
										for hs in paramDict["HS"]:
											for neg in paramDict["NEGATIVE"]:
												combis.append(ParameterCombination(it, dm, win, mincount, dmmean, dimension, sample, method, hs, neg))
	return combis
