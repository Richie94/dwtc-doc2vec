import gzip
import ujson as json

class TableReader:
	def __init__(self, filename):
		self.file = gzip.open(filename, 'r')
		self.line_count = 0

	def close(self):
		self.file.close()

	def get_next_table(self):
		self.line_count += 1
		line = self.file.readline()
		if line:
			return json.loads(line)
		else:
			return None

	def get_line_count(self):
		return self.line_count