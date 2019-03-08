import sqlite3, utils, file_struct

"""***************************************************************************"""


tables = ['Users','Scards','JobsLog']
table_fields = [file_struct.users_fields,file_struct.scard_fields,file_struct.jobslog_fields]

"""***************************************************************************"""
"""***************************************************************************"""
""" Function definitions"""

def create_tables():
    conn = sqlite3.connect('CLAS12_OCRDB.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS Scards(BatchID integer primary key autoincrement)')
    c.execute('CREATE TABLE IF NOT EXISTS Users(UserID integer primary key autoincrement)')
    c.execute('CREATE TABLE IF NOT EXISTS JobsLog(JobID integer primary key autoincrement)')
    c.close()
    conn.close()
    
def write_fields(table_name,arr):
  for i in range(0,len(arr)):
    utils.add_field(table_name,arr[i][0],arr[i][1])


"""***************************************************************************"""
""" Code execution"""

create_tables()

for i in range(0,len(tables)):
  write_fields(tables[i],table_fields[i])


"""***************************************************************************"""
