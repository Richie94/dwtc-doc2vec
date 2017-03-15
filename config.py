import re

MIN_ROW_AMOUNT = 4
MIN_COL_AMOUNT = 3
MAX_STD_DEV = 5	

ALLOWED_DOMAINS = ['org', 'us', 'gov', 'edu', 'uk', 'com']

RE_NO_RUBBISH = re.compile('.*[a-z,A-Z,0-9].*')
RE_NO_NUMBER = re.compile('[a-z,A-Z]')
RE_MULT_CHAR = re.compile('\w\w+')
KEEP = "keep/"
DATA = "dwtcData/"

METHOD = "MULTI"
WINDOW_SIZE = 8