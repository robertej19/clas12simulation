from __future__ import print_function
from utils import utils, file_struct, scard_helper
import sqlite3, time


username = 'mungaro'
email = 'mungaro@example.com'
join_datestamp = int(time.time())
batches = 0
jobs = 0
events = 0
last_active = int(time.time())
user_array = (username,email,join_datestamp,batches,jobs,events,last_active)

def dynamic_data_entry(DBname,user_array):
    ta = user_array
    strn = """INSERT INTO Users(User, Email, JoinDateStamp, Total_Batches,
                  Total_Jobs, Total_Events, Most_Recent_Active_Date)
                  VALUES ("{0}","{1}","{2}","{3}","{4}",
                   "{5}","{6}");""".format(ta[0],ta[1],ta[2],ta[3]
                   ,ta[4],ta[5],ta[6])
    utils.sql3_exec(DBname,strn)
    print("Record added to DB for User")

dynamic_data_entry(file_struct.DBname,user_array)
