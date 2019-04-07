from __future__ import print_function
import file_struct, sqlite3, os

#Takes in a .template file, a list of values to replace (old_vals) and a list of what to replace them with (new_vals)
def overwrite_file(template_file,old_vals,new_vals,BatchID,batch_field): #template_file = str, old_vals, new_vals = LIST
    with open(template_file,"r") as tmp: str_script = tmp.read()
    newfile = str(template_file)[:-9]#This removes the '.template' ending
    for i in range(0,len(old_vals)):
      str_script = str_script.replace(old_vals[i],str(new_vals[i]))
    print("Overwriting '{0}'".format(newfile))
    with open(newfile,"w") as file: file.write(str_script)
    return str_script


#Takes a dictionary, retuns 2 lists: key (oldvals) and value (newvals) from table in DBName
def grab_DB_data(DBname,table,dictionary): #DBName, table = str, dictionary = dict
    oldvals, newvals = [],[]
    for key in dictionary:
      strn = "SELECT {0} FROM {1} ORDER BY ScardID DESC LIMIT 1;".format(dictionary[key],table)#This just grabs the most recent DB entry.
      value = sql3_grab(DBname,strn)
      oldvals.append(key)
      newvals.append(value)
    strn = "SELECT {0} FROM {1} ORDER BY ScardID DESC LIMIT 1;".format("BatchID",table)#This just grabs the most recent DB entry.
    batchID = sql3_grab(DBname,strn)
    return oldvals, newvals, batchID, 0

#Add a field to an existing DB. Need to add error statements if DB or table does not exist
def add_field(DBname,tablename,field_name,field_type):
  strn = "ALTER TABLE {0} ADD COLUMN {1} {2}".format(tablename,field_name, field_type)
  sql3_exec(DBname,strn)
  print('In database {0}, table {1} has succesfully added field {2}'.format(DBname,tablename,field_name))

#Create a table in a database
def create_table(DBname,tablename,PKname,FKargs):
  strn = "CREATE TABLE IF NOT EXISTS {0}({1} integer primary key autoincrement {2})".format(tablename,PKname,FKargs)
  sql3_exec(DBname,strn)
  print('In database {0}, table {1} has succesfully been created with primary key {2}'.format(DBname,
        tablename,PKname))

#Executes writing commands to DB. To return data from DB, use sql3_grab(), defined below
def sql3_exec(DBname,strn):
  dirname = os.path.dirname(__file__)
  conn = sqlite3.connect(dirname+file_struct.DB_rel_location+DBname)
  c = conn.cursor()
  c.execute('PRAGMA foreign_keys = ON;')
  #print('Executing SQL Command: {}'.format(strn)) #Turn this on for explict printing of all DB write commands
  c.execute(strn)
  conn.commit()
  c.close()
  conn.close()

#Executes reading commands to DB. Cannot currently be used to return data from DB
def sql3_grab(DBname,strn):
  dirname = os.path.dirname(__file__)
  conn = sqlite3.connect(dirname+file_struct.DB_rel_location+DBname)
  c = conn.cursor()
  #print('Executing SQL Command: {}'.format(strn)) #Turn this on for explict printing of all DB write commands
  c.execute(strn)
  #print(c.fetchall())
  try:
    return_item = c.fetchall()[0][0]#Get value from list of tuples. There should be a cleaner way to do this (maybe don't return a list of tuples from c.fetchall)
  #Also note that return_item will only give the first item in a list of possibly many items.
  except:
    print('There appears to be no records in DB {0}, exiting'.format(DBname))
  c.close()
  conn.close()
  return return_item
