#****************************************************************
"""
# This is a sript which executes all scripts needed to generate
submission files from an scard. It just invokes submission_script_maker, and
passes arguements to it. 
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
