import sqlite3, file_struct, utils

#Grab write values
con_old, con_new = utils.grab_DB_data('CLAS12_OCRDB.db','Scards',file_struct.SCTable_CondOverwrite)
rs_old, rs_new = utils.grab_DB_data('CLAS12_OCRDB.db','Scards',file_struct.SCTable_RSOverwrite)

#Write from template files out to submission files
utils.overwrite_file("clas12.condor.template",con_old,con_new)
utils.overwrite_file("runscript.sh.template",rs_old,rs_new)
