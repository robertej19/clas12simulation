from __future__ import print_function
from utils import utils, file_struct
import sqlite3, os, shutil, argparse

dirname = os.path.dirname(__file__)
if dirname == '': dirname = '.' #Need this because if running in this file's directory, dirname is blank
db_path = dirname+file_struct.DB_rel_location_src+file_struct.DBname
sub_files_path = dirname+file_struct.sub_files_rel_location


temp_location = dirname + "/templates/"
argparser = argparse.ArgumentParser()
argparser.add_argument('-b','--batchID', default='none', help = 'Enter the ID# of the batch you want to submit')
args = argparser.parse_args()

def grab_batchID(dirname,args):
  if args.batchID != 'none':
    BatchID = args.batchID
  else:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    strn = "SELECT BatchID FROM Batches;"
    c.execute(strn)
    Batches = c.fetchall()
    BatchID = max(Batches)[0]
  return BatchID

def grab_gcards(dirname,BatchID):
  conn = sqlite3.connect(db_path)
  c = conn.cursor()
  strn = "SELECT GcardID, gcard_text FROM GCards WHERE BatchID = {};".format(BatchID)#This just grabs the most recent DB entry.
  c.execute(strn)
  gcards = c.fetchall()
  return gcards

BatchID = grab_batchID(dirname,args)
gcards = grab_gcards(dirname,BatchID)
con_old, con_new = utils.grab_DB_data(file_struct.DBname,
                                      'Scards',file_struct.SCTable_CondOverwrite,BatchID)
rs_old, rs_new = utils.grab_DB_data(file_struct.DBname,
                                    'Scards',file_struct.SCTable_RSOverwrite,BatchID)
for gcard in gcards:
  GcardID = gcard[0]
  newfile = "gcard_{}_batch_{}.gcard".format(GcardID,BatchID)
  file_loc= sub_files_path+'gcards/'
  print(file_loc+newfile)
  with open(file_loc+newfile,"w") as file: file.write(gcard[1])
  strn = "INSERT INTO Submissions(BatchID,GcardID) VALUES ({0},{1});".format(BatchID,GcardID)
  utils.sql3_exec(file_struct.DBname,strn)


#Write from template files out to submission files
print("\nWriting submission files based off of specifications of scard from BatchID = {} \n".format(BatchID))
conout = utils.overwrite_file(temp_location+"clas12.condor.template",con_old,con_new,BatchID,file_struct.condor_field)
runout = utils.overwrite_file(temp_location+"runscript.sh.template",rs_old,rs_new,BatchID,file_struct.runscript_field)

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

submission_writer(BatchID,conout)
