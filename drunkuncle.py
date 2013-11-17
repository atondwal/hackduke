from topia.termextract import tag, extract

import re, math, collections, itertools, os

import nltk, nltk.classify.util, nltk.metrics
from nltk.classify import NaiveBayesClassifier
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist

class DrunkUncle:
	def __init__(self):
		self.key_tagger = tag.Tagger()
		self.key_tagger.initialize()
		self.key_extract = extract.TermExtractor(self.key_tagger)
		self.key_extract.filter = extract.permissiveFilter
		trainers = self.movieTrain()
		trainers += self.afinnTrain()
		trainers += self.congressTrain()
		#print trainers
		self.classifier = NaiveBayesClassifier.train(trainers)

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

	def movieTrain(self):
		trainData = []
		with open("pos.txt", "r") as pos:
			for word in pos:
				posWords = re.findall(r"[\w']+|[.,!?;]", word.rstrip())
				posFeatures = [dict([(word, True) for word in posWords]), '+']
				trainData.append(posFeatures)

		with open("neg.txt", "r") as neg:
			for word in neg:
				negWords = re.findall(r"[\w']+|[.,!?;]", word.rstrip())
				negFeatures = [dict([(word, True) for word in negWords]), '-']
				trainData.append(negFeatures)

		return trainData

	def afinnTrain(self):
		wordSet = collections.defaultdict(set)
		trainData = []
		with open("AFINN/AFINN-111.txt", "r") as afinn:
			for line in afinn:
				m = re.match(r"(?P<word>[a-zA-Z-0-9]+)\t(?P<score>[-]?[0-9]+)", line.rstrip())
				if m is not None:
					wordSet[m.group("word")] = int(m.group("score"))
					for i in range(abs(int(m.group("score")))):
						trainData.append([dict([(m.group("word"), True)]), '+' if m.group("score") > 0 else '-'])

		return trainData

	def congressTrain(self):
		trainingData = []
		for dataFile in os.listdir("convote_v1.1/data_stage_three/training_set"):
			with open('convote_v1.1/data_stage_three/training_set/' + dataFile, "r") as speech:
				opinion = '+' if os.path.splitext(dataFile)[0][-1].lower() == 'y' else '-'
				for word in speech:
					words = re.findall(r"[\w']+|[.,!?;]", word.rstrip())
					speechFeatures = [dict([(word, True) for word in words]), opinion]
					trainingData.append(speechFeatures)

		return trainingData

	def getSentiment(self, text):
                #text = str(text)
		textKeys = text.split(" ")
		words = dict(map(lambda word: (word, True), textKeys))
		result = self.classifier.prob_classify(words)
		return result.max() + str(result.prob(result.max()))

