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
cat runscript_gcard_1_batch_1.sh
echo "-------------"
echo "-------------"

./condor_wrapper /tmp/runscript_gcard_1_batch_1.sh