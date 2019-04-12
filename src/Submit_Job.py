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
from utils import utils, file_struct
import sqlite3, os, argparse, subprocess

#This allows a user to specifiy which batch to use to generate files using a specific BatchID
argparser = argparse.ArgumentParser()
argparser.add_argument('-s','--scard', default=file_struct.scard_path+file_struct.scard_name,
                      help = 'relative path and name scard you want to submit, e.g. ../scard.txt')
argparser.add_argument(file_struct.debug_short,file_struct.debug_longdash,
                      default = file_struct.debug_default,help = file_struct.debug_help)
args = argparser.parse_args()

dirname = os.path.dirname(__file__)
if dirname == '': dirname = '.'

if not os.path.isfile(file_struct.DB_path+file_struct.DBname):
  print("CLAS12 Off Campus Resources Database not found, creating!")
  subprocess.call(['python2',dirname+'/utils/create_database.py','-d',str(args.debug)])
  print("Creating example user [needed for testing purposes]")
  subprocess.call(['python2',dirname+'/db_user_entry.py','-d',str(args.debug)])


subprocess.call(['python2',dirname+'/db_batch_entry.py','-d',str(args.debug),'-s',str(args.scard)])

print("\n Generating submission files from database")
subprocess.call(['python2',dirname+'/sub_script_generator.py','-d',str(args.debug)])
