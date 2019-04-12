#****************************************************************
"""
# Takes in an scard, then calls gcard_helper and scard_helper to populate the
# database based off the batchID.
"""
#****************************************************************
from __future__ import print_function
from utils import utils, file_struct, scard_helper, user_validation #See below as gcard_helper is also imported
import sqlite3, time, os, argparse
from utils import gcard_helper #There is a bug with gcard_helper argparser interfering
#with the argparser in this script.I had to include the scard flag in the argparser in gcard_helper
#Or else this file won't include the -s --scard flags as useable

def Batch_Entry(scard_file):
    unixtimestamp = int(time.time()) # Can modify this if need 10ths of seconds or more resolution
    #Assign a user and a timestamp for a given batch
    print(str(utils.timeconvert(unixtimestamp)))
    strn = "INSERT INTO Batches(timestamp) VALUES ({0});".format(utils.timeconvert(unixtimestamp))
    utils.sql3_exec(strn)

    #Grab BatchID to pass to scard table (probably not needed in future)
    strn = "SELECT {0} FROM {1} WHERE timestamp = {2};".format('BatchID','Batches',utils.timeconvert(unixtimestamp))
    BatchID = utils.sql3_grab(strn)[0][0]#The [0][0]  is needed because sql3_grab returns a list of tuples, we need the value
    utils.printer("Batch specifications written to database with BatchID {}".format(BatchID))

    #Write the text contained in scard.txt to a field in the Batches table
    with open(scard_file, 'r') as file: scard = file.read()
    strn = "UPDATE Batches SET {0} = '{1}' WHERE BatchID = {2};".format('scard',scard,BatchID)
    utils.sql3_exec(strn)


    #See if user exists already in database; if not, add them
    scard_fields = scard_helper.scard_class(scard_file)
    user_validation.user_validation()

    #Write scard into scard table fields (This will not be needed in the future)
    print("\nReading in information from {0}".format(scard_file))
    utils.printer("Writing SCard to Database")
    scard_fields.data['group_name'] = scard_fields.data.pop('group') #'group' is a protected word in SQL so we can't use the field title "group"
    # For more information on protected words in SQL, see https://docs.intersystems.com/irislatest/csp/docbook/DocBook.UI.Page.cls?KEY=RSQL_reservedwords
    scard_fields.data['genExecutable'] = file_struct.genExecutable.get(scard_fields.data.get('generator'))
    scard_fields.data['genOutput'] = file_struct.genOutput.get(scard_fields.data.get('generator'))
    scard_helper.SCard_Entry(BatchID,unixtimestamp,scard_fields.data)
    print('\t Your scard has been read into the database with BatchID = {0} at {1} \n'.format(BatchID,
                                          utils.timeconvert(unixtimestamp)))

    """
    #Write gcards into gcards table
    utils.printer("Writing GCards to Database")
    gcard_helper.GCard_Entry(BatchID,unixtimestamp,scard_fields.data['gcards'])
    print("Successfully added gcards to database")
    strn = "UPDATE Batches SET {0} = '{1}' WHERE BatchID = {2};".format('User',scard_fields.data['user'],BatchID)
    utils.sql3_exec(strn)
    """

    return 0

if __name__ == "__main__":
  argparser = argparse.ArgumentParser()
  argparser.add_argument('-s','--scard', default=file_struct.scard_path+file_struct.scard_name,
                      help = 'relative path and name scard you want to submit, e.g. ../scard.txt')
  argparser.add_argument(file_struct.debug_short,file_struct.debug_longdash,
                      default = file_struct.debug_default,help = file_struct.debug_help)
  args = argparser.parse_args()



  file_struct.DEBUG = getattr(args,file_struct.debug_long)
  scard_file = args.scard
  Batch_Entry(scard_file)
