import glob
from gensim import models
import config

def scaleToTen(x, maxV, minV):
	# cosine similarity -> [1,-1]
	# transform it to 0-10
	return 10 * (x - minV) / (maxV - minV)

with open(config.EVA, "r") as f:
	lines = f.read().split("\n")[1:]

	for filename in glob.glob(config.MODELS+"*.doc2vec"):
		print filename
		positives, negatives = 0, 0
		model = models.doc2vec.Doc2Vec.load(filename)
		for line in lines:
			splittedLine = line.split("\t")
			word1, word2, similarity = splittedLine[0], splittedLine[1], splittedLine[2]

			if word1 == word2:
				continue

			try:
				
				ourSimilarity = model.similarity(word1, word2)

				highestSimilarity = max(model.most_similar(word1)[0][1], model.most_similar(word2)[0][1])
				
				farthest1 = model.most_similar(negative=[word1])[0][0]
				farthest2 = model.most_similar(negative=[word2])[0][0]
				farthestSimilarity = min(model.similarity(word1, farthest1), model.similarity(word2, farthest2))
				
				similarityScore = scaleToTen(ourSimilarity, highestSimilarity, farthestSimilarity)

				if ourSimilarity > highestSimilarity:
					continue


				if abs(float(similarityScore) - float(similarity)) < 2:
					positives += 1
				else:
					negatives += 1

				#print word1, word2, "%.2f" % similarityScore, similarity, ourSimilarity, highestSimilarity, farthestSimilarity

			except Exception as e:
				#print e
				pass

		print positives, negatives
	
