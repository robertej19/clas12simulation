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


"""
argparser_gch = argparse.ArgumentParser()
argparser_gch.add_argument(file_struct.debug_short,file_struct.debug_longdash,
                      default = file_struct.debug_default,help = file_struct.debug_help)
argparser_gch.add_argument('-s','--scard', default=file_struct.scard_path+file_struct.scard_name,
                      help = 'relative path and name scard you want to submit, e.g. ../scard.txt')
args_gch = argparser_gch.parse_args()
file_struct.DEBUG = getattr(args_gch,file_struct.debug_long)
"""
def user_validation():
  username = (subprocess.check_output('whoami'))
  strn = "SELECT 1 FROM Users WHERE EXISTS (SELECT 1 FROM Users WHERE User ='{0}')".format(username)
  user_exists = utils.sql3_grab(strn)
  if not user_exists:
    print('\nThis is the first time {0} has submitted jobs. Adding user to database'.format(str(username)))
    strn = """INSERT INTO Users(User, hostname, JoinDateStamp, Total_Batches,
              Total_Jobs, Total_Events, Most_Recent_Active_Date)
              VALUES ("{0}","{1}","{2}","{3}","{4}","{5}","{6}");""".format(
              username,socket.gethostname(),int(time.time()),0,0,0,"Null")
    utils.sql3_exec(strn)

  return username
