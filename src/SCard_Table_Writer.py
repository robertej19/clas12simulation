from __future__ import print_function
import scard_parser, sqlite3, file_struct, time
import utils

def SCard_Entry(DBname,UID,timestamp,scard_dict,):
    strnx = "INSERT INTO Scards(UserID,timestamp) VALUES ('{0}',{1});".format(UID,timestamp)
    utils.sql3_exec(file_struct.DBname,strnx)
    for key in scard_dict:
      strn = "UPDATE Scards SET {0} = '{1}' WHERE timestamp = {2};".format(key,scard_dict[key],unixtimestamp)
      utils.sql3_exec(file_struct.DBname,strn)
    print("SCard record added to database")

filename = "scard.txt"
scard_fields = scard_parser.scard_parser(filename)
scard_fields.data['group_name'] = scard_fields.data.pop('group') #'group' is a protected word in SQL so we can't use the field title "group"
scard_fields.data['genExecutable'] = file_struct.genExecutable.get(scard_fields.data.get('generator'))
scard_fields.data['genOutput'] = file_struct.genOutput.get(scard_fields.data.get('generator'))

UID = "robertej" #This is more or less a placeholder, currently. Explained in 20190312 PR documentation
unixtimestamp = int(time.time()) # Can modify this if need 10ths of seconds or more resolution
SCard_Entry(file_struct.DBname,UID,unixtimestamp,scard_fields.data)
