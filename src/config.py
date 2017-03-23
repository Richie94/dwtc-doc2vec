import re

MIN_ROW_AMOUNT = 4
MIN_COL_AMOUNT = 3
MAX_STD_DEV = 5	

ALLOWED_DOMAINS = ['org', 'us', 'gov', 'edu', 'uk', 'com']

RE_NO_RUBBISH = re.compile('.*[a-z,A-Z,0-9].*')
RE_NO_NUMBER = re.compile('[a-z,A-Z]')
RE_MULT_CHAR = re.compile('\w\w+')

MODELS = "..\\models\\"
KEEP = "..\\keep\\"
DATA = "..\\dwtcData\\"
EVA = "..\\eva\\"

METHOD = "MULTI"
WINDOW_SIZE = 10
DIMENSIONS = 300
DM = 2 # tried once 2, was totally bad
HS = 1 # vs 0
ITER = 15
DM_MEAN = 0 # vs 1
DBOW_WORDS = 0 # vs 1
MINCOUNT = 5

# Parameters for Doc2Vec
# dm: Different Algorithms ->  Options: 1, 2 	
# size: Dimension of feature vector
# window: window around each word
# alpha: initial learning rate
# min_count: ignores words with lower count
# sample: downsample high frequ word -> Options: 0, 1e-5
# workers: multicore
# iter: Number of epochs -> Std: 5, Pptions 10, 20 ..
# hs: hierachichal sampling (1: on, 0: off)  ???
# negative: amount of drawned noise words
# dm_mean: 0: sum of contect word 1: dm_mean
# dm_concat: 0: off 1:on -> results in pretty large corpus
# dbow_words: 0: faster 1: dbow training ???
# trim: zahlen, ():
