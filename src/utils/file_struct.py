# This file is the central location for this software information. It includes:
# - database schema, including:
#        - database name
#        - tables & table fields
#        - primary and foreign keys
# - scard and running scripts specifications, including:
#        - all fields that are necessary and sufficient to define a valid scard
#        - all values that will be overwritten in creating run scripts
# - other specifications, including:
#      - mapping between scard generator keyword and genOutput & genExecutable


"""*****************************************************************************
-------------------------  DB Schema Specification -----------------------------
*****************************************************************************"""
tables = ['Users','Batches','Scards','Gcards','Submissions','JobsLog']

#Primary Key definitions:
PKs = ['UserID','BatchID','ScardID','GcardID','SubmissionID','JobID']

users_fields = (('Email','TEXT'),('JoinDateStamp','INT'),('Total_Batches','INT'),
                ('Total_Jobs','INT'),('Total_Events','INT'),('Most_Recent_Active_Date','INT'))

runscript_field = 'runscript' #This is a crutch until a better and more general data structure is established
condor_field = 'condor_script' #This is a crutch until a better and more general data structure is established
run_job_field = 'run_job_script'
cw_field = 'condor_wrapper_script'

batches_fields = (('timestamp','FLOAT'),('scard','VARCHAR'))

#Since there is only 1 scard / batch, in princple this entire scard table should be deleted
#The submission scripts can be completely written using just the text in the VARCHAR 'scard' field in the Batches table
#Importantly, this is not yet implemented. It should be straightforward to do so, but time consuming
scards_fields = (('group_name','TEXT'),('Nevents','INT'),
                ('Generator','TEXT'),('genExecutable','TEXT'),('genOutput','TEXT'),
                ('GenOptions','TEXT'),('Gcards','TEXT'),('Jobs','INT'),
                ('Project','TEXT'),('Luminosity','INT'),('Tcurrent','INT'),('Pcurrent','INT'),
                ('Cores_Req','INT'),('Mem_Req','INT'),('timestamp','FLOAT'))

gcards_fields = (('gcard_text','VARCHAR'),)

submissions_fields = (('submission_pool','TEXT'),#submission pool is not yet used
                      ('runscript_name','TEXT'),(runscript_field,'VARCHAR'),
                      ('condor_script_name','TEXT'),(condor_field,'VARCHAR'),
                      ('run_job_name','TEXT'),(run_job_field,'VARCHAR'),
                      ('cw_name','TEXT'),(cw_field,'VARCHAR'))

joblogs_fields = (('Job_Submission_Datestamp','INT'),
                  ('Job_Completion_Datestamp','TEXT'),('Output_file_directory','TEXT'),
                  ('Output_file_size','INT'),('Number_Job_failures','INT'))

table_fields = [users_fields,batches_fields, scards_fields, gcards_fields, submissions_fields, joblogs_fields]

#Below defines foreign key relations. There is a more succinet way to do this but as we have
#only a few relations, I did not spend the time to modifiy this code.
users_special_relations = """, User TEXT NOT NULL UNIQUE"""
batches_foreign_keys = """, User TEXT,
                      FOREIGN KEY(User) REFERENCES Users(User)"""
scards_foreign_keys = """, User TEXT, BatchID INTEGER,
                      FOREIGN KEY(User) REFERENCES Users(User)
                      FOREIGN KEY(BatchID) REFERENCES Batches(BatchID)"""
gcards_foreign_keys = """, BatchID INTEGER,
                      FOREIGN KEY(BatchID) REFERENCES Batches(BatchID)"""
submissions_foreign_keys = """, BatchID INTEGER, GcardID INTEGER,
                      FOREIGN KEY(BatchID) REFERENCES Batches(BatchID)
                      FOREIGN KEY(GcardID) REFERENCES Gcards(GcardID)"""
joblogs_foreign_keys = """, UserID INTEGER, BatchID INTEGER, SubmissionID INTEGER,
                      FOREIGN KEY(UserID) REFERENCES Users(UserID)
                      FOREIGN KEY(BatchID) REFERENCES Batches(BatchID)
                      FOREIGN KEY(SubmissionID) REFERENCES Submissions(SubmissionID)"""
#create table yourtablename (_id  integer primary key autoincrement, column1 text not null unique, column2 text);

foreign_key_relations = [users_special_relations, batches_foreign_keys,
                        scards_foreign_keys, gcards_foreign_keys,
                        submissions_foreign_keys, joblogs_foreign_keys]
"""*****************************************************************************
-------------------- Scard and Runscripts Specifications -----------------------
*****************************************************************************"""
#This defines the ordering and items that need to be in scard.txt
scard_key = ('group','user','nevents','generator',
            'genOptions',  'gcards', 'jobs',  'project',
            'luminosity', 'tcurrent',  'pcurrent','cores_req','mem_req')

#This defines the variables that will be written out to submission scripts and maps to DB values
SCTable_CondOverwrite = {'project_scard':'project','jobs_scard':'jobs',
                          'cores_req_scard':'cores_req','mem_req_scard':'mem_req','nevents_scard': 'nevents'}

SCTable_RSOverwrite = {'gcards_scard': 'gcards', 'genOutput_scard': 'genOutput',
                        'user_scard': 'user','nevents_scard': 'nevents',
                        'pcurrent_scard': 'pcurrent', 'tcurrent_scard': 'tcurrent',
                        'genOptions_scard': 'genOptions', 'genExecutable_scard': 'genExecutable',
                        'LUMIOPTION_scard':'luminosity','group_scard': 'group_name'}

SCTable_RunJobOverwrite = {'runscript.overwrite': 'rs_overwrite_unused'}

SCTable_CWOverwrite = {'gcards_scard': 'gcards'} #This is unused currently

"""*****************************************************************************
------------------------- File Path Specifications -----------------------------
*****************************************************************************"""
"""Current path specifications are as follows: (only important files & dirs included)
clas12simulation(s)
  scard.txt
  database
    CLAS12_OCRDB.db
  submission_files
    condor_files
    condor_wrapper_files
    gcards
    run_job_files
    runscript_files
  src
     db_batch_entry.py
     db_user_entry.py
     sub_script_generator.py
     templates
        *.template
     utils
        create_database.py
        file_struct.py **** this file, all locations are referenced relative to this
        gcard_helper.py
        scard_helper.py
        utils.py
"""
#Specifiy Database name:
DBname = 'CLAS12_OCRDB.db'
#Specify scard name
scard_name = 'scard.txt'
#Specify the directory names of all submission files
gcards_dir = 'gcards/'
condor_dir = 'condor_files/'
runscript_dir = 'runscript_files/'
run_job_dir = 'run_job_files/'
cw_dir = 'condor_wrapper_files/' #This is not currently used / needed, but included for completenents

import os #I would like to do this part differently, but dont have the time to do this right now.
#I would like to remove dirname entirely, and have everything run relatively, but right now this works.
dirname = os.path.dirname(__file__)

#Specify the location of where all submission files live (runscripts, gcards,etc)
sub_files_path = dirname+'/../../submission_files/'
#Specify the location of all template files
template_files_path = dirname + "/../templates/"
#Specify the location of the DB relative to here (This will get changed when moving to SQL RDBMS)
DB_path = dirname+"/../../database/"
DB_path_src = dirname+"/../../database/"
#Specify the location of the scard
scard_path = dirname+"/../../"

"""*****************************************************************************
------------------------ Submission File Specifications ------------------------
*****************************************************************************"""

class sub_file():
  def __init__(self,name):
    self.name = name
    self.file_path = 0
    self.filebase = 0
    self.file_end = 0
    self.overwrite_vals = 0
    self.field_loc = 0
    self.script_name = 0

runscript_file_obj = sub_file('runscript')
runscript_file_obj.file_path = sub_files_path+runscript_dir
runscript_file_obj.filebase = 'runscript'
runscript_file_obj.file_end = '.sh'
runscript_file_obj.overwrite_vals = SCTable_RSOverwrite
runscript_file_obj.field_loc = runscript_field
runscript_file_obj.script_name = 'runscript_name'

condor_file_obj = sub_file('clas12_condor')
condor_file_obj.file_path = sub_files_path+condor_dir
condor_file_obj.filebase = 'clas12'
condor_file_obj.file_end = '.condor'
condor_file_obj.overwrite_vals = SCTable_CondOverwrite
condor_file_obj.field_loc = condor_field
condor_file_obj.script_name = 'condor_script_name'

run_job_obj = sub_file('run_job')
run_job_obj.file_path = sub_files_path+run_job_dir
run_job_obj.filebase = 'run_job'
run_job_obj.file_end = '.sh'
run_job_obj.overwrite_vals = SCTable_RunJobOverwrite
run_job_obj.field_loc = run_job_field
run_job_obj.script_name = 'run_job_name'

cw_obj = sub_file('condor_wrapper')
cw_obj.file_path = sub_files_path+cw_dir
cw_obj.filebase = 'condor_wrapper'
cw_obj.file_end = ''
cw_obj.overwrite_vals = SCTable_CWOverwrite
cw_obj.field_loc = cw_field
cw_obj.script_name = 'cw_name'

"""*****************************************************************************
---------------------------- Other Specifications ------------------------------
*****************************************************************************"""

# This defines a mapping between 'generator' in scard and the genOutput and genExecutable literals to be invoked
genOutput= {'clasdis': 'sidis.dat', 'dvcs': 'dvcs.dat','disrad':'dis-rad.dat'}
genExecutable =  {'clasdis': 'clasdis', 'dvcs': 'dvcsgen','disrad':'generate-dis'}

#This is for creating a default user in the database
default_user = 'mungaro'
default_email = 'mungaro@example.com'
