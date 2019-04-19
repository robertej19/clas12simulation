def file_mover(scard):
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
  echo "notsouseful started at" $notsouseful_start"""
  return strn
