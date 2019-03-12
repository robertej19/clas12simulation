from __future__ import print_function
import sqlite3, file_struct, utils, os, shutil

cwd = os.getcwd()
print(cwd)
temp_location = cwd + "/templates/"

#Grab values to write from database from table 'SCards'
con_old, con_new, fail_con = utils.grab_DB_data(file_struct.DBname,'Scards',file_struct.SCTable_CondOverwrite)
rs_old, rs_new, fail_rs = utils.grab_DB_data(file_struct.DBname,'Scards',file_struct.SCTable_RSOverwrite)

if fail_con + fail_rs == 0: #I think there is a better way to handle error conditions, should recode this part
  #As constructed, this will only run if grab_DB_data returns 0 for both condor and runscript
  #Write from template files out to submission files
  utils.overwrite_file(temp_location+"clas12.condor.template",con_old,con_new)
  utils.overwrite_file(temp_location+"runscript.sh.template",rs_old,rs_new)
else:
  print('Error retrieving values from database. Are you sure database is populated?')

files = ["/runscript.sh","/clas12.condor"]
for file in files:
  old = temp_location+file
  new = cwd+file
  shutil.move(old,new)
  #Should these files be given unique names so they are not overwritten everytime?
