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

#runscript=`cat runscript.sh`

./condor_wrapper /tmp/runscript.sh
