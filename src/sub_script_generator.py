#****************************************************************
"""
# This file will query the command line to see what BatchID it should use,
# or if no arguement is given on the CL, the most recent BatchID will be used
# This BatchID is used to identify the proper scard and gcards, and then submission
# files corresponding to each gcard are generated and stored in the database, as
# well as written out to a file with a unique name. This latter part will be passed
# to the server side in the near future.
"""
#****************************************************************

from __future__ import print_function
from utils import utils, file_struct
import sqlite3, os, argparse

#This allows a user to specifiy which batch to use to generate files using a specific BatchID
argparser = argparse.ArgumentParser()
argparser.add_argument('-b','--batchID', default='none', help = 'Enter the ID# of the batch you want to submit (e.g. -b 23)')
argparser.add_argument(file_struct.debug_short,file_struct.debug_longdash,
                      default = file_struct.debug_default,help = file_struct.debug_help)
args = argparser.parse_args()

file_struct.DEBUG = getattr(args,file_struct.debug_long)
#This uses the argument passed from command line, if no args, grab most recent DB entry
def grab_batchID(args):
  if args.batchID != 'none':
    BatchID = args.batchID
  else:
    strn = "SELECT BatchID FROM Batches;"
    Batches = utils.sql3_grab(strn)
    BatchID = max(Batches)[0]
  return BatchID

#Grabs all GCards from a corresponding Batch
def grab_gcards(BatchID):
  strn = "SELECT GcardID, gcard_text FROM GCards WHERE BatchID = {};".format(BatchID)
  gcards = utils.sql3_grab(strn)
  return gcards

#This function writes a file from a file object (see file_struct file). This is currently not done consicely and should be improved for code readability
def write_files(sub_file_obj,params):
  sf = sub_file_obj
  p = params
  if sf.name != file_struct.run_job_obj.name:
    old_vals, new_vals = utils.grab_DB_data(p['table'],sf.overwrite_vals,p['BatchID'])
  else:
    old_vals, new_vals = sf.overwrite_vals.keys(), (file_struct.run_job_obj.overwrite_vals['runscript.overwrite'],)
  utils.printer("Writing submission file '{0}' based off of specifications of BatchID = {1}, GcardID = {2}".format(sf.file_base,
        p['BatchID'],p['GcardID']))
  extension = "_gcard_{}_batch_{}".format(p['GcardID'],p['BatchID'])
  newfile = sf.file_path+sf.file_base+extension+sf.file_end
  out_strn = utils.overwrite_file(p['temp_location']+sf.file_base+sf.file_end+".template",newfile,old_vals,new_vals)
  if sf.file_base == 'runscript':
    out_strn = utils.overwrite_file(newfile,newfile,['gcards_gcard',],[p['gfile'],])#Need to pass arrays to overwrite_file function
    file_struct.run_job_obj.overwrite_vals['runscript.overwrite'] = newfile #this is needed for run_job.sh since we do not go through the database
  str_script_db = out_strn.replace('"',"'") #I can't figure out a way to write "" into a sqlite field without errors
  #For now, we can replace " with ', which works ok, but IDK how it will run if the scripts were submitted to HTCondor
  #for field, value in (sf.file_text_fieldname,str_script_db):
  strn = 'UPDATE Submissions SET {0} = "{1}" WHERE GcardID = {2};'.format(sf.file_text_fieldname,str_script_db,p['GcardID'])
  utils.sql3_exec(strn)

#Grabs batch and gcards as described in respective files
BatchID = grab_batchID(args)
gcards = grab_gcards(BatchID)

#Create a set of submission files for each gcard in the batch
for gcard in gcards:
  GcardID = gcard[0]
  newfile = "gcard_{}_batch_{}.gcard".format(GcardID,BatchID)
  gfile= file_struct.sub_files_path+file_struct.gcards_dir+newfile
  with open(gfile,"w") as file: file.write(gcard[1])
  strn = "INSERT INTO Submissions(BatchID,GcardID) VALUES ({0},{1});".format(BatchID,GcardID)
  utils.sql3_exec(strn)
  params = {'table':'Scards','BatchID':BatchID,'GcardID':GcardID,
            'gfile':gfile,'temp_location':file_struct.template_files_path}
  write_files(file_struct.condor_file_obj,params)
  write_files(file_struct.runscript_file_obj,params)
  write_files(file_struct.run_job_obj,params)
print("\t Successfully generated submission files for Batch {0} \n".format(BatchID))
