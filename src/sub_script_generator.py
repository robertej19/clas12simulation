from __future__ import print_function
from utils import utils, file_struct
import sqlite3, os, shutil

dirname = os.path.dirname(__file__)
temp_location = dirname + "/templates/"

#Grab values to write from database from table 'SCards'
con_old, con_new, BatchID1, fail_con = utils.grab_DB_data(file_struct.DBname,'Scards',file_struct.SCTable_CondOverwrite)
rs_old, rs_new, BatchID2, fail_rs = utils.grab_DB_data(file_struct.DBname,'Scards',file_struct.SCTable_RSOverwrite)

#This error message should not be needed as the above should be rewritten in a better way
if BatchID1 != BatchID2:
  print("ERROR: BatchID1 and BatchID2 Do NOT Match, quitting")
  exit()

if fail_con + fail_rs == 0: #I think there is a better way to handle error conditions, should recode this part
  #As constructed, this will only run if grab_DB_data returns 0 for both condor and runscript
  #Write from template files out to submission files
  print("\nWriting submission files based off of specifications of scard from BatchID = {} \n".format(BatchID2))
  utils.overwrite_file(temp_location+"clas12.condor.template",con_old,con_new,BatchID1,file_struct.condor_field)
  utils.overwrite_file(temp_location+"runscript.sh.template",rs_old,rs_new,BatchID2,file_struct.runscript_field)
else:
  print('Error retrieving values from database. Are you sure database is populated?')

files = ["/runscript.sh","/clas12.condor"]
cwd = os.getcwd()
for file in files:
  old = temp_location+file
  new = cwd+file
  shutil.move(old,new)
  #Should these files be given unique names so they are not overwritten everytime?


"""Also need to generate gcard for submission from GCards table,
and pass location to runscript """
#oldvals, newvals = [],[]
#    for key in dictionary:
strn = "SELECT gcard_text FROM GCards WHERE BatchID = {};".format(BatchID1)#This just grabs the most recent DB entry.
value = utils.sql3_grab(file_struct.DBname,strn)
#print(value)
