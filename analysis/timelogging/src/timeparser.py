#Note: This workin is EXTREMELY contingent on having a certain structure in the log output files
#IF the structur of the output files are changed, this script must be changed accordingly.
#This needs to be fixed for code maintaince purposes. Perhaps write directly to logging database instead of parsing log files
# This is written in python2
# This also assumes that run times do NOT cross over 2 days, which might not be a problem as job would then have to run for more than 24 hours
import os

def swapper(ar):
  ar[0],ar[1],ar[2],ar[3],ar[4],ar[5] = ar[4],ar[3],ar[2],ar[1],ar[0],ar[5]
  return ar

def timeconvert(timearray): #assumes timestamp entries of form 'HH:MM:SS'
  i = 0
  for item in timearray:
    tb = item.split(':')
    daytime = int(tb[0])*3600+int(tb[1])*60+int(tb[2])
    timearray[i] = daytime
    i +=1
  return timearray

def job_out_reader(filename):
  process = []
  timestamp = []
  lineno = 0
  for line in reversed(open('../../log/'+filename).readlines()): # This is inefficent as it has to read in the whole file. Change this to a better method if needed. For now, it works.
    words = line.split()
    process.append(words[0])
    timestamp.append(words[6])
    lineno +=1
    if lineno > 5:
        break
  swapper(process)
  swapper(timestamp)
  return process, timestamp

def runtimes(ta):
  runtime = []
  for i in range(0,len(ta)-1):
    if ta[i+1] - ta[i] < 0:
      ta[i+1] = ta[i+1]+24*3600 #This handles cases where the job runs over 1 day. Does NOT handle cases where job spans 2 days
    runtime.append(ta[i+1] - ta[i])
  runtime.append(sum(runtime))
  return runtime

def parse_times(filename):
  p, t = job_out_reader(filename) #p here is actually not useful
  useable_times = timeconvert(t)
  return runtimes(useable_times)
