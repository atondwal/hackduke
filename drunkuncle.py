from topia.termextract import tag, extract

class DrunkUncle:
	def __init__(self):
		self.key_tagger = tag.Tagger()
		self.key_tagger.initialize()
		self.key_extract = extract.TermExtractor(self.key_tagger)
		self.key_extract.filter = extract.permissiveFilter

	def keyExtract(self, text):
		text = str(text)
		keywords = {}
		try:
			term = sorted(self.key_extract(text), key=lambda strength: strength[2])
			for i in term:
				keywords[i[0]] = i[1]
		except:
			print "Things broke"
		return keywords
	