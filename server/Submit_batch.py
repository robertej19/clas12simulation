#****************************************************************
"""
# This is an umbrella script which executes all scripts needed to generate
submission files from an scard. It will create a DB and user if they do not yet
exist. It then executes db_batch_entry.py and sub_script_generator.py to read the
scard, download the gcards, and write the submission scripts. This script will change
slightly when the db_user_entry script is redesigned to automatically create a user
based off the value found in the scard
"""
#****************************************************************

from __future__ import print_function
from utils import utils, file_struct, create_database
import sqlite3, os, argparse, subprocess, time
from src import db_batch_entry
from subprocess import PIPE, Popen

#This allows a user to specifiy which batch to use to generate files using a specific BatchID
argparser = argparse.ArgumentParser()
argparser.add_argument(file_struct.debug_short,file_struct.debug_longdash,
                      default = file_struct.debug_default,help = file_struct.debug_help)
argparser.add_argument('-b','--BatchID', default='none', help = 'Enter the ID# of the batch you want to submit (e.g. -b 23)')
argparser.add_argument('-r','--run', help = 'Use this flag (no arguements) if you want to submit the job', action = 'store_true')
argparser.add_argument('scard',default=file_struct.scard_path+file_struct.scard_name,nargs='?',
                        help = 'relative path and name scard you want to submit, e.g. ../scard.txt')
args = argparser.parse_args()

dirname = os.path.dirname(__file__)
if dirname == '': dirname = '.'

#This will obviously be removed when we are out of the testing stage
if not os.path.isfile(file_struct.DB_path+file_struct.DBname):
  print("\nCLAS12 Off Campus Resources Database not found, creating!")
  create_database.create_database(args)

if args.BatchID == 'none':
  db_batch_entry.Batch_Entry(args.scard)

print("\nGenerating submission files from database")
GcardID = new_script_generator.submission_script_maker(args)

if args.run:
  """ if value in submission === not submitted"""

  """This entire section should be written into a dedicated function / script"""
  subprocess.call(['chmod','+x','runscript.sh'])
  submission = Popen(['condor_submit','clas12.condor'], stdout=PIPE).communicate()[0]
  #The below is for testing purposes
  #submission = """Submitting job(s)...
#3 job(s) submitted to cluster 7334290."""
  print(submission)
  words = submission.split()
  node_number = words[len(words)-1] #This might only work on SubMIT
  print(node_number)

  strn = "UPDATE Submissions SET run_status = 'submitted to pool' WHERE GcardID = '{0}';".format(GcardID)
  utils.sql3_exec(strn)

  timestamp = utils.gettime() # Can modify this if need 10ths of seconds or more resolution
  strn = "UPDATE Submissions SET submission_timestamp = '{0}' WHERE GcardID = '{1}';".format(timestamp,GcardID)
  utils.sql3_exec(strn)

  strn = "UPDATE Submissions SET pool_node = '{0}' WHERE GcardID = '{1}';".format(node_number,GcardID)
  utils.sql3_exec(strn)
