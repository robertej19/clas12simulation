#****************************************************************
"""
#This replaces a previous version of gcard_helper.py by using the HTMLParser class
#This allows for more robust parsing of the html mother directory to find gcard files
#Even better would be to use BeautifulSoup, which would allow for the code to be condensed as:
#```import requests
#from bs4 import BeautifulSoup
#page = requests.get('http://www.website.com')
#bs = BeautifulSoup(page.content, features='lxml')
#for link in bs.findAll('a'):
#    print(link.get('href'))```
#Unfortunately, this module must be imported and cannot be gaurannted that it will be on whatever
#server this software will live on, so it is safer to instead use HTMLParser which is more common
####
#This file takes in a BatchID, unixtimestamp, and gcard url from db_batch_entry and passes it through
#a few functions to download the gcards from the specified location and to enter them into the
#appropriate gcard table in the database.
# Some effort should be developed to sanitize the gcard files to prevent
# against sql injection attacks
"""
#***************************************************************
from __future__ import print_function
import utils, file_struct
from HTMLParser import HTMLParser
import urllib2, argparse

argparser_gch = argparse.ArgumentParser()
argparser_gch.add_argument(file_struct.debug_short,file_struct.debug_longdash,
                      default = file_struct.debug_default,help = file_struct.debug_help)
argparser_gch.add_argument('-s','--scard', default=file_struct.scard_path+file_struct.scard_name,
                      help = 'relative path and name scard you want to submit, e.g. ../scard.txt')
args_gch = argparser_gch.parse_args()
file_struct.DEBUG = getattr(args_gch,file_struct.debug_long)


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

def Gather_Gcard_urls(url_dir):
  response = urllib2.urlopen(url_dir)
  html = response.read()
  parser = MyHTMLParser()
  parser.feed(html)

def db_gcard_write(BatchID,timestamp,gcard_text):
    strn = "INSERT INTO Gcards(BatchID) VALUES ({0});".format(BatchID)
    utils.sql3_exec(strn)
    strn = """UPDATE Gcards SET {0} = "{1}" WHERE BatchID = {2};""".format('gcard_text',gcard_text,BatchID)
    utils.sql3_exec(strn)
    utils.printer("GCard added to database corresponding to BatchID {}".format(BatchID))

def GCard_Entry(BatchID,unixtimestamp,url_dir):
  print("Gathering gcards from {} ".format(url_dir))
  Gather_Gcard_urls(url_dir)
  for url_ending in gcard_urls:
    utils.printer('Gcard URL name is: '+url_ending)
    response = urllib2.urlopen(url_dir+'/'+url_ending)
    gcard_text = response.read()
    utils.printer2('HTML from gcard link is: {}'.format(gcard_text))
    gcard_text_db = gcard_text.replace('"',"'")
    print("\t Gathered gcard '{}'".format(url_ending))
    db_gcard_write(BatchID,unixtimestamp,gcard_text_db)
