from __future__ import print_function
import file_struct, sqlite3

#Takes in a .template file, a list of values to replace (old_vals) and a list of what to replace them with (new_vals)
def overwrite_file(template_file,old_vals,new_vals): #template_file = str, old_vals, new_vals = LIST
    with open(template_file,"r") as tmp: str_script = tmp.read()
    newfile = str(template_file)[:-9]#This removes the '.template' ending
    for i in range(0,len(old_vals)):
      str_script = str_script.replace(old_vals[i],str(new_vals[i]))
    print("Overwriting '{}'".format(newfile))
    with open(newfile,"w") as file: file.write(str_script)
    print("Done.\n")

#Takes a dictionary, retuns 2 lists: key (oldvals) and value (newvals) from table in DBName
def grab_DB_data(DBName,table,dictionary): #DBName, table = str, dictionary = dict
    conn = sqlite3.connect(DBName)
    c = conn.cursor()
    oldvals, newvals = [],[]
    for key in dictionary:
      strn = "SELECT {} FROM {};".format(dictionary[key],table)
      c.execute(strn)
      oldvals.append(key)
      newvals.append((c.fetchall()[-1])[0]) #This [-1] just grabs the most recent DB entry. The [0] is because it returns a tuple
    return oldvals, newvals

def add_field(DBname,tablename,field_name,field_type):
  strn = "ALTER TABLE {} ADD COLUMN {} {}".format(tablename,field_name, field_type)
  sql3_exec(DBname,strn)
  print('In database {}, table {} has succesfully added field {}'.format(DBname,tablename,field_name))

def create_table(DBname,tablename,PKname):
  strn = "CREATE TABLE IF NOT EXISTS {}({} integer primary key autoincrement)".format(tablename,PKname)
  sql3_exec(DBname,strn)
  print('In database {}, table {} has succesfully been created with primary key {}'.format(DBname,
        tablename,PKname))

def sql3_exec(DBname,strn):
  conn = sqlite3.connect(DBname)
  c = conn.cursor()
  c.execute(strn)
  c.close()
  conn.close()
