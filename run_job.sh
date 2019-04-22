#!/bin/bash

echo "XXX"
echo "XXX"
pwd;
echo "XXX"
echo "XXX"
ls -l;


echo "-------------"
echo "-------------"
cat condor_wrapper
echo "-------------"
echo "-------------"
cat condor_exec.exe
echo "-------------"
echo "-------------"
cat runscript.sh
echo "-------------"
echo "-------------"

#runscript=`cat /mnt/c/Users/Bobby/Dropbox/Linux/clas12_submit/clas12simulation/src/utils/../../submission_files/runscript_files/runscript_gcard_10_batch_4.sh`

./condor_wrapper /tmp/runscript.sh
