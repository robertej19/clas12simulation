#!/bin/csh

# initial job log

printf "Start time: "; /bin/date
printf "Job is running on node: "; /bin/hostname
printf "Job running as user: "; /usr/bin/id
printf "Job is running in directory: "; /bin/pwd


gemc -help-all


# final job log
printf "Job finished time: "; /bin/date
