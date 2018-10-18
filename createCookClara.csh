#!/bin/csh -f

# two mandatory arguments
# 1 input file
# 2 output directory
# optional argument is number of threads

if($#argv != 2 && $#argv != 3) then
	echo " "
	echo "Usage:   "
	echo  "  >> createCookClara <inputfile.hipo> <output dir> [nthreads]"
	echo " "
	exit 0
endif

set inputF = $1
set oDir  = $2

echo "set files $inputF"    >  cook.clara
echo "set outputDir $oDir" >> cook.clara
if($3 != "") then
	echo "set threads $3"   >> cook.clara
endif
echo "run local"           >> cook.clara
echo "exit"                >> cook.clara


