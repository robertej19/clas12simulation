#****************************************************************
"""
# This file enters in users to the Users table of the database
# if the script is called, it will try to enter in the file_struct.default_user
# if that user already exists in the DB, it will query the command line for a user
# if that user also already exists, the script will display an error message and quit
# In the future, this file will query the scard for the user, and if does not already exist,
# it will enter that name into the DB, and the host OS name instead of the email
"""
#****************************************************************

from __future__ import print_function
from utils import utils, file_struct, scard_helper
import sqlite3, time, os, argparse

argparser_gch = argparse.ArgumentParser()
argparser_gch.add_argument(file_struct.debug_short,file_struct.debug_longdash,
                      default = file_struct.debug_default,help = file_struct.debug_help)
argparser_gch.add_argument('-s','--scard', default=file_struct.scard_path+file_struct.scard_name,
                      help = 'relative path and name scard you want to submit, e.g. ../scard.txt')
args_gch = argparser_gch.parse_args()
file_struct.DEBUG = getattr(args_gch,file_struct.debug_long)

#This function prompts the user to enter in information. In the future this will not run out of the command line, so this will change
def manual_data():
  username = raw_input("Enter username: ")
  email = raw_input("Enter hostname ")
  return username, email

#This function is not really necessary, I just didn't want to have this long string repeated in the code
def command_writer(user,email):
  strn = """INSERT INTO Users(User, hostname, JoinDateStamp, Total_Batches,
          Total_Jobs, Total_Events, Most_Recent_Active_Date)
          VALUES ("{0}","{1}","{2}","{3}","{4}","{5}","{6}");""".format(
          user,hostname,int(time.time()),0,0,0,"Null")
  return strn

#The code will try to submit a defualt user to the DB. If the default user already exists,
#then the prompt will come up at the command line asking for a new user
# IF the username that is returned already exists in the command line, another error will be returned and program will quit.
if __name__ == "__main__":
  try:
    conn = sqlite3.connect(file_struct.DB_path + file_struct.DBname)
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys = ON;')
    strn = command_writer(file_struct.default_user,file_struct.default_hostname)
    c.execute(strn)
    if int(file_struct.DEBUG) == 2:
      utils.printer('Executing SQL Command: {}'.format(strn)) #Turn this on for explict printing of all DB write commands
    conn.commit()
    c.close()
    conn.close()
    utils.printer("Record added to DB for User")
  except sqlite3.IntegrityError:
    try:
      c.close()
      conn.close()
      utils.printer("Default user '{0}' is already in Users table. Please enter a new, unique user".format(file_struct.default_user))
      user, hostname = manual_data()
      strn = command_writer(user,hostname)
      utils.sql3_exec(strn)
      utils.printer("Record added to DB for User")
    except sqlite3.IntegrityError:
      utils.printer("User {0} also already exists in the Users table. Please run the program again, and enter a UNIQUE user".format(user))
      utils.printer("To see users already in DB, execute 'sqlite3 {}', 'SELECT * FROM Users;'".format(file_struct.DBname))
