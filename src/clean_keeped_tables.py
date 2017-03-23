import glob, config

#TODO: Resturkturierung der Files nach Tabellengroesse, wenn genug Files beisammen sind

if __name__ == "__main__":
	for filename in glob.glob(config.KEEP+"*"):
		text = ""
		with open(filename, "r") as f:
			text = f.read().replace("(", " ")
			text = text.replace(")", " ") 
			text = text.replace(":", " ")
			text = text.replace(",", " ")
			text = text.replace("[", " ")
			text = text.replace("]", " ")
			text = text.replace("!", " ")
			text = text.replace("?", " ")
			text = text.replace("{", " ")
			text = text.replace("}", " ")
			text = text.replace(".", " ")
			text = text.replace("/", " ")
			text = text.replace("=", " ")
			text = text.replace("'", " ")
			text = text.replace("*", " ")

		with open(filename, "w") as f:
			f.write(text)