from __future__ import print_function
import utils, file_struct
import sqlite3

#Create tables in the database
for i in range(0,len(file_struct.tables)):
  utils.create_table(file_struct.DBname,file_struct.tables[i],
                    file_struct.PKs[i],file_struct.foreign_key_relations[i])

#Add fields to each table in the database
for j in range(0,len(file_struct.tables)):
  for i in range(0,(len(file_struct.table_fields[j]))):
    utils.add_field(file_struct.DBname,file_struct.tables[j],
                    file_struct.table_fields[j][i][0],file_struct.table_fields[j][i][1])
