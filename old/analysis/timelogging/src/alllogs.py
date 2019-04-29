from log_write import *
from os import listdir
from os.path import isfile, join
import os


def jobstowrite():
  mypath = os.path.dirname(os.path.realpath(__file__))+'/../../log'
  files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
  outfiles = [ x for x in files if "out" in x]
  return outfiles

jobby = "job.7299012.12.out"

def find_nevents(job):
  lineno = 0
  for line in reversed(open('../../log/'+job).readlines()):
    if '>>>>> progress :' in line:
      events_raw = line.split()[4] #located in fifth word of string
      nevents = int(events_raw[:-1])+1 #OBO error
      break
    else:
      lineno +=1
      if lineno > 50:
        print 'Could not find nevents'
        break
  return nevents

for job in jobstowrite():
  if os.stat('../../log/'+job).st_size == 0:
    print job + " is empty. Skipping. \n"
  else:
    nevents = find_nevents(job)
    write_record(job,nevents)
