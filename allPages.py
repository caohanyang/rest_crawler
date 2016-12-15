#!/usr/bin/env python
# coding=utf-8
from bs4 import BeautifulSoup
import urllib2
import itertools
import random
import urlparse
import sys
import list2tree

class Crawler(object):
 """docstring for Crawler"""

 def __init__(self):
    self.soup = None                               # BeautifulSoup object
    # https://www.instagram.com/developer/endpoints
    # https://dev.twitter.com/rest/reference
    # https://www.flickr.com/services/api
    # https://developers.google.com/youtube/v3/docs
    # https://developers.facebook.com/docs/graph-api/reference
    # http://docs.aws.amazon.com/AWSECommerceService/latest/DG/Welcome.html   http://docs.aws.amazon.com/AWSECommerceService/latest/DG
    # https://www.twilio.com/docs/api/rest
    # http://www.last.fm/api
    # https://go.developer.ebay.com/api-documentation   http://developer.ebay.com/devzone/rest
    # https://msdn.microsoft.com/en-us/library/ff701713.aspx  https://msdn.microsoft.com/en-us/library/ff
    # https://github.com/domainersuitedev/delicious-api https://github.com/domainersuitedev/delicious-api/blob/master/api
    # https://developer.foursquare.com/docs/
    # https://docs.docusign.com/esign/restapi
    # http://www.geonames.org/export/ws-overview.html   http://www.geonames.org/export

    if len(sys.argv) == 1:
        self.doc_page = "https://developers.google.com/youtube/v3/docs"
        self.doc_filter = "https://developers.google.com/youtube/v3/docs"
    elif len(sys.argv) == 2:
        self.doc_page = sys.argv[1]
        self.doc_filter = sys.argv[1]
    elif len(sys.argv) == 3:
        self.doc_page = sys.argv[1]
        self.doc_filter = sys.argv[2]

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

        if link.__contains__('github') :
            # Get real link:  In some cases, it redirected to a new address
            res = urllib2.urlopen(link)
            link = res.geturl()

        # if link's last part contains #, means the same page. return False
        if (link.split('/').pop().__contains__('#')):
            return False

        # Test the if link contains the doc_page
        if link.__contains__(self.doc_filter):

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
            if link is None or link.find('javascript') > -1:
                continue

            # First if the link contains the parameter '?', remove the later part
            if link.find('?') > -1:
                link = link.split('?')[0]

            # Second if the link contains the parameter '#', remove the later part
            if link.find('#') > -1:
                link = link.split('#')[0]

            # Second remove the last / from the link  /developer/endpoint/ => /develper/endpoint
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

    # convert set (unordered) to list (ordered)
    self.visited_links = list(self.visited_links)
    for i in range(0, len(self.visited_links)):
        # change unicode to a list of string
        # remove the http head
        self.visited_links[i] = str(self.visited_links[i]).split('://')[-1].split('/')
        # print "visited: " + self.visited_links[i]

    # Start to print the url address tree
    tree = list2tree.group_urls(self.visited_links)
    print tree.get_ascii(show_internal=True)

if __name__ == "__main__":
     C = Crawler()
     C.run()