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

def wrile(sub_file_obj,params):
  run_script_loc = ''
  sf = sub_file_obj
  p = params
  if sf.name != file_struct.run_job_obj.name:
    old_vals, new_vals = utils.grab_DB_data(p['DBname'],p['table'],sf.overwrite_vals,p['BatchID'])
  else:
    #print(sf.overwrite_vals.keys()[0])
    old_vals, new_vals = sf.overwrite_vals.keys(), (run_script_loc,)
  print("\nWriting submission file '{0}' based off of specifications of BatchID = {1}, GcardID = {2}".format(sf.filebase,
        p['BatchID'],p['GcardID']))
  extension = "_gcard_{}_batch_{}".format(p['GcardID'],p['BatchID'])
  newfile = sf.file_path+sf.filebase+extension+sf.file_end
  out_strn = utils.overwrite_file(p['temp_location']+sf.filebase+sf.file_end+".template",newfile,old_vals,new_vals)
  if sf.filebase == 'runscript':
    out_strn = utils.overwrite_file(newfile,newfile,['gcards_gcard',],[p['gfile'],])#Need to pass arrays to overwrite_file function
    run_script_loc = newfile
  str_script_db = out_strn.replace('"',"'") #I can't figure out a way to write "" into a sqlite field without errors
  #For now, we can replace " with ', which works ok, but IDK how it will run if the scripts were submitted to HTCondor
  for field, value in ((sf.field_loc,str_script_db),(sf.script_name,newfile)):
    strn = 'UPDATE Submissions SET {0} = "{1}" WHERE GcardID = {2};'.format(field,value,p['GcardID'])
    utils.sql3_exec(file_struct.DBname,strn)

BatchID = grab_batchID(dirname,args)
gcards = grab_gcards(dirname,BatchID)

for gcard in gcards:
  GcardID = gcard[0]
  newfile = "gcard_{}_batch_{}.gcard".format(GcardID,BatchID)
  gfile= sub_files_path+file_struct.gcards_dir+newfile
  with open(gfile,"w") as file: file.write(gcard[1])
  strn = "INSERT INTO Submissions(BatchID,GcardID) VALUES ({0},{1});".format(BatchID,GcardID)
  utils.sql3_exec(file_struct.DBname,strn)
  params = {'DBname':file_struct.DBname,'table':'Scards','BatchID':BatchID,'GcardID':GcardID,
            'gfile':gfile,'temp_location':temp_location}
  wrile(file_struct.condor_file_obj,params)
  wrile(file_struct.runscript_file_obj,params)
  wrile(file_struct.run_job_obj,params)
