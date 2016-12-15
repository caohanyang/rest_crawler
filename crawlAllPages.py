#!/usr/bin/env python
# coding=utf-8
from bs4 import BeautifulSoup
import urllib2
import itertools
import random
import urlparse
import sys

class Crawler(object):
 """docstring for Crawler"""

 def __init__(self):
    self.soup = None                               # BeautifulSoup object
    # https://www.instagram.com/developer/endpoints
    # https://dev.twitter.com/rest/reference
    # https://www.flickr.com/services/api
    # https://developers.google.com/youtube/v3/docs
    # https://developers.facebook.com/docs/graph-api/reference
    # http://docs.aws.amazon.com/AWSECommerceService/latest/DG ?
    # https://www.twilio.com/docs/api/rest
    # http://www.last.fm/api
    # https://go.developer.ebay.com/api-documentation ??
    # https://msdn.microsoft.com/en-us/library/ff701713.aspx  ???
    # https://github.com/domainersuitedev/delicious-api https://github.com/domainersuitedev/delicious-api/tree/master
    # https://developer.foursquare.com/docs/
    # https://docs.docusign.com/esign/restapi
    # http://www.geonames.org/export/ws-overview.html

    if len(sys.argv) == 1:
        self.doc_page = "http://www.geonames.org/export/"
    else:
        self.doc_page = sys.argv[1]
    self.current_page = self.doc_page   # Current page adress
    self.links        = set()                      # Queue with every links fetched
    self.visited_links= set()
    self.counter = 0                               # Simple counter for debug purpose
    # Tell the real doc_page url   with '/' or without '/'
    # True：https://www.flickr.com/services/api/
    # False: https://www.flickr.com/services/api
    self.withSlash = False

 def open(self):

    # Define filter
    def filter(link):
        # first time crawl all the matched links
        # if first_time:
        #     if link.__contains__(self.doc_page):
        #         return True
        #     else:
        #         return False
        # else:
            # Define crawler depth = 1, means we don't crawl inside links from the second time
            # if link.__contains__(self.doc_page) and len(link.split('/')) == len(self.doc_page.split('/')) + 1:

        # if link's last part contains #, means the same page. return False
        if (link.split('/').pop().__contains__('#')):
            return False
        # Test the if link contains the current_page and doc_page
        if link.__contains__(self.doc_page) and link.__contains__(self.current_page):
            return True
        else:
            return False
    # Open url
    print self.counter, ":", self.current_page
    try:
        res = urllib2.urlopen(self.current_page)
        print "Real: " + res.geturl()

        html_code = res.read()
    except Exception, ex:
        print ex
        # Remove url in the self.links
        self.links.remove(self.current_page)
        # Give a new self.current_page
        if len(self.links.difference(self.visited_links)) > 0:
            # Choose a random url from non-visited set
            self.current_page = random.sample(self.links.difference(self.visited_links), 1)[0]
        return

    # add in the list the origin url
    self.visited_links.add(self.current_page)

    # change to the redirect url
    self.current_page = res.geturl()  # This is the real url   with '/' or without '/'
    if self.current_page.split('/').pop() is None:
        self.withSlash = True
    else:
        self.withSlash = False

    # Fetch every links
    self.soup = BeautifulSoup(html_code, "html.parser")
    page_links = []
    try:
        for link in [h.get('href') for h in self.soup.find_all('a')]:
            if link is None:
                continue
            print "Found link: " + link
            # First remove the last / from the link  /developer/endpoint/ => /develper/endpoint
            link = link.split("/")
            if link[-1] == "":
                link.pop()
            link = '/'.join(link)
            # Start to handle link
            if link.startswith('http'):
                if filter(link):
                    page_links.append(link)
                    print "Adding link " + link + "\n"
            elif link.startswith('/'):
                parts = urlparse.urlparse(self.current_page)
                tmp_link = parts.scheme + '://' + parts.netloc + link
                if filter(tmp_link):
                    page_links.append(tmp_link)
                    print "Adding link " + tmp_link
            elif link.startswith('..'):
                # If starts with '../', indicates that the link in the previous catalog, which has been add before
                continue
            elif link.startswith('#') or len(link) == 0 or link.startswith('\\'):
                continue
            else:
                # Start without /   ex: public
                print "???  " + link
                print self.current_page

                firstParts = self.current_page.split('/')

                # if end without '/', Remove last element  api/rest/application  => api/rest
                if not self.withSlash:
                    firstParts.pop()

                firstParts = "/".join(firstParts)
                tmp_link = firstParts+'/'+link
                print "Tmp link " + tmp_link
                if filter(tmp_link):
                    page_links.append(tmp_link)
                    print "Adding link " + tmp_link

    except Exception, ex:
         print ex


    # Update links

    self.links = self.links.union(set(page_links))
    # Continue if not visit some links

    if len(self.links.difference(self.visited_links)) > 0:
        # Choose a random url from non-visited set
        self.current_page = random.sample(self.links.difference(self.visited_links), 1)[0]
        self.counter+=1

 def run(self):

    # Run it first time
    # first_time = True
    self.open()
    # first_time = False
    # Crawl 3 webpages (or stop if all url has been fetched)
    while len(self.links.difference(self.visited_links)) != 0:
        self.open()

    print len(self.links)
    for link in self.links:
        print link

    print len(self.visited_links)
    for link1 in self.visited_links:
        print "visited: " + link1

if __name__ == "__main__":
     C = Crawler()
     C.run()