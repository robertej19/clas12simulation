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
import submission_script_maker, htcondor_submit
from subprocess import PIPE, Popen

#This allows a user to specifiy which batch to use to generate files using a specific BatchID
argparser = argparse.ArgumentParser()
argparser.add_argument(file_struct.debug_short,file_struct.debug_longdash,
                      default = file_struct.debug_default,help = file_struct.debug_help)
argparser.add_argument('-b','--BatchID', default='none', help = 'Enter the ID# of the batch you want to submit (e.g. -b 23)')
argparser.add_argument('-s','--submit', help = 'Use this flag (no arguements) if you want to submit the job', action = 'store_true')
args = argparser.parse_args()

dirname = os.path.dirname(__file__)
if dirname == '': dirname = '.'

print("\nGenerating submission files from database")
submission_script_maker.submission_script_maker(args)
