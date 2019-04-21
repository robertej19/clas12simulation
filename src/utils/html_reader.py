#****************************************************************
"""
#This description needs to be written
"""
#***************************************************************
from __future__ import print_function
import utils, file_struct
from HTMLParser import HTMLParser
import urllib2, argparse

def html_reader(url_dir):
  # create a subclass and override the handler methods
  # from https://docs.python.org/2/library/htmlparser.html
  gcard_urls = []
  class MyHTMLParser(HTMLParser):
      def handle_starttag(self, tag, attrs):
          utils.printer2("Encountered a start tag: {}".format(tag))
      def handle_endtag(self, tag):
          utils.printer2("Encountered an end tag: {}".format(tag))
      def handle_data(self, data):
          utils.printer2("Encountered some data  : {}".format(data))
          if file_struct.gcard_identifying_text in data:
            gcard_urls.append(data)

  response = urllib2.urlopen(url_dir)
  html = response.read()
  parser = MyHTMLParser()
  parser.feed(html)

  return gcard_urls
