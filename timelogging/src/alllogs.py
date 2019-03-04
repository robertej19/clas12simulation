from log_write import *
from os import listdir
from os.path import isfile, join
import os


def jobstowrite():
  mypath = os.path.dirname(os.path.realpath(__file__))+'/../../log'
  files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
  outfiles = [ x for x in files if "out" in x]
  return outfiles

for job in jobstowrite():
  if os.stat('../../log/'+job).st_size == 0:
    print job + " is empty. Skipping. \n"
  else:
    write_record(job)
