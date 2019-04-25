#****************************************************************
"""
# write me
"""
#****************************************************************

from __future__ import print_function
from utils import utils, file_struct, create_database
import sqlite3, os, argparse, subprocess, time
from subprocess import PIPE, Popen

#This allows a user to specifiy which batch to use to generate files using a specific BatchID
argparser = argparse.ArgumentParser()
argparser.add_argument(file_struct.debug_short,file_struct.debug_longdash,
                      default = file_struct.debug_default,help = file_struct.debug_help)
argparser.add_argument('-b','--BatchID', default='none', help = 'Enter the ID# of the batch you want to submit (e.g. -b 23)')
argparser.add_argument('-s','--submit', help = 'Use this flag (no arguements) if you want to submit the job', action = 'store_true')
argparser.add_argument('scard',default=file_struct.scard_path+file_struct.scard_name,nargs='?',
                        help = 'relative path and name scard you want to submit, e.g. ../scard.txt')
args = argparser.parse_args()

dirname = os.path.dirname(__file__)
if dirname == '': dirname = '.'

#This will obviously be removed when we are out of the testing stage
if not os.path.isfile(file_struct.DB_path+file_struct.DBname):
  print("\nCLAS12 Off Campus Resources Database not found, creating!")
  create_database.create_database(args)
