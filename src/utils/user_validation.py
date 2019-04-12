#****************************************************************
"""
#This file inteacts with db_batch_entry and scard_helper to see from the scard
#if the user exists in the database. If not, the user gets added to the Database
#and the OS host is also added
"""
#****************************************************************
from __future__ import print_function
import sqlite3, time
import utils, file_struct, argparse, subprocess, socket

def user_validation():
  user = subprocess.check_output('whoami')
  host = socket.gethostname()
  strn = "SELECT 1 FROM Users WHERE EXISTS (SELECT 1 FROM Users WHERE User ='{0}' AND hostname = '{1}')".format(user,host)
  user_exists = utils.sql3_grab(strn)
  if not user_exists:
    print('\nThis is the first time {0}@{1} has submitted jobs. Adding user to database'.format(user,host))
    strn = """INSERT INTO Users(User, hostname, JoinDateStamp, Total_Batches,
              Total_Jobs, Total_Events, Most_Recent_Active_Date)
              VALUES ("{0}","{1}","{2}","{3}","{4}","{5}","{6}");""".format(
              user,host,utils.timeconvert(time.time()),0,0,0,"Null")
    utils.sql3_exec(strn)
