from __future__ import print_function
from utils import utils, file_struct
import sqlite3, os, argparse, subprocess

#This allows a user to specifiy which batch to use to generate files using a specific BatchID
argparser = argparse.ArgumentParser()
argparser.add_argument('-s','--scard', default='scard.txt', help = 'name of the scard you want to submit')
argparser.add_argument(file_struct.debug_short,file_struct.debug_longdash,
                      default = file_struct.debug_default,help = file_struct.debug_help)
args = argparser.parse_args()

if not os.path.isfile(file_struct.DB_path+file_struct.DBname):
  print("CLAS12 Off Campus Resources Database not found, creating!")
  subprocess.call(['python2','src/utils/create_database.py','-d',str(args.debug)])
  print("Creating example user [needed for testing purposes]")
  subprocess.call(['python2','src/db_user_entry.py','-d',str(args.debug)])

print("Reading scard & other information into database")
subprocess.call(['python2','src/db_batch_entry.py','-d',str(args.debug)])

print("Writing submission scripts")
subprocess.call(['python2','src/sub_script_generator.py','-d',str(args.debug)])
