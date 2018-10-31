#!/bin/csh -f

# This script creates a cook.clara script and run clara-shell with it
# The output file is hardcoded to be gemc.hipo

# file is stored in a files.txt
rm -f files.txt ; echo gemc.hipo > files.txt

rm -f cook.clara
echo "set fileList files.txt"   > cook.clara
echo "set inputDir ."          >> cook.clara
echo "set outputDir ."         >> cook.clara
echo "set threads 1"           >> cook.clara
echo "set logDir log"          >> cook.clara
echo "run local"               >> cook.clara
echo "exit"                    >> cook.clara

mkdir -p log
clara-shell cook.clara

