from __future__ import print_function
from utils import utils, file_struct, scard_helper
import sqlite3

username = 'robertej'
affiliation = 'MIT'
date = 'TODAY'
perms = 'moderator'
dir = '/home/robertej'
batches = 0
jobs = 0
events = 0
last_active = 'TODAY'
user_array = (username,affiliation,date,perms,dir,batches,jobs,events,last_active)

def dynamic_data_entry(DBname,user_array):
    ta = user_array
    strn = """INSERT INTO Users(Username, Affiliation, JoinDateStamp,Permissions,
                   Default_Output_Dir, Total_Batches, Total_Jobs, Total_Events,
                   Most_Recent_Active_Date) VALUES ("{0}","{1}","{2}","{3}","{4}",
                   "{5}","{6}","{7}","{8}");""".format(ta[0],ta[1],ta[2],ta[3]
                   ,ta[4],ta[5],ta[6],ta[7],ta[8])
    utils.sql3_exec(DBname,strn)
    print("Record added to DB for User")

dynamic_data_entry(file_struct.DBname,user_array)
