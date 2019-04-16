#!/bin/csh 

  set script_start  = `date`

  # source /cvmfs/cms.cern.ch/cmsset_default.csh 

  echo "XXXXXXXXXXXX"
  #cat $PWD/.job.ad
  echo "XXXXXXXXXXXX"
  echo Submitted by bobby, test1
    uname -a 

    echo " ==== PWD"
    pwd 

    echo " ==== ./"
    ls -lhrt ./ 

    echo " ==== /etc/profile.d/"
    ls -lhrt /etc/profile.d/ 

    echo " ==== ENV"
    env 

    source /etc/profile.d/environmentB.csh
    cd /tmp 

    #set ClusterId = `sed -n '0,/ClusterId = "\([^"]*\)"//p' $PWD/.job.ad` 

    set ClusterId = ` awk -F '=' '/^ClusterId/ {print $2}' $PWD/.job.ad`
    echo ClusterId $ClusterId 


    set ProcId = ` awk -F '=' '/^ProcId/ {print $2}' $PWD/.job.ad`
    echo ProcId $ProcIdprintf "Start time: "; /bin/date
  printf "Job is running on node: "; /bin/hostname
  printf "Job running as user: "; /usr/bin/id
  printf "Job is running in directory: "; /bin/pwd

  echo
  echo JLAB_ROOT: $JLAB_ROOT
  echo

  echo starting files
  ls -l
  set generator_start  = `date`
  test2 --trig test5 --docker test4
  echo after generatorls -l
  set gemc_start = `date`
  gemc -USE_GUI=0 -N=test5 -INPUT_GEN_FILE="lund, test6"test7 test8
  echo after gemcls -l
  set evio2hipo_start = `date`
  evio2hipo -r 11 -t test9 -s test0 -i out.ev -o gemc.hipo
  echo after decoderls -l
  set notsouseful_start = `date`
  notsouseful-util -i gemc.hipo -o out_gemc.hipo -c 2
  echo after cookingls -l 

  echo Moving file
  echo $ClusterId
  mv out.ev out.$ProcId.ev
  mv gemc.hipo gemc.$ProcId.hipo
  mv genOutput_scard genOutput_scard.$ProcId
  echo File moved
  echo `basename genOutput_scard.$ProcId`
  echo `basename out.$ProcId.ev`
  echo `basename gemc.$ProcId.hipo`
  echo `basename out_gemc.$ProcId.hipo` 
 

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
  echo "notsouseful started at" $notsouseful_start