#!/bin/bash

if [ ! -f scard.txt ]; then
	echo "scard.txt not found, please create before attempting to continue. Exiting"
	exit
fi
cp scard.txt src/

cd src
ls

if [ ! -f CLAS12_OCRDB.db ]; then
	echo "CLAS12 Off Campus Resources Database not found, creating!"
	python2 make_DB.py
fi

python2 Users_Table_Writer.py

echo "Reading scard into database"
python2 SCard_Table_Writer.py

rm scard.txt

echo "Writing Scard information to submission scripts"
python2 SCard_Table_Parser.py


cd ../

mv src/runscript.sh .
mv src/clas12.condor .

chmod +x runscript.sh

condor_submit clas12.condor
