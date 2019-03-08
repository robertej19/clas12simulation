#from utils import utils
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

def dynamic_data_entry(user_array):
    conn = sqlite3.connect('CLAS12_OCRDB.db')
    c = conn.cursor()
    ta = user_array
    c.execute("""INSERT INTO Users(Username, Affiliation, JoinDateStamp,Permissions,
              Default_Output_Dir, Total_Batches, Total_Jobs, Total_Events,Most_Recent_Active_Date)
              VALUES (?,?,?,?,?,?,?,?,?)""",
              (ta[0],ta[1],ta[2],ta[3],ta[4],ta[5],ta[6],ta[7],ta[8]))
    conn.commit()
    print("Record added to DB for User")
    c.close()
    conn.close()

dynamic_data_entry(user_array)
