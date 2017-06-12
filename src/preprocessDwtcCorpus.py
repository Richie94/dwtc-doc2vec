# coding=UTF-8
import sys, copy, glob
import ujson as json
from guess_headers import guessHeaders
from clean_table import *
from check_table import checkTable, checkSize
from table_to_html_parse import *
import config
import os.path
import re

def cleanText(text):
	#zwischen zwei ; löschen
	if len(text.split(";")) > 2:
		text = text.split(";")[0]
	text = config.RE_STYLE_1.sub('', text)
	text = config.RE_STYLE_2.sub('', text)
	text = config.RE_STYLE_3.sub('', text)
	text = config.RE_STYLE_4.sub('', text)
	text = text.split("}")[0]
	text = text.split("{")[0]
	return text


def saveTable(id, table, filename):
	with open(config.KEEP+filename, "a") as f:
		#also take words in url into count
		line = ' '.join(re.split('\/|\.|-|_', table["url"].split("?")[0])) + "\t"
		#entity line is nearly same but all entitys in table are with _ instead of space -> 1 word
		entityLine = ""

		line += cleanText(table["textBeforeTable"])+ "\t"
		entityLine += line

		if config.MULT_HEADER and table["hasHeader"] == True:

			if table["headerPosition"] == "FIRST_COL":
				#transpose table
				table["relation"] = [list(i) for i in zip(*table["relation"])]

			#skip header row
			for column in table["relation"][1:]:
				for i, entry in enumerate(column):
					try:
						line += " " + str(table["relation"][0][i]) + " " + str(entry)
						entityLine += " " + str(table["relation"][0][i].replace(" ", "_")) + " " + str(entry).replace(" ", "_")
					except:
						pass
				line += "\t"
				entityLine += "\t"
		else:
			for column in table["relation"]:
				for entry in column:
					try:
						line += " " + str(entry)
						entityLine += " " + str(entry).replace(" ", "_")
					except:
						pass
				line += "\t"
				entityLine += "\t"

		line += cleanText(table["textAfterTable"])+ "\t"
		entityLine += cleanText(table["textAfterTable"])+ "\t"

		line = ' '.join([x for x in line.split(" ") if config.RE_NO_RUBBISH.match(x)])
		line = id + "\t" + line
		line += "\n"
		line = line.encode('utf-8')
		f.write(line)

		entityLine = ' '.join([x for x in entityLine.split(" ") if config.RE_NO_RUBBISH.match(x)])
		entityLine = id + "\t" + entityLine
		entityLine += "\n"
		entityLine = entityLine.encode('utf-8')

		with open(config.KEEP_ENTITY+filename, "a") as g:
			g.write(entityLine)

		


if __name__ == "__main__":
	total, accepted = 0, 0,
	for foldername in [x for x in glob.glob(config.DATA+"*") if len(x.split("/")[-1].split(".")) == 1]:
		print("Folder: ", foldername)
		cleanedFoldername = foldername.split("/")[-1]
		if os.path.isfile(config.KEEP+cleanedFoldername+".txt"):
			print(cleanedFoldername + " already done")
			continue

		for jsonFile in glob.glob(foldername+"/*.json"):
			table = json.loads(open(jsonFile, "r").read())
			total += 1
			if total % 100 == 0:
				print(total, accepted)
			table["relation"] = initialCleanTable(table["relation"])

			if checkTable(table):
				accepted += 1
				saveTable(jsonFile, table, cleanedFoldername+".txt")


	
