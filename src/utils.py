from __future__ import print_function
import file_struct, sqlite3

#Takes in a .template file, a list of values to replace (old_vals) and a list of what to replace them with (new_vals)
def overwrite_file(template_file,old_vals,new_vals): #template_file = str, old_vals, new_vals = LIST
    with open(template_file,"r") as tmp: str_script = tmp.read()
    newfile = str(template_file)[:-9]#This removes the '.template' ending
    for i in range(0,len(old_vals)):
      str_script = str_script.replace(old_vals[i],str(new_vals[i]))
    print("Overwriting '{0}'".format(newfile))
    with open(newfile,"w") as file: file.write(str_script)
    print("Done.\n")

#Takes a dictionary, retuns 2 lists: key (oldvals) and value (newvals) from table in DBName
def grab_DB_data(DBname,table,dictionary): #DBName, table = str, dictionary = dict
    conn = sqlite3.connect(DBname)
    c = conn.cursor()
    oldvals, newvals = [],[]
    for key in dictionary:
      strn = "SELECT {0} FROM {1} ORDER BY BatchID DESC LIMIT 1;".format(dictionary[key],table)#This just grabs the most recent DB entry.
      c.execute(strn)
      oldvals.append(key)
      try:
        value = c.fetchall()[0][0]#Get value from list of tuples. There should be a cleaner way to do this (maybe don't return a list of tuples from c.fetchall)
      except:
        print('There appears to be no records in the table {0} in DB {1}, exiting'.format(table,DBname))
        return [], [], 1
      newvals.append(value)
    return oldvals, newvals, 0

#Add a field to an existing DB. Need to add error statements if DB or table does not exist
def add_field(DBname,tablename,field_name,field_type):
  strn = "ALTER TABLE {0} ADD COLUMN {1} {2}".format(tablename,field_name, field_type)
  sql3_exec(DBname,strn)
  print('In database {0}, table {1} has succesfully added field {2}'.format(DBname,tablename,field_name))

#Create a table in a database
def create_table(DBname,tablename,PKname):
  strn = "CREATE TABLE IF NOT EXISTS {0}({1} integer primary key autoincrement)".format(tablename,PKname)
  sql3_exec(DBname,strn)
  print('In database {0}, table {1} has succesfully been created with primary key {2}'.format(DBname,
        tablename,PKname))

#Executes writing commands to DB. Cannot currently be used to return data from DB
def sql3_exec(DBname,strn):
  conn = sqlite3.connect(DBname)
  c = conn.cursor()
  c.execute(strn)
  #print('Executed SQL Command: {}'.format(strn)) #Turn this on for explict printing of all DB write commands
  conn.commit()
  c.close()
  conn.close()
