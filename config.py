import re

MIN_ROW_AMOUNT = 4
MIN_COL_AMOUNT = 4

RE_NO_RUBBISH = re.compile('.*[a-z,A-Z,0-9].*')
RE_NO_NUMBER = re.compile('[a-z,A-Z]')