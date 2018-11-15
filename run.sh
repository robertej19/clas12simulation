#!/bin/csh

# initial job log

printf "Start time: "; /bin/date
printf "Job is running on node: "; /bin/hostname
printf "Job running as user: "; /usr/bin/id
printf "Job is running in directory: "; /bin/pwd

echo starting files
ls -l

# Generators
# Readmes at:
#
# https://github.com/JeffersonLab/clasdis-nocernlib/blob/master/README.md
# https://github.com/JeffersonLab/dvcsgen/blob/master/README.md
# https://github.com/JeffersonLab/inclusive-dis-rad/blob/master/README.md

clasdis --trig 10000 --docker      # sidis.dat
generate-dis --trig 10000 --docker # dis-rad.dat
dvcsgen --trig 10000 --docker      # dvcs.dat


# using official gcard
rm -f gemc.log
gemc -USE_GUI=0 -N=1000 -BEAM_P="e-, 4*GeV, 20*deg, 5*deg"  /jlab/work/clas12.gcard > gemc.log # internal generator
gemc -USE_GUI=0 -N=1000 -INPUT_GEN_FILE="LUND, sidis.dat"   /jlab/work/clas12.gcard > gemc.log # clasdis
gemc -USE_GUI=0 -N=1000 -INPUT_GEN_FILE="LUND, dis-rad.dat" /jlab/work/clas12.gcard > gemc.log # dis with radiative correction
gemc -USE_GUI=0 -N=1000 -INPUT_GEN_FILE="LUND, dvcs.dat"    /jlab/work/clas12.gcard > gemc.log # clasdvcs

echo after gemc
ls -l
echo



rm -f e2h.log
evio2hipo -r 11 -t -1.0 -s -1.0 -i out.ev -o gemc.hipo > e2h.log

echo after evio2hipo
ls -l
echo


# re-establish the runClara.sh with the stuff below
# argument is n threads

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
cat cook.clara

mkdir -p log
rm -f reco.log
clara-shell cook.clara > reco.log


echo after cooking
ls -l
echo


# final job log
printf "Job finished time: "; /bin/date

