import re, glob
from gensim import models
import config
from table_reader import TableReader

def parseTableToHTML(table, filename, targetTable=False):
	html = "<table>"
	if targetTable:
		html += "<hr><hr>"
	transpose = [list(i) for i in zip(table)]
	for i, row in enumerate(table):
		html += "<tr>"
		for j, entry in enumerate(row):
			html += "<td>"
			html += entry.encode('utf-8').strip() + "</td>"
		html += "</tr>"
	html += "</table><hr>"
	if targetTable:
		html += "<hr>"

	with open(filename, "a") as f:
		f.write(html + "\n")

togetherList = []

for filename in glob.glob(config.MODELS+"*.doc2vec"):
	print filename
	togetherDict = {}
	model = models.doc2vec.Doc2Vec.load(filename)

	with open(config.KEEP+"dwtc-001.json.gz.txt") as f:
		lines = f.read().split("\n")[:5]
		labels = [("SENT_" + str(line.split("\t")[0])) for line in lines]

	for targetLabel in labels:

		similarLabelPairs = model.docvecs.most_similar([targetLabel])
		print similarLabelPairs
		togetherDict[targetLabel.split("\\")[-1]] = [a[0].split("\\")[-1] for a in similarLabelPairs]
		
		#for similarLabel in [(targetLabel, 1)] + similarLabelPairs:
		#	targetFileName = config.DATA + similarLabel[0].split("\\")[1].split(" ")[0] + ".json.gz"
		#	reader = TableReader(targetFileName)
		#	targetTable = reader.get_line(int(similarLabel[0].split("-")[-1]))["relation"]

		#	transpose = [list(i) for i in zip(*targetTable)]
		#	parseTableToHTML(transpose, config.EVA+filename.split(config.MODELS)[1]+".html", similarLabel in [(targetLabel, 1)])

	togetherList.append(togetherDict)
print togetherList
for key in togetherList[0]:
	for d in togetherList:
		print d[key]


			#targetFileName = similarLabel[0].split("\\")[1].split(" ")[0] + ".json.gz.txt"
			#with open(config.KEEP+targetFileName, "r") as g:
				#reg = re.compile(similarLabel[0].split("_")[1].replace("\\", "\\\\")+"\t.*?\n", re.MULTILINE)
				#searchedTable = re.search(reg, g.read()).group()
				#tableWithoutIndex = '\t'.join(searchedTable.split("\t")[1:])
				
				#tableLike = [i.strip().split(" ") for i in tableWithoutIndex.strip().split("\t")]
				#transpose = [list(i) for i in zip(*tableLike)]

				#parseTableToHTML(transpose, "test.html", similarLabel in [(targetLabel, 1)])
				
				

				





