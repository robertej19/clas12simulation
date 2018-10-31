#!/bin/csh

# initial job log

printf "Start time: "; /bin/date
printf "Job is running on node: "; /bin/hostname
printf "Job running as user: "; /usr/bin/id
printf "Job is running in directory: "; /bin/pwd


echo starting files
ls -l

gemc -USE_GUI=0 -N=1000 -BEAM_P="e-, 4*GeV, 20*deg, 5*deg" clas12.gcard

echo after gemc
ls -l

evio2hipo -r 11 -t -1.0 -s -1.0 -i out.ev -o gemc.hipo

echo after evio2hipo
ls -l

cook.csh

cat cook.clara

echo after cooking
ls -l


# final job log
printf "Job finished time: "; /bin/date

