def startup(user_scard,group_scard):

  strn1 = """set ClusterId = ` awk -F '=' '/^ClusterId/ {print $2}' $PWD/.job.ad`"""
  strn2 = """set ProcId = ` awk -F '=' '/^ProcId/ {print $2}' $PWD/.job.ad`"""

  strn = """#!/bin/csh \n
  set script_start  = `date`\n
  # source /cvmfs/cms.cern.ch/cmsset_default.csh \n
  echo "XXXXXXXXXXXX"
  #cat $PWD/.job.ad
  echo "XXXXXXXXXXXX"
  echo Submitted by {0}, {1}
    uname -a \n
    echo " ==== PWD"
    pwd \n
    echo " ==== ./"
    ls -lhrt ./ \n
    echo " ==== /etc/profile.d/"
    ls -lhrt /etc/profile.d/ \n
    echo " ==== ENV"
    env \n
    source /etc/profile.d/environmentB.csh
    cd /tmp \n
    #set ClusterId = `sed -n '0,/ClusterId = "\([^"]*\)"/\1/p' $PWD/.job.ad` \n
    {2}
    echo ClusterId $ClusterId \n\n
    {3}
    echo ProcId $ProcId""".format(user_scard,group_scard,strn1,strn2)
  return strn


def initialization(genExecutable_scard,nevents_scard,genOptions_scard):
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
  echo after generator""".format(genExecutable_scard,nevents_scard,genOptions_scard)
  return strn

def run_gemc(nevents_scard,genOutput_scard,LUMIOPTION_scard,gcards_gcard):
  strn = """ls -l
  set gemc_start = `date`
  gemc -USE_GUI=0 -N={0} -INPUT_GEN_FILE="lund, {1}"{2} {3}
  echo after gemc""".format(nevents_scard,genOutput_scard,LUMIOPTION_scard,gcards_gcard)
  return strn

def run_evio2hipo(tcurrent_scard,pcurrent_scard):
  strn = """ls -l
  set evio2hipo_start = `date`
  evio2hipo -r 11 -t {0} -s {1} -i out.ev -o gemc.hipo
  echo after decoder""".format(tcurrent_scard,pcurrent_scard)
  return strn

def run_cooking():
  strn = """ls -l
  set notsouseful_start = `date`
  notsouseful-util -i gemc.hipo -o out_gemc.hipo -c 2
  echo after cooking"""
  return strn

def move_files():
  strn = """ls -l \n
  echo Moving file
  echo $ClusterId
  mv out.ev out.$ProcId.ev
  mv gemc.hipo gemc.$ProcId.hipo
  mv genOutput_scard genOutput_scard.$ProcId
  echo File moved
  echo `basename genOutput_scard.$ProcId`
  echo `basename out.$ProcId.ev`
  echo `basename gemc.$ProcId.hipo`
  echo `basename out_gemc.$ProcId.hipo` \n \n
  echo creating directory
  mkdir out_`basename $ClusterId`_nnevents_scard
  echo moving file
  mv genOutput_scard.$ProcId out_`basename $ClusterId`_nnevents_scard
  mv out.$ProcId.ev out_`basename $ClusterId`_nnevents_scard
  mv gemc.$ProcId.hipo out_`basename $ClusterId`_nnevents_scard
  mv out_gemc.hipo out_gemc.$ProcId.hipo
  mv out_gemc.$ProcId.hipo out_`basename $ClusterId`_nnevents_scard

  echo copying gcard and scard
  cp gcards_scard out_`basename $ClusterId`_nnevents_scard
  cp scard_name out_`basename $ClusterId`_nnevents_scard

  #final job log
  printf "Job finished time: "; /bin/date

  echo "script started at" $script_start
  echo "generator started at" $generator_start
  echo "gemc started at" $gemc_start
  echo "evio2hipo started at" $evio2hipo_start
  echo "notsouseful started at" $notsouseful_start""".format()
  return strn

if __name__ == "__main__":
  print(startup('bobby','MIT'))
