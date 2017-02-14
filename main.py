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
	#print guessHeaders([["Wer kommt alles?", "Hans", "Peter", "Klaus", "Bernhard"],["Wann wird gekocht?", "18:30","18:30","18:30","18:30"], ["Wie viele?", "2", "2","2", "2"]])
	#print guessHeaders([[u'CONSTRUCTION', u'Steel', u'Steel', u'Aluminum'], [u'MOBILE', u'With Casters', u'No Casters', u'With Casters'], [u'DESCRIPTION', u'With Connection Hinge', u'With Connection Hinge', u'With Connection Hinge'], [u'COLOR', u'Yellow/Black', u'Yellow/Black', u'Yellow/Black'], [u'H"', u'40', u'37', u'39-9/16'], [u'FOLDED', u'16', u'15-1/2"', u'15-1/4'], [u'EXPANDED', u'141', u'137"', u'139'], [u'IMAGE', u'Quick View', u'Quick View', u'Quick View'], [u'MODEL', u'WB955042', u'WB955040', u'WB239451'], [u'QTY', u'See Product Details', u'See Product Details', u'See Product Details'], [u'PRICE', u'$132.00', u'$200.95', u'$323.95']])

	with open( "html_test.html", "w") as f:
		f.write("\n")

	if (len(sys.argv) > 1):
		for arg in sys.argv[1:]:
			reader = TableReader(arg)
			table = reader.get_next_table()

			while (table):

				table["relation"] = initialCleanTable(table["relation"])
				tableAccepted, headerType ,indexHeader = checkTable(table)
				if indexHeader != []:
					print tableAccepted, headerType, indexHeader 
				if headerType != 0:
					print(table["relation"])
					keepTable(table)
					parseTableToHTML(table, "html_test.html", headerType, indexHeader)
				#if table["url"] == "http://www.pro-football-reference.com/players/P/ParsBo00/gamelog/1976/":
				#	break
				table = reader.get_next_table()