# coding=UTF-8
import config
from glob import glob

with open(config.URL_LIST, "w") as g:
	for filename in glob(config.KEEP+"*.txt"):
		with open(filename, "rb") as f:
			lines = f.read().split("\n")
			for i in range(len(lines)/500):
				identifier = lines[i].split("\t")[0]
				tableUrl = ''.join(identifier.split("-")[:-1])
				tableNum = identifier.split("-")[-1]
				g.write(tableUrl + "\t" + tableNum + "\n")

