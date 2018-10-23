#!/bin/csh

# initial job log
printf "Start time: "; /bin/date
printf "Job is running on node: "; /bin/hostname
printf "Job running as user: "; /usr/bin/id
printf "Job is running in directory: "; /bin/pwd


pwd

ls -l
ls -l /jlab
ls -l /jlab/work

which gemc

gemc -help-all


gemc clas12.gcard -N=100 -PRINT_EVENT=10 -USE_GUI=0


# final job log
printf "Job finished time: "; /bin/date
