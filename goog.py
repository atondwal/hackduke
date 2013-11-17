#!/usr/bin/python
import urllib2
from subprocess import Popen,PIPE
import re, HTMLParser, uuid, os
import requests
from unidecode import unidecode
import urllib3
import BeautifulSoup
import re
from pandocfilters import *
import json
import socket
import drunkuncle

TCP_IP='127.0.0.1'
TCP_PORT=6969
BUFFER_SIZE=1024

fin=[]
rel=0
sent=0
text_sentiment=0
aggregate_text=""


wiki_base_url = "http://en.wikipedia.org/wiki/Special:Search/"

def getgoogleurl(search,siteurl=False):
    if siteurl==False:
        return 'http://www.google.com/search?q='+urllib2.quote(search)+'&oq='+urllib2.quote(search)
    else:
        return 'http://www.google.com/search?q=site:'+urllib2.quote(siteurl)+'%20'+urllib2.quote(search)+'&oq=site:'+urllib2.quote(siteurl)+'%20'+urllib2.quote(search)

def getgooglelinks(search,siteurl=False):
    #google returns 403 without user agent
    headers = {'User-agent':'Mozilla/11.0'}
    req = urllib2.Request(getgoogleurl(search,siteurl),None,headers)
    site = urllib2.urlopen(req)
    data = site.read()
    site.close()

    #no beatifulsoup because google html is generated with javascript
    start = data.find('<div id="res">')
    end = data.find('<div id="foot">')
    if data[start:end]=='':
        #error, no links to find
        return False
    else:
        links =[]
        data = data[start:end]
        start = 0
        end = 0     
        while start>-1 and end>-1:
            #get only results of the provided site
            if siteurl==False:
                start = data.find('<a href="/url?q=')
            else: 
                start = data.find('<a href="/url?q='+str(siteurl))
            data = data[start+len('<a href="/url?q='):]
            end = data.find('&amp;sa=U&amp;ei=')
            if start>-1 and end>-1: 
                link =  urllib2.unquote(data[0:end])
                data = data[end:len(data)]
                if link.find('http')==0 and link.find('google')==-1:
                    links.append(link)
    return links

def fil(key, value, format, meta):
    if key == 'Para':
        string=stringify(Para(value))
        data = parser.getSentiment(text)
        rel = relevance(keywords, aggregate_text, string)
        fin.append( (-float(data)*text_sentiment*rel, string) )

def relevant_passage(text, parser): 
    text_sentiment= parser.getSentiment(text)
    keywords = parser.keyExtract(text)
    search = " ".join([k for k in keywords.keys()[:5]])
    keywords = keywords.keys()[:10] #Only us the top 10 keywords
    print("We will search for '%s'"%search)

    # Gets the aggregate text of the relationship search
    aggregate_text = ""
    for word in keywords:
        r = requests.get(wiki_base_url+word)
        source = r.text
        soup = BeautifulSoup.BeautifulSoup(source)
        aggregate_text += soup.p.text

    for link in getgooglelinks(search):
        print link
        #rel = relevance(keywords, aggregate_text, sentence)
        #sent = parser.getSentiment(sentence)
        # sent*text_sentiment has large magnitude if they are far apart
        #   and is positive only if they have the same sign. Thus we take the negation.
        #fin.append( (-sent*text_sentiment*rel, sentence) )
        response = urllib2.urlopen(link)
        html=response.read()
        p=Popen(['pandoc','-f','html','-t','json'],stdin=PIPE)
        tree=json.loads(p.communicate(html))
        walk(tree,fil,"",tree[0]['unMeta'])
    return sorted(fin[0][1])

def relevance(keywords, aggregate, text):
    text = re.sub("(\s+|\\\\)", " ", text, flags=re.MULTILINE | re.S) # Takes care of whitespaces.
    print(text)
    pats = [re.compile(k)  for k in text.split(' ') if k != ""]
    wc = 0
    for word in keywords:
        # see if it's in the text
        wc += len(re.findall(word, text))
    for i in pats:
        wc += 0.03 * len(i.findall(aggregate))
    return wc

if __name__ == "__main__":
        relevant_passage("Fermi Sucks",drunkuncle.DrunkUncle())
