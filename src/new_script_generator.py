from __future__ import print_function
import subprocess, os
from script_generators import startup,initialization,run_gemc,run_evio2hipo,run_cooking,file_mover


funcs = (startup,initialization,run_gemc,run_evio2hipo,run_cooking,file_mover)
fname = ('startup','initialization','run_gemc','run_evio2hipo','run_cooking','file_mover')

class sdx:
  def __init__(self):
    self.name = 'Bobby'

scard = sdx

newfile = "runscript.sh"
if os.path.isfile(newfile):
  subprocess.call(['rm',newfile])
for count, f in enumerate(funcs):
  generated_text = getattr(f,fname[count])(scard)
  with open(newfile,"a") as file: file.write(generated_text)
