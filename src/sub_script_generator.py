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

def wrile(file_path,filebase,file_end,DBname,table,overwrite_vals,BatchID,field_loc,GcardID,gfile):
  old_vals, new_vals = utils.grab_DB_data(DBname,table,overwrite_vals,BatchID)
  print("\nWriting submission file '{0}' based off of specifications of scard from BatchID = {1} \n".format(filebase,BatchID))
  extension = "_gcard_{}_batch_{}".format(GcardID,BatchID)
  newfile = file_path+filebase+extension+file_end
  out_strn = utils.overwrite_file(temp_location+filebase+file_end+".template",newfile,old_vals,new_vals)
  if filebase == 'runscript':
    out_strn = utils.overwrite_file(newfile,newfile,['gcards_gcard',],[gfile,])
  str_script_db = out_strn.replace('"',"'") #I can't figure out a way to write "" into a sqlite field without errors
  #For now, we can replace " with ', which works ok, but IDK how it will run if the scripts were submitted to HTCondor
  strn = 'UPDATE Submissions SET {0} = "{1}" WHERE GcardID = {2};'.format(field_loc,str_script_db,GcardID)
  print("Saving submission script to batch field '{0}' with BatchID = {1} \n".format(field_loc,BatchID))
  utils.sql3_exec(file_struct.DBname,strn)



BatchID = grab_batchID(dirname,args)
gcards = grab_gcards(dirname,BatchID)

#gcards_gcard

for gcard in gcards:
  GcardID = gcard[0]
  newfile = "gcard_{}_batch_{}.gcard".format(GcardID,BatchID)
  gfile= sub_files_path+file_struct.gcards_dir+newfile
  with open(gfile,"w") as file: file.write(gcard[1])
  strn = "INSERT INTO Submissions(BatchID,GcardID) VALUES ({0},{1});".format(BatchID,GcardID)
  utils.sql3_exec(file_struct.DBname,strn)
  wrile(sub_files_path+file_struct.condor_dir,'clas12','.condor',
      file_struct.DBname,'Scards',file_struct.SCTable_CondOverwrite,BatchID,file_struct.condor_field,GcardID,gfile)
  wrile(sub_files_path+file_struct.runscript_dir,'runscript','.sh',
      file_struct.DBname,'Scards',file_struct.SCTable_RSOverwrite,BatchID,file_struct.runscript_field,GcardID,gfile)
