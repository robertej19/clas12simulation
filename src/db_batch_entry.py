from __future__ import print_function
from utils import utils, file_struct, scard_helper, gcard_helper
import sqlite3, time, argparse

argparser = argparse.ArgumentParser()
argparser.add_argument(file_struct.debug_short,file_struct.debug_longdash,
                      default = file_struct.debug_default,help = file_struct.debug_help)
args = argparser.parse_args()
file_struct.DEBUG = getattr(args,file_struct.debug_long)

def Batch_Entry(timestamp,scard_file):
    #Assign a user and a timestamp for a given batch
    strn = "INSERT INTO Batches(timestamp) VALUES ({0});".format(timestamp)
    utils.sql3_exec(strn)

    #Write the text contained in scard.txt to a field in the Batches table
    with open(scard_file, 'r') as file: scard = file.read()
    strn = "UPDATE Batches SET {0} = '{1}' WHERE timestamp = {2};".format('scard',scard,timestamp)
    utils.sql3_exec(strn)

    #Grab BatchID to pass to scard table (probably not needed in future)
    strn = "SELECT {0} FROM {1} WHERE timestamp = {2};".format('BatchID','Batches',timestamp)
    BatchID = utils.sql3_grab(strn)[0][0]#The [0][0]  is needed because sql3_grab returns a list of tuples, we need the value
    utils.printer("Batch specifications written to database with BatchID {}".format(BatchID))

    #Write scard into scard table fields (This will not be needed in the future)
    utils.printer("Writing SCard to Database")
    scard_fields = scard_helper.scard_class(scard_file)
    scard_fields.data['group_name'] = scard_fields.data.pop('group') #'group' is a protected word in SQL so we can't use the field title "group"
    scard_fields.data['genExecutable'] = file_struct.genExecutable.get(scard_fields.data.get('generator'))
    scard_fields.data['genOutput'] = file_struct.genOutput.get(scard_fields.data.get('generator'))
    scard_helper.SCard_Entry(BatchID,unixtimestamp,scard_fields.data)

    #Write gcards into gcards table
    utils.printer("Writing GCards to Database")
    gcard_helper.GCard_Entry(BatchID,unixtimestamp,scard_fields.data['gcards'])
    strn = "UPDATE Batches SET {0} = '{1}' WHERE timestamp = {2};".format('User',scard_fields.data['user'],timestamp)
    utils.sql3_exec(strn)

scard_file = file_struct.scard_path+file_struct.scard_name
unixtimestamp = int(time.time()) # Can modify this if need 10ths of seconds or more resolution
Batch_Entry(unixtimestamp,scard_file)
