# coding=UTF-8
import sys, copy, glob
from table_reader import TableReader
from guess_headers import guessHeaders
from clean_table import *
from check_table import checkTable, checkSize
from table_to_html_parse import *
import config
import os.path

def keepTable(table, indexHeader):
	removedHeader = removeHeaderAndOrientate(table["relation"], indexHeader)
	return laterCleanTable(removedHeader)
	
def saveTable(id, table, filename):
	with open(filename, "a") as f:
		line = id + "\t"
		for column in table["relation"]:
			for entry in column:
				try:
					line += " " + str(entry)
				except:
					pass
			line += "\t"
		line += "\n"
		f.write(line)


if __name__ == "__main__":
	total, accepted, cleanAccepted = 0, 0, 0
	for filename in glob.glob(config.DATA+"*"):
		cleanedFilename = filename.split("\\")[-1]
		print filename

		if os.path.isfile(config.KEEP+cleanedFilename+".txt"):
			print("Already processed")
			continue

		reader = TableReader(filename)
		table = reader.get_next_table()

		while (table):
			total += 1
			if total % 100 == 0:
				print(filename, total, accepted, cleanAccepted)
			table["relation"] = initialCleanTable(table["relation"])
			# Accepts header if: 
			# 1. Correct Domain
			# 2. Correct Size
			# 3. (Non Mixed) Header Recognized
			# 5. Correct Language in Header
			tableAccepted, headerType, indexHeader = checkTable(table)
			if tableAccepted:
				accepted += 1
				table["relation"] = keepTable(table, indexHeader)
				if len(table["relation"]) > 0:
					cleanAccepted += 1
					saveTable(reader.get_name() + "-" + str(reader.get_line_count()), table, config.KEEP+cleanedFilename+".txt")

			table = reader.get_next_table()

	