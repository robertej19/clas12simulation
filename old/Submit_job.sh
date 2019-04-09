#!/bin/bash

#Currently, this must be run in the "clas12simulation[s]" directory!

clear

if [ ! -f scard.txt ]; then
	printf "scard.txt not found, please create before attempting to continue. Exiting"
	exit
fi

if [ ! -f database/CLAS12_OCRDB.db ]; then
	printf "\n\n CLAS12 Off Campus Resources Database not found, creating! \n\n"
	python2 src/utils/create_database.py
	printf "\n\n Creating example user [needed for testing purposes] \n\n"
	python2 src/db_user_entry.py
fi

printf "\n\n Reading scard & other information into database \n\n"
python2 src/db_batch_entry.py

#rm scard.txt

printf "\n\n Writing submission scripts  \n\n"
python2 src/sub_script_generator.py


#chmod +x runscript.sh

#condor_submit clas12.condor
