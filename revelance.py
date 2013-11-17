import requests
import urllib3
from bs4 import BeautifulSoup

base_url = "http://en.wikipedia.org/wiki/Special:Search/"

def wiki_count(word, url):
	wc = 0
	r = requests.get(url)
	source = r.text
	soup = BeautifulSoup(data)
	# follow every link that contains our word
	for link in soup.find_all('a'):
		if link.find(word) != -1:
			wc += wiki_count(word, link.get('href'))	
	# scour the page, aaarrrrgg
	text = soup.p.text
	index = text.find(index)
	while index != -1:
		wc++
		index = text.find(word, index+1)
	return wc

def revelance(keywords, text):
	for word in keywords:
		# see if it's in the text
		wc = 0
		index = text.find(word)
		while index != -1 && index+1 < len(text)
			wc++
			index = text.find(word, index+1)
		# check wikipedia	
		wc += wiki_count(word, base_url + word)
	return wc
