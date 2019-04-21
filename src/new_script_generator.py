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
import subprocess, sqlite3, time, os, argparse
from script_generators import startup,initialization,run_gemc,run_evio2hipo,run_cooking,file_mover
from utils import utils, file_struct, scard_helper, user_validation, gcard_helper
from condor_scripts import condor_startup, condor_1, condor_2

#This uses the argument passed from command line, if no args, grab most recent DB entry
def grab_batchID(args):
  Batches = []
  strn = "SELECT BatchID FROM Batches;"
  Batches_array = utils.sql3_grab(strn)
  for i in Batches_array: Batches.append(i[0])
  if args.BatchID != 'none':
    if not int(args.BatchID) in Batches:
      print("The selected batch (BatchID = {0}) does not exist, exiting".format(args.BatchID))
      exit()
    else:
      BatchID = args.BatchID
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

#Grabs all GCards from a corresponding Batch
def grab_username(BatchID):
  strn = "SELECT user FROM Batches WHERE BatchID = {};".format(BatchID)
  username = utils.sql3_grab(strn)
  return username

#Generates a script by appending functions that output strings
def script_factory(script_obj,gen_funcs,func_names,scard,params):
  script_text = ""
  utils.printer("\tWriting submission file '{0}' based off of specifications of BatchID = {1}, GcardID = {2}".format(script_obj.name,
      params['BatchID'],params['GcardID']))
  if os.path.isfile(script_obj.name):
    subprocess.call(['rm',script_obj.name])
  for count, f in enumerate(gen_funcs):
    generated_text = getattr(f,func_names[count])(scard)
    with open(script_obj.name,"a") as file: file.write(generated_text)
    script_text += generated_text
  str_script_db = script_text.replace('"',"'") #I can't figure out a way to write "" into a sqlite field without errors
    #For now, we can replace " with ', which works ok, but IDK how it will run if the scripts were submitted to HTCondor
  strn = 'UPDATE Submissions SET {0} = "{1}" WHERE GcardID = {2};'.format(script_obj.file_text_fieldname,str_script_db,params['GcardID'])
  utils.sql3_exec(strn)

def submission_script_maker(args):
  file_struct.DEBUG = getattr(args,file_struct.debug_long)
  #Grabs batch and gcards as described in respective files
  BatchID = grab_batchID(args)
  gcards = grab_gcards(BatchID)
  username = grab_username(BatchID)

  funcs_rs = (startup,initialization,run_gemc,run_evio2hipo,run_cooking,file_mover)
  fname_rs = ('startup','initialization','run_gemc','run_evio2hipo','run_cooking','file_mover')
  funcs_kwargs_rs = ('','','','','','')

  funcs_condor = (condor_startup,condor_1,condor_2)
  fname_condor = ('condor_startup','condor_1','condor_2')
  func_kwargs_condor = ('','','')

  strn = "SELECT scard FROM Batches WHERE BatchID = {};".format(BatchID)
  scard_text = utils.sql3_grab(strn)[0][0] #sql3_grab returns a list of tuples, we need the 0th element of the 0th element
  scard = scard_helper.scard_class(scard_text)


  scard.data['genExecutable'] = file_struct.genExecutable.get(scard.data.get('generator'))
  scard.data['genOutput'] = file_struct.genOutput.get(scard.data.get('generator'))

  for gcard in gcards:
    GcardID = gcard[0]
    strn = "INSERT INTO Submissions(BatchID,GcardID) VALUES ({0},{1});".format(BatchID,GcardID)
    utils.sql3_exec(strn)
    strn = "UPDATE Submissions SET submission_pool = '{0}' WHERE GcardID = '{1}';".format(scard.data['farm_name'],GcardID)
    utils.sql3_exec(strn)
    strn = "UPDATE Submissions SET run_status = 'not yet in pool' WHERE GcardID = '{0}';".format(GcardID)
    utils.sql3_exec(strn)

    """
    Need to have block of code for grabbing appropriate gcard. For now, just assume we grab
    the standard gcard so we don't have to worry about this
    newfile = "gcard_{}_batch_{}.gcard".format(GcardID,BatchID)
    gfile= file_struct.sub_files_path+file_struct.gcards_dir+newfile
    with open(gfile,"w") as file: file.write(gcard[1])
    """
    params = {'table':'Scards','BatchID':BatchID,'GcardID':GcardID,
              'gfile':'gfile'}
    script_factory(file_struct.runscript_file_obj,funcs_rs,fname_rs,scard,params)
    script_factory(file_struct.condor_file_obj,funcs_condor,fname_condor,scard,params)
  print("\tSuccessfully generated submission files for Batch {0} \n".format(BatchID))

if __name__ == "__main__":
  argparser = argparse.ArgumentParser()
  argparser.add_argument('-b','--BatchID', default='none', help = 'Enter the ID# of the batch you want to submit (e.g. -b 23)')
  argparser.add_argument('-s','--scard', default=file_struct.scard_path+file_struct.scard_name,
                      help = 'relative path and name scard you want to submit, e.g. ../scard.txt')
  argparser.add_argument(file_struct.debug_short,file_struct.debug_longdash,
                      default = file_struct.debug_default,help = file_struct.debug_help)
  args = argparser.parse_args()

  file_struct.DEBUG = getattr(args,file_struct.debug_long)

  submission_script_maker(args)
