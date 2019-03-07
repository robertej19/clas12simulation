import sqlite3
### Need to make scard USERID, JOBSLOGS BATCHID AND USERID to be relational constricted
## Figure out proper datestamping - DATETIME DEFAULT CURRENT_TIMESTAMP
#Use epoch time in runscripts

#Note: "Group" is a reserved word in SQL and so cannot be used for field name
# https://docs.intersystems.com/irislatest/csp/docbook/DocBook.UI.Page.cls?KEY=RSQL_reservedwords
#Field tuples contain all fields except for PK

"""***************************************************************************"""
""" DB Schema Specification """

scard_fields = (('UserID','TEXT'),('Group_name','INT'),('User','INT'),('Nevents','INT'),
                ('Generator','TEXT'),('GenOptions','TEXT'),('Gcards','TEXT'),('Jobs','INT'),
                ('Project','TEXT'),('Luminosity','INT'),('Tcurrent','INT'),('Pcurrent','INT'),
                ('Cores Requested','INT'),('Memory Requested','INT'))

users_fields = (('Username','TEXT'),('Affiliation','TEXT'),('JoinDateStamp','INT'),
                ('Permissions','TEXT'),('Default_Output_Dir','TEXT'),('Total_Batches','INT'),
                ('Total_Jobs','INT'),('Total_Events','INT'),('Most_Recent_Active_Date','INT'))

jobslog_fields = (('BatchID', 'TEXT'),('UserID','TEXT'),('Job_Submission_Datestamp','INT'),
                  ('Job_Completion_Datestamp','TEXT'),('Output_file_directory','TEXT'),
                  ('Output_file_size','INT'),('Number_Job_failures','INT'))

tables = ['Users','Scards','JobsLog']
table_fields = [users_fields,scard_fields,jobslog_fields]

"""***************************************************************************"""
"""***************************************************************************"""
""" Function definitions"""

def create_tables():
    c.execute('CREATE TABLE IF NOT EXISTS Scards(BatchID integer primary key autoincrement)')
    c.execute('CREATE TABLE IF NOT EXISTS Users(UserID integer primary key autoincrement)')
    c.execute('CREATE TABLE IF NOT EXISTS JobsLog(JobID integer primary key autoincrement)')

def add_column(tablename,field_name,field_type):
  print(tablename)
  print(field_name)
  print(field_type)
  c.execute('ALTER TABLE %s ADD COLUMN %s %s' % (tablename,field_name, field_type))


def write_fields(table_name,arr):
  for i in range(0,len(arr)):
    add_column(table_name,arr[i][0],arr[i][1])


"""***************************************************************************"""
""" Code execution"""

conn = sqlite3.connect('CLAS12_OCRDB.db')
c = conn.cursor()

create_tables()

for i in range(0,len(tables)):
  write_fields(tables[i],table_fields[i])

c.close()
conn.close()
"""***************************************************************************"""
