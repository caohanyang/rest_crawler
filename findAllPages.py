#!/usr/bin/env python
from bs4 import BeautifulSoup
import urllib2

#The address of the API documendation
API_DOC = "https://www.instagram.com/developer/endpoints/"
API_MAIN= "https://www.instagram.com"

soup = BeautifulSoup(urllib2.urlopen(API_DOC).read(), "html.parser")

links = soup.find_all('a')

def handleLink(linkTag):
    # add http header if necessary
    if linkTag.find("http") == -1:
       linkTag = API_MAIN + linkTag
    # filter the links
    if linkTag.find(API_DOC) > -1:
       return linkTag
    else:
       return None


for tag in links:
   link = tag.get('href', None)
   link = handleLink(link)
   if link is not None:
      print link
