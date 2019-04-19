from __future__ import print_function
import subprocess, os
#import new_script_generator

#print(dir(new_script_generator))
#from script_generators import *
from script_generators import startup, initialization
#import script_generators
from inspect import getmembers, isfunction
#from my_project import my_module

#functions_list = [o for o in getmembers(my_module) if isfunction(o[0])]

funcs = (startup,initialization)
fname = ('startup','initialization')
#for f in funcs:
##  print(f.f())
#print(funcs[0].)
i = 0
for f in funcs:
#USE ENUMERATE HERE!
  result = getattr(f,fname[i])()
  print(result)
  i = i + 1
#print(result)
#print(initialization.initialization())
#for
#print(getmembers(my_module))
#for my_module in script_generators:
#  print(dir(my_module))
"""user_scard = 'bobby'
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

funcs = [startup(),
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
"""
