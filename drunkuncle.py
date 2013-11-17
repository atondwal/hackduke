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
		#self. classifier = self.train()
		self.classifier = self.afinnTrain()

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

	def train(self):
		trainData = []
		with open("pos.txt", "r") as pos:
			for word in pos:
				posWords = re.findall(r"[\w']+|[.,!?;]", word.rstrip())
				posFeatures = [dict([(word, True) for word in posWords]), 'pos']
				trainData.append(posFeatures)

		with open("neg.txt", "r") as neg:
			for word in neg:
				negWords = re.findall(r"[\w']+|[.,!?;]", word.rstrip())
				negFeatures = [dict([(word, True) for word in negWords]), 'neg']
				trainData.append(negFeatures)

		return NaiveBayesClassifier.train(trainData)

	def afinnTrain(self):
		wordSet = collections.defaultdict(set)
		with open("AFINN/AFINN-111.txt", "r") as afinn:
			for line in afinn:
				m = re.match(r"(?P<word>[a-zA-Z]+)\t(?P<score>[-]?[0-9]+)", line.rstrip())
				if m is not None:
					wordSet[m.group("word")] = int(m.group("score"))
		return wordSet

	def getSentiment(self, text):
		text = str(text)
		textKeys = text.split(" ")
		#words = dict(map(lambda word: (word, True), textKeys))
		score = 0
		for word in textKeys:
			if word in self.classifier:
				score += self.classifier[word]
		return score