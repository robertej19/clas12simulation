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

tables = ['Users','Batches','Scards','JobsLog']

users_fields = (('Username','TEXT'),('Affiliation','TEXT'),('JoinDateStamp','INT'),
                ('Permissions','TEXT'),('Default_Output_Dir','TEXT'),('Total_Batches','INT'),
                ('Total_Jobs','INT'),('Total_Events','INT'),('Most_Recent_Active_Date','INT'))

runscript_field = 'runscript' #This is a crutch until a better and more general data structure is established
condor_field = 'condor_script' #This is a crutch until a better and more general data structure is established
batches_fields = (('timestamp','FLOAT'),('scard','VARCHAR'),('submission_pool','TEXT'),#submission pool is not yet used
                  (runscript_field,'VARCHAR'),(condor_field,'VARCHAR'))

scards_fields = (('group_name','TEXT'),('User','TEXT'),('Nevents','INT'),
                ('Generator','TEXT'),('genExecutable','TEXT'),('genOutput','TEXT'),
                ('GenOptions','TEXT'),('Gcards','TEXT'),('Jobs','INT'),
                ('Project','TEXT'),('Luminosity','INT'),('Tcurrent','INT'),('Pcurrent','INT'),
                ('Cores_Req','INT'),('Mem_Req','INT'),('timestamp','FLOAT'))

jobslog_fields = (('Job_Submission_Datestamp','INT'),
                  ('Job_Completion_Datestamp','TEXT'),('Output_file_directory','TEXT'),
                  ('Output_file_size','INT'),('Number_Job_failures','INT'))

#Primary Key definitions:
PKs = ['UserID','BatchID','ScardID','JobID']

#Below defines foreign key relations. There is a more succinet way to do this but as we have
#only a few relations, I did not spend the time to modifiy this code.
users_foreign_keys = ''
batches_foreign_keys = """, UserID INTEGER,
                      FOREIGN KEY(UserID) REFERENCES Users(UserID)"""
scards_foreign_keys = """, UserID INTEGER, BatchID INTEGER,
                      FOREIGN KEY(UserID) REFERENCES Users(UserID)
                      FOREIGN KEY(BatchID) REFERENCES Batches(BatchID)"""
logs_foreign_keys = """, BatchID TEXT, UserID TEXT,
                    FOREIGN KEY(BatchID) REFERENCES Batches(BatchID)
                    FOREIGN KEY(UserID) REFERENCES Users(UserID)"""

foreign_key_relations = [users_foreign_keys, batches_foreign_keys, scards_foreign_keys, logs_foreign_keys]
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
                        'group_scard': 'group_name'}
"""*****************************************************************************
---------------------------- Other Specifications ------------------------------
*****************************************************************************"""
# This defines a mapping between 'generator' in scard and the genOutput and genExecutable literals to be invoked
genOutput= {'clasdis': 'sidis.dat', 'dvcs': 'dvcs.dat','disrad':'dis-rad.dat'}
genExecutable =  {'clasdis': 'clasdis', 'dvcs': 'dvcsgen','disrad':'generate-dis'}
