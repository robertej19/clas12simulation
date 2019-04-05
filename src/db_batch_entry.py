from __future__ import print_function
from utils import utils, file_struct, scard_helper
import sqlite3, time

def Batch_Entry(DBname,UID,timestamp,scard_file):
    #Assign a user and a timestamp for a given batch
    strn = "INSERT INTO Batches(UserID,timestamp) VALUES ('{0}',{1});".format(UID,timestamp)
    utils.sql3_exec(file_struct.DBname,strn)

    #Write the text contained in scard.txt to a field in the Batches table
    with open(scard_file, 'r') as file: scard = file.read()
    strn = "UPDATE Batches SET {0} = '{1}' WHERE timestamp = {2};".format('scard',scard,timestamp)
    utils.sql3_exec(file_struct.DBname,strn)

    #Grab BatchID to pass to scard table (probably not needed in future)
    strn = "SELECT {0} FROM {1} WHERE timestamp = {2};".format('BatchID','Batches',timestamp)
    BatchID = utils.sql3_grab(file_struct.DBname,strn)
    print("Batch specifications written to database with BatchID {}".format(BatchID))

    #Write scard into scard table fields (This will not be needed in the future)
    scard_fields = scard_helper.scard_class(scard_file)
    scard_fields.data['group_name'] = scard_fields.data.pop('group') #'group' is a protected word in SQL so we can't use the field title "group"
    scard_fields.data['genExecutable'] = file_struct.genExecutable.get(scard_fields.data.get('generator'))
    scard_fields.data['genOutput'] = file_struct.genOutput.get(scard_fields.data.get('generator'))
    scard_helper.SCard_Entry(file_struct.DBname,UID,BatchID,unixtimestamp,scard_fields.data)

    #Write gcards into gcards table
    """This function needs to be created
    we can use scard_fields.gcards to find location of gcard files
    then use wget to make local
    finally read in using with open(gcard_file, 'r'), similar to above, to write to db"""

scard_file = "scard.txt"
UID = 1 #This 1 references the first USER listed in the USERS table of the database. This User must exist, or else an error will be thrown.
#This above (UID) is more or less a placeholder, currently. Explained in 20190312 PR documentation
unixtimestamp = int(time.time()) # Can modify this if need 10ths of seconds or more resolution
Batch_Entry(file_struct.DBname,UID,unixtimestamp,scard_file)
