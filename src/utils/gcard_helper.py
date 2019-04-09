from __future__ import print_function
import sqlite3, time
import utils, file_struct
import subprocess
import urllib
import urllib2

def GCard_Entry(BatchID,unixtimestamp,url_dir):
  gcard_urls = Gather_Gcard_urls(url_dir)
  for url_ending in gcard_urls:
    response = urllib2.urlopen(url_dir+'/'+url_ending)
    gcard_text = response.read()
    gcard_text_db = gcard_text.replace('"',"'")
    db_gcard_write(BatchID,unixtimestamp,gcard_text_db)

def db_gcard_write(BatchID,timestamp,gcard_text):
    strn = "INSERT INTO Gcards(BatchID) VALUES ({0});".format(BatchID)
    utils.sql3_exec(strn)
    strn = """UPDATE Gcards SET {0} = "{1}" WHERE BatchID = {2};""".format('gcard_text',gcard_text,BatchID)
    utils.sql3_exec(strn)
    print("GCard added to database corresponding to BatchID {}".format(BatchID))


def Gather_Gcard_urls(url_dir):
  gcard_urls = []
  response = urllib2.urlopen(url_dir)
  html = response.read().split(' ')
  matching_text = ".gcard"
  second_qualifier = ">"
  """Do something like 'if href = XXX' with XXX contiaing .gcard, then download location"""
  for section in html:
    if matching_text in section:
      sections = section.split('"')
      for item in sections:
        if (matching_text in item) and (second_qualifier not in item):
          gcard_urls.append(item)
  return gcard_urls
