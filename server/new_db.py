#****************************************************************
"""
# write me
"""
#****************************************************************

from __future__ import print_function
from utils import utils, file_struct, create_database
import sqlite3, os, argparse, subprocess, time
from src import db_batch_entry
from subprocess import PIPE, Popen


dirname = os.path.dirname(__file__)
if dirname == '': dirname = '.'

#This will obviously be removed when we are out of the testing stage
if not os.path.isfile(file_struct.DB_path+file_struct.DBname):
  print("\nCLAS12 Off Campus Resources Database not found, creating!")
  create_database.create_database(args)
