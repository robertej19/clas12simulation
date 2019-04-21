from __future__ import print_function
import subprocess, sqlite3, time, os, argparse
from script_generators import startup,initialization,run_gemc,run_evio2hipo,run_cooking,file_mover
from utils import utils, file_struct, scard_helper, user_validation, gcard_helper


def grabber(scard_file):
  funcs = (startup,initialization,run_gemc,run_evio2hipo,run_cooking,file_mover)
  fname = ('startup','initialization','run_gemc','run_evio2hipo','run_cooking','file_mover')

  scard = scard_helper.scard_class(scard_file)
  username = user_validation.user_validation()

  #Write scard into scard table fields (This will not be needed in the future)
  print("\nReading in information from {0}".format(scard_file))
  utils.printer("Writing SCard to Database")
  scard.data['genExecutable'] = file_struct.genExecutable.get(scard.data.get('generator'))
  scard.data['genOutput'] = file_struct.genOutput.get(scard.data.get('generator'))
  #scard_helper.SCard_Entry(BatchID,timestamp,scard_fields.data)
  #print('\t Your scard has been read into the database with BatchID = {0} at {1} \n'.format(BatchID,timestamp))

  for item in scard.data:
    #print(scard.data.get(item))
    print(item)
  newfile = "runscript.sh"
  if os.path.isfile(newfile):
    subprocess.call(['rm',newfile])
  for count, f in enumerate(funcs):
    generated_text = getattr(f,fname[count])(scard)
    with open(newfile,"a") as file: file.write(generated_text)

"""
    with open(scard_file, 'r') as file: scard = file.read()
    strn = "UPDATE Batches SET {0} = '{1}' WHERE BatchID = "{2}";"""""".format('scard',scard,BatchID)
    utils.sql3_exec(strn)
"""
"""


"""
if __name__ == "__main__":
  argparser = argparse.ArgumentParser()
  argparser.add_argument('-s','--scard', default=file_struct.scard_path+file_struct.scard_name,
                      help = 'relative path and name scard you want to submit, e.g. ../scard.txt')
  argparser.add_argument(file_struct.debug_short,file_struct.debug_longdash,
                      default = file_struct.debug_default,help = file_struct.debug_help)
  args = argparser.parse_args()

  file_struct.DEBUG = getattr(args,file_struct.debug_long)
  scard_file = args.scard
  grabber(scard_file)
