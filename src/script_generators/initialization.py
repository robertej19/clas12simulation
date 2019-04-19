def initialization():
  strn = """printf "Start time: "; /bin/date
  printf "Job is running on node: "; /bin/hostname
  printf "Job running as user: "; /usr/bin/id
  printf "Job is running in directory: "; /bin/pwd\n
  echo
  echo JLAB_ROOT: $JLAB_ROOT
  echo\n
  echo starting files
  ls -l
  set generator_start  = `date`
  {0} --trig {1} --docker {2}
  echo after generator""".format('scard.genExecutable','scard.nevents','scard.genOption')
  return strn
