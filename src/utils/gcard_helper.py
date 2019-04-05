from __future__ import print_function
import sqlite3, time
import utils, file_struct
import subprocess
import urllib
import urllib2
#>>> resp = urllib2.urlopen("http://google.com/abc.jpg")

def GCard_Entry(DBname,UID,BatchID,unixtimestamp,url_dir):
  #gcard_urls = Gather_Gcard_urls(url_dir)
  gcard_urls = ["444","555"]
  for url_ending in gcard_urls:
    #response = urllib2.urlopen(url_dir+'/'+url_ending)
    #gcard_text = response.read()
    gcard_text = url_ending
    db_gcard_write(DBname,UID,BatchID,unixtimestamp,gcard_text)

def db_gcard_write(DBname,UID,BatchID,timestamp,gcard_text):
    strn = "INSERT INTO Gcards(UserID,timestamp) VALUES ('{0}',{1});".format(UID,timestamp)
    utils.sql3_exec(DBname,strn)
    strn = "UPDATE Gcards SET {0} = '{1}' WHERE timestamp = {2};".format('Gcards',gcard_text,timestamp)
    utils.sql3_exec(DBname,strn)
    print("GCard record added to database corresponding to BatchID {}".format(BatchID))
    strn = "UPDATE Gcards SET {0} = '{1}' WHERE timestamp = {2};".format("BatchID",BatchID,timestamp)
    utils.sql3_exec(DBname,strn)

def Gather_Gcard_urls(url_dir):
  gcard_urls = []
  response = urllib2.urlopen(url_dir)
  html = response.read().split(' ')
  matching_text = ".gcard"
  second_qualifier = ">"
  for section in html:
    if matching_text in section:
      sections = section.split('"')
      for item in sections:
        if (matching_text in item) and (second_qualifier not in item):
          gcard_urls.append(item)
  return gcard_urls
