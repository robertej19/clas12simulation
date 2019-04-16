from __future__ import print_function
import subprocess, os
#import new_script_generator

#print(dir(new_script_generator))
from new_script_generator import *

user_scard = 'bobby'
group_scard = 'test1'
genExecutable_scard = 'test2'
nevents_scard = 'test3'
genOptions_scard = 'test4'
nevents_scard = 'test5'
genOutput_scard = 'test6'
LUMIOPTION_scard = 'test7'
gcards_gcard = 'test8'
tcurrent_scard = 'test9'
pcurrent_scard  = 'test0'

funcs = [startup(user_scard,group_scard),
initialization(genExecutable_scard,nevents_scard,genOptions_scard),
run_gemc(nevents_scard,genOutput_scard,LUMIOPTION_scard,gcards_gcard),
run_evio2hipo(tcurrent_scard,pcurrent_scard),
run_cooking(),
move_files()]

newfile = "test_runscript.sh"
if os.path.isfile(newfile):
  subprocess.call(['rm',newfile])
for function in funcs:
  with open(newfile,"a") as file: file.write(function)
