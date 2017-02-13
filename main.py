# coding=UTF-8
import sys
from table_reader import TableReader
from guess_headers import guessHeaders
from clean_table import *
from check_table import checkTable
from table_to_html_parse import *
import config
from gensim import corpora, models, similarities

def keepTable(table):
	laterCleanTable(table)
	pass

if __name__ == "__main__":
	print guessHeaders([["Wer kommt alles?", "Hans", "Peter", "Klaus", "Bernhard"],["Wann wird gekocht?", "18:30","18:30","18:30","18:30"], ["Wie viele?", "2", "2","2", "2"]])
	
	with open( "html_test.html", "w") as f:
		f.write("\n")

	if (len(sys.argv) > 1):
		for arg in sys.argv[1:]:
			reader = TableReader(arg)
			table = reader.get_next_table()

			while (table):

				table["relation"] = initialCleanTable(table["relation"])
				tableAccepted, rowHeader, indexHeader = checkTable(table)
				print tableAccepted, rowHeader, indexHeader 
				if tableAccepted:
					print(table["relation"])
					keepTable(table)
					parseTableToHTML(table, "html_test.html", rowHeader, indexHeader)
				table = reader.get_next_table()