#!/bin/csh -f
# two mandatory arguments
# 1 input file
# 2 number of threads

if($#argv != 2) then
	echo " "
	echo "Usage:   "
	echo  "  >> createClaraCook <inputfilename> <nthreads>"
	echo " "
	exit 0
endif

set inputF = $1
set nthrea = $2


# file is stored in a files.txt
rm -f files.txt ; echo $inputF > files.txt

rm -f cook.clara
echo "set fileList files.txt"   > cook.clara
echo "set inputDir ."          >> cook.clara
echo "set outputDir ."         >> cook.clara
echo "set threads "$nthrea     >> cook.clara
echo "set logDir log"          >> cook.clara
echo "run local"               >> cook.clara
echo "exit"                    >> cook.clara
mkdir -p log
cat cook.clara
