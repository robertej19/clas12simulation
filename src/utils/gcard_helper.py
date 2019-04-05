from __future__ import print_function
import sqlite3, time
import utils, file_struct
import subprocess
import urllib
import urllib2
#>>> resp = urllib2.urlopen("http://google.com/abc.jpg")

def GCard_Entry(DBname,UID,BatchID,unixtimestamp,url_dir):
  response = urllib2.urlopen(url_dir)
  html = response.read()
  a = ".gcard"
  bb = ">"
  q = html.split(' ')
  for item in q:
    if a in item:
      b = item.split('"')
      for item in b:
        if (a in item) and (bb not in item):
          print(item)
