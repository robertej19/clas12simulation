#!/bin/bash

#Currently, this must be run in the "clas12simulation[s]" directory!

if [ ! -f scard.txt ]; then
	echo "scard.txt not found, please create before attempting to continue. Exiting"
	exit
fi

if [ ! -f database/CLAS12_OCRDB.db ]; then
	echo "CLAS12 Off Campus Resources Database not found, creating!"
	python2 src/utils/create_database.py
fi

echo "Creating example user [needed for testing purposes]"
python2 src/db_user_entry.py

#echo "Reading scard & other information into database"
#python2 src/db_batch_entry.py

#rm scard.txt

#echo "\n\nWriting submission scripts"
#python2 sub_script_generator.py


#mv src/runscript.sh .
#mv src/clas12.condor .

#chmod +x runscript.sh

#condor_submit clas12.condor
