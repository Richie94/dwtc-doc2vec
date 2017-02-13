# coding=UTF-8
import sys
from table_reader import TableReader
from clean_table import *
from check_table import checkTable
import config
from gensim import corpora, models, similarities


def keepTable(table):
	laterCleanTable(table)
	pass

if __name__ == "__main__":
	print guessHeaders([["Wer", "Hans", "Peter", "Klaus", "Bernhard"],["Wann wird gekocht ", "18:30","18:30","18:30","18:30"], ["Wie viele?", "2", "2","2", "2"]])
	if (len(sys.argv) > 1):
		for arg in sys.argv[1:]:
			reader = TableReader(arg)
			table = reader.get_next_table()
			while (table):
				if checkTable(table):
					print(table["relation"])
					keepTable(table)
				table = reader.get_next_table()