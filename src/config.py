import re

MIN_ROW_AMOUNT = 4
MIN_COL_AMOUNT = 3
MAX_STD_DEV = 5	

ALLOWED_DOMAINS = ['org', 'us', 'gov', 'edu', 'uk', 'com']

RE_NO_RUBBISH = re.compile('.*[a-z,A-Z,0-9].*')
RE_NO_NUMBER = re.compile('[a-z,A-Z]')
RE_MULT_CHAR = re.compile('\w\w+')
RE_STYLE_1 = re.compile('\w*?=".*?"')
RE_STYLE_2 = re.compile("\w*?='.*?'")
RE_STYLE_3 = re.compile("document.write(.*)")
RE_STYLE_4 = re.compile("<\w*?>.*?</\w*?>")

MODELS = "../models/"
KEEP = "../keep_multheader/"
KEEP_ENTITY = "../keep_multheader/"
DATA = "../../mhcorpus/"
EVA = "../eva/"
MULT_HEADER = True

paramsDM = {
	"ITER": [15],
	"DM": [1],
	"WINDOW_SIZE": [5, 20],
	"MINCOUNT": [5, 200],
	"DM_MEAN": [0, 1],
	"DIMENSIONS": [100, 300],
	"SAMPLE": [0, 1e-5],
	"METHOD": ["MULTI", "SINGLE"],
	"HS": [0, 1],
	"NEGATIVE": [0, 20]
}

paramsDBOW = {
	"ITER": [15],
	"DM": [2],
	"WINDOW_SIZE": [10], #should be irrelevant
	"MINCOUNT": [5, 200],
	"DM_MEAN": [0], # should be irrelevant
	"DIMENSIONS": [100, 300],
	"SAMPLE": [0, 1e-5],
	"METHOD": ["SINGLE"],
	"HS": [0, 1],
	"NEGATIVE": [0, 20]
}

# Parameters for Doc2Vec
# dm: Different Algorithms ->  Options: 1 (dm), 2 (dbow) 	
# size: Dimension of feature vector
# window: window around each word
# alpha: initial learning rate
# min_count: ignores words with lower count
# sample: downsample high frequ word -> Options: 0, 1e-5
# workers: multicore
# iter: Number of epochs -> Std: 5, Options 10, 20 ..
# hs: hierachichal sampling (1: on, 0: off)  ???
# negative: amount of drawned noise words
# dm_mean: 0: sum of contect word 1: dm_mean
# dm_concat: 0: off 1:on -> results in pretty large corpus
# dbow_words: 0: faster 1: trains words like skip_gram
# trim: zahlen, ():

# size, min_count, sample, hs, negative?
	# dm: 1 ->
		# dm_mean, dm_concat, window, multi/single
	# dm: 2 -> 
		# dbow_words: 1 -> multi/single, 0: -> nothing
