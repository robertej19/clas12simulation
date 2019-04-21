from __future__ import print_function
import subprocess, sqlite3, time, os, argparse
from script_generators import startup,initialization,run_gemc,run_evio2hipo,run_cooking,file_mover
from utils import utils, file_struct, scard_helper, user_validation, gcard_helper
from condor_scripts import condor_startup, condor_1, condor_2

def script_generator(script_name,gen_funcs,func_names,scard):
  newfile = "runscript.sh"
  if os.path.isfile(newfile):
    subprocess.call(['rm',newfile])
  for count, f in enumerate(funcs):
    generated_text = getattr(f,fname[count])(scard)
    with open(newfile,"a") as file: file.write(generated_text)

  newfile = "clas12.condor"
  if os.path.isfile(newfile):
    subprocess.call(['rm',newfile])
  for count, f in enumerate(funcs_condor):
    generated_text = getattr(f,fname_condor[count])(scard)
    with open(newfile,"a") as file: file.write(generated_text)

def grabber(scard_file,BatchID):
  funcs = (startup,initialization,run_gemc,run_evio2hipo,run_cooking,file_mover)
  fname = ('startup','initialization','run_gemc','run_evio2hipo','run_cooking','file_mover')
  funcs_condor = (condor_startup,condor_1,condor_2)
  fname_condor = ('condor_startup','condor_1','condor_2')

  strn = "SELECT scard FROM Batches WHERE BatchID = {};".format(BatchID)
  scard_text = utils.sql3_grab(strn)[0][0] #sql3_grab returns a list of tuples, we need the 0th element of the 0th element
  scard = scard_helper.scard_class(scard_text)
  username = user_validation.user_validation()

  print("\nReading in information from {0}".format(scard_file))
  utils.printer("Writing SCard to Database")
  scard.data['genExecutable'] = file_struct.genExecutable.get(scard.data.get('generator'))
  scard.data['genOutput'] = file_struct.genOutput.get(scard.data.get('generator'))

  """
  Need to have block of code for grabbing appropriate gcard. For now, just assume we grab
  the standard gcard so we don't have to worry about this
  """

  script_generator("runscript.sh",funcs,fname,scard):
  script_generator("clas12.condor",funcs_condor,fname_condor,scard):

if __name__ == "__main__":
  argparser = argparse.ArgumentParser()
  argparser.add_argument('-s','--scard', default=file_struct.scard_path+file_struct.scard_name,
                      help = 'relative path and name scard you want to submit, e.g. ../scard.txt')
  argparser.add_argument(file_struct.debug_short,file_struct.debug_longdash,
                      default = file_struct.debug_default,help = file_struct.debug_help)
  args = argparser.parse_args()

  file_struct.DEBUG = getattr(args,file_struct.debug_long)
  scard_file = args.scard
  BatchID = 1
  grabber(scard_file,BatchID)
