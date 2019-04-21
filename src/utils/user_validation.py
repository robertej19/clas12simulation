#****************************************************************
"""
#This file inteacts with db_batch_entry and scard_helper to see from the scard
#if the user exists in the database. If not, the user gets added to the Database
#and the OS host is also added
"""
#****************************************************************
from __future__ import print_function
import sqlite3, time
import utils, file_struct, argparse, socket, subprocess
import datetime


def user_validation():
  username = (subprocess.check_output('whoami'))[:-1]#The [:-1] is so we drop the implicit \n from the string
  hostname = subprocess.check_output(['hostname','-d'])#socket.getfqdn()  #socket.gethostname()
  print('hostname is {}'.format(hostname))
  strn = """SELECT 1 FROM Users WHERE EXISTS (SELECT 1 FROM Users WHERE User ='{0}'
          AND hostname = '{1}')""".format(username,hostname)
  user_already_exists = utils.sql3_grab(strn)
  if not user_already_exists:
    print("""\nThis is the first time {0} from {1} has submitted jobs. Adding user to database""".format(username,hostname))
    strn = """INSERT INTO Users(User, hostname, JoinDateStamp, Total_Batches,
              Total_Jobs, Total_Events, Most_Recent_Active_Date)
              VALUES ("{0}","{1}","{2}","{3}","{4}","{5}","{6}");""".format(
              username,hostname,utils.gettime(),0,0,0,"Null")
    utils.sql3_exec(strn)

  return username
