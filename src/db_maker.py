from __future__ import print_function
import sqlite3, utils, file_struct


tab_fields = [file_struct.users_fields,file_struct.batches_fields,
              file_struct.scards_fields,file_struct.jobslog_fields]

#Create tables in the database
for i in range(0,len(file_struct.tables)):
  utils.create_table(file_struct.DBname,file_struct.tables[i],file_struct.PKs[i],file_struct.foreign_key_relations[i])

#Add fields to each table in the database
for j in range(0,len(file_struct.tables)):
  for i in range(0,(len(tab_fields[j]))):
    utils.add_field(file_struct.DBname,file_struct.tables[j],tab_fields[j][i][0],tab_fields[j][i][1])
