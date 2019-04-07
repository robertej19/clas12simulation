from __future__ import print_function
from utils import utils, file_struct
import sqlite3, os, shutil, argparse

dirname = os.path.dirname(__file__)
temp_location = dirname + "/templates/"

argparser = argparse.ArgumentParser()
argparser.add_argument('-b','--batchID', default='none', help = 'Enter the ID# of the batch you want to submit')
args = argparser.parse_args()

def grab_batchID(dirname):
  conn = sqlite3.connect(dirname+file_struct.DB_rel_location_src+file_struct.DBname)
  c = conn.cursor()
  strn = "SELECT BatchID FROM Batches;"
  c.execute(strn)
  batches = c.fetchall()
  return batches

if args.batchID != 'none':
  batchID = args.batchID
else:
  batches = grab_batchID(dirname)
  batchID = max(batches)[0]

print(batchID)

"""
#Grab values to write from database from table 'SCards'
con_old, con_new, BatchID1, fail_con = utils.grab_DB_data(file_struct.DBname,'Scards',file_struct.SCTable_CondOverwrite)
rs_old, rs_new, BatchID2, fail_rs = utils.grab_DB_data(file_struct.DBname,'Scards',file_struct.SCTable_RSOverwrite)

def grab_gcards(dirname,BatchID):
  conn = sqlite3.connect(dirname+file_struct.DB_rel_location_src+file_struct.DBname)
  c = conn.cursor()
  strn = "SELECT GcardID, gcard_text FROM GCards WHERE BatchID = {};".format(BatchID)#This just grabs the most recent DB entry.
  c.execute(strn)
  gcards = c.fetchall()
  return gcards

gcards = grab_gcards(dirname,BatchID1)

for gcard in gcards:
  GcardID = gcard[0]
  newfile = "gcard"+str(GcardID)+".gcard"
  file_loc= file_struct.sub_files_rel_location_src+'gcards/'
  print(file_loc+newfile)
  #print(gcard[1])
  with open(file_loc+newfile,"w") as file: file.write(gcard[1])
"""
"""
#This error message should not be needed as the above should be rewritten in a better way
if BatchID1 != BatchID2:
  print("ERROR: BatchID1 and BatchID2 Do NOT Match, quitting")
  exit()


if fail_con + fail_rs == 0: #I think there is a better way to handle error conditions, should recode this part
  #As constructed, this will only run if grab_DB_data returns 0 for both condor and runscript
  #Write from template files out to submission files
  print("\nWriting submission files based off of specifications of scard from BatchID = {} \n".format(BatchID2))
  conout = utils.overwrite_file(temp_location+"clas12.condor.template",con_old,con_new,BatchID1,file_struct.condor_field)
  runout = utils.overwrite_file(temp_location+"runscript.sh.template",rs_old,rs_new,BatchID2,file_struct.runscript_field)
else:
  print('Error retrieving values from database. Are you sure database is populated?')

files = ["/runscript.sh","/clas12.condor"]
cwd = os.getcwd()
for file in files:
  old = temp_location+file
  new = cwd+file
  shutil.move(old,new)
  #Should these files be given unique names so they are not overwritten everytime?

def submission_writer(BatchID,conout):
#Assign a user and a timestamp for a given batch
    strn = "INSERT INTO Submissions(BatchID) VALUES ({0});".format(BatchID)
    utils.sql3_exec(file_struct.DBname,strn)
    str_script_db = conout.replace('"',"'") #I can't figure out a way to write "" into a sqlite field without errors
    #For now, we can replace " with ', which works ok, but IDK how it will run if the scripts were submitted to HTCondor
    strn = 'UPDATE Submissions SET {0} = "{1}" WHERE BatchID = {2};'.format(file_struct.condor_field,str_script_db,BatchID)
    print("Saving submission script to batch field '{0}' with BatchID = {1} \n".format(file_struct.condor_field,BatchID))
    utils.sql3_exec(file_struct.DBname,strn)

submission_writer(BatchID1,conout)
"""
