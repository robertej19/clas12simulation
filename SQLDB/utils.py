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

def add_field(tablename,field_name,field_type):
      conn = sqlite3.connect('CLAS12_OCRDB.db')
      c = conn.cursor()
      c.execute('ALTER TABLE %s ADD COLUMN %s %s' % (tablename,field_name, field_type))
      c.close()
      conn.close()
