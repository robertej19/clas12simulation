from __future__ import print_function
from utils import utils, file_struct, scard_helper
import sqlite3, time, os

dirname = os.path.dirname(__file__)
if dirname == '': dirname = '.' #Need this because if running in this file's directory, dirname is blank
db_path = dirname+file_struct.DB_rel_location_src+file_struct.DBname

def manual_data():
  username = raw_input("Enter JLab username: ")
  email = raw_input("Enter email address: ")
  return username, email

def command_writer(array):
  strn = """INSERT INTO Users(User, Email, JoinDateStamp, Total_Batches,
          Total_Jobs, Total_Events, Most_Recent_Active_Date)
          VALUES ("{0}","{1}","{2}","{3}","{4}","{5}","{6}");""".format(
          array[0],array[1],join_datestamp,0,0,0,"Null")
  return strn

default_user = 'mungaro'
default_email = 'mungaro@example.com'
join_datestamp = int(time.time())
user_array = (default_user,default_email)

conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute('PRAGMA foreign_keys = ON;')

try:
    strn = command_writer(user_array)
    c.execute(strn)
    conn.commit()
    c.close()
    conn.close()
    print("Record added to DB for User")
except sqlite3.IntegrityError:
    c.close()
    conn.close()
    print("Default user '{0}' is already in Users table. Please enter a new, unique user".format(default_user))
    user, email = manual_data()
    man_user_array = (user,email)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys = ON;')
    strn = command_writer(man_user_array)
    c.execute(strn)
    conn.commit()
    c.close()
    conn.close()
    print("Record added to DB for User")
