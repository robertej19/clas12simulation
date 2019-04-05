from __future__ import print_function
import scard_parser, sqlite3, file_struct, time
import utils

def Batch_Entry(DBname,UID,timestamp,scard_file):
    strnx = "INSERT INTO Batches(UserID,timestamp) VALUES ('{0}',{1});".format(UID,timestamp)
    utils.sql3_exec(file_struct.DBname,strnx)
    with open(scard_file, 'r') as file: scard = file.read()
    print(scard)
    strn = "UPDATE Batches SET {0} = '{1}' WHERE timestamp = {2};".format('scard',scard,unixtimestamp)
    utils.sql3_exec(file_struct.DBname,strn)

scard_file = "scard.txt"

UID = 1 #This 1 references the first USER listed in the USERS table of the database. This User must exist, or else an error will be thrown.
#This above (UID) is more or less a placeholder, currently. Explained in 20190312 PR documentation
unixtimestamp = int(time.time()) # Can modify this if need 10ths of seconds or more resolution
Batch_Entry(file_struct.DBname,UID,unixtimestamp,scard_file)
