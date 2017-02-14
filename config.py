import re

MIN_ROW_AMOUNT = 2
MIN_COL_AMOUNT = 2
MAX_STD_DEV = 9

RE_NO_RUBBISH = re.compile('.*[a-z,A-Z,0-9].*')
RE_NO_NUMBER = re.compile('[a-z,A-Z]')