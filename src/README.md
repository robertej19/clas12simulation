- The database and scard structure is described in the file "file_struct.py". Changes to lists in this file will alter the 
database structure upon rerunning of the python scripts.

- to create a database, execute:
python2 make_DB.py


- to add users to the database, execute:
python2 Users_Table_Writer.py

This currently just creates an example user, with entries specified directly in the "Users_Table_Writer.py" file
Note that this step is currently OPTIONAL as foreign key relations are NOT yet enforced

- to add an scard record to the database, execute:
python2 SCard_Table_Writer.py

This will read in an "scard.txt" file, which must be located in the same directory as SCard_Table_Writer.py, as currently configured.

- to create submission scripts (currently just runscript.sh and clas12.condor), execute:
python2 SCard_Table_Parser.py

This will grab the runscript.sh.template and clas12.condor.template files found in the templates/ directory,
write in them as specified by the scard, and move the submission scripts to the src/ directory.

- to submit a job:
Follow the above commands to create submission files. Then copy / move the submission files to the main directory (the directory above /src)
Then execute:
condor_submit clas12.condor
