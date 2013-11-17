#!/usr/bin/python
import urllib2
from subprocess import Popen,PIPE
import re, HTMLParser, uuid

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

def relevant_passage(text, keywords): 
    search = " ".join([k for k in keywords[:5]])
    keywords = keywords[:10] #Only us the top 10 keywords
    print("We will search for '%s'"%search)
    for link in getgooglelinks(search):
        print link
        connection = urllib2.urlopen(link)
        encoding = connection.headers.getparam('charset')
        html = connection.read().decode(encoding)
        # Replace html tags and leave only the text in.
        #html = re.sub("<script.+?script>", " ", html, flags = re.MULTILINE | re.S)
        #html = re.sub("<style.+?style>", " ", html, flags = re.MULTILINE | re.S)
        #html = re.sub("\s+", " ", re.sub("<.+?>"," ", html, flags = re.MULTILINE | re.S), flags=re.MULTILINE | re.S)
        #html = HTMLParser.HTMLParser().unescape(html)

        # Replaces all links
        html = re.sub("</?a(|.+?)>", " ", html)
        filename = uuid.uuid1().hex
        p=Popen(['pandoc','-o',filename],stdin=PIPE)
        p.communicate(html)
        FILE = open(filename, 'r')
        for sentence in FILE.readlines():
            # relevance(keywords, sentence)
            pass
