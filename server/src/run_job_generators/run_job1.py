#****************************************************************
"""
# Commentary for this file does not yet exist
"""
#****************************************************************

def run_job1(scard,**kwargs):
  strn = """#!/bin/bash

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
cat {0}
echo "-------------"
echo "-------------"

./condor_wrapper /tmp{0}""".format(kwargs['runscript_filename'])
  return strn
