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
DBname = 'CLAS12_OCRDB.db'
DB_rel_location = "/../../database/" #This will get changed when moving to SQL RDBMS
DB_rel_location_src = "/../database/" #This is needed for db_user_entry, should be removed later
tables = ['Users','Batches','Scards','Gcards','Submissions','JobsLog']

#Primary Key definitions:
PKs = ['UserID','BatchID','ScardID','GcardID','SubmissionID','JobID']

users_fields = (('Email','TEXT'),('JoinDateStamp','INT'),('Total_Batches','INT'),
                ('Total_Jobs','INT'),('Total_Events','INT'),('Most_Recent_Active_Date','INT'))

runscript_field = 'runscript' #This is a crutch until a better and more general data structure is established
condor_field = 'condor_script' #This is a crutch until a better and more general data structure is established
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
                      ('condor_script_name','TEXT'),(condor_field,'VARCHAR'))

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
"""*****************************************************************************
---------------------------- Other Specifications ------------------------------
*****************************************************************************"""

#This specifies a folder where all submission files live (runscripts, gcards,etc)
sub_files_rel_location = "/../submission_files/"
gcards_dir = 'gcards/'
condor_dir = 'condor_files/'
runscript_dir = 'runscript_files/'


import os
dirname = os.path.dirname(__file__)
if dirname == '': dirname = '.' #Need this because if running in this file's directory, dirname is blank
db_path = dirname+DB_rel_location_src+DBname
sub_files_path = dirname+'/..'+sub_files_rel_location

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


# This defines a mapping between 'generator' in scard and the genOutput and genExecutable literals to be invoked
genOutput= {'clasdis': 'sidis.dat', 'dvcs': 'dvcs.dat','disrad':'dis-rad.dat'}
genExecutable =  {'clasdis': 'clasdis', 'dvcs': 'dvcsgen','disrad':'generate-dis'}
