from __future__ import print_function
import sqlite3, utils, file_struct


tables = ['Users','Scards','JobsLog']
PKs = ['UserID','BatchID','JobID']
tab_fields = [file_struct.users_fields,file_struct.scard_fields,file_struct.jobslog_fields]

#Create tables in the database
for i in range(0,len(tables)):
  utils.create_table(file_struct.DBname,tables[i],PKs[i])

#Add fields to each table in the database
for j in range(0,len(tables)):
  for i in range(0,(len(tab_fields[j]))):
    utils.add_field(file_struct.DBname,tables[j],tab_fields[j][i][0],tab_fields[j][i][1])
