#!/bin/csh -f

if($#argv != 1) then
	echo " "
	echo "Usage:   "
	echo  "  >> csh submit.csh steeringcard.txt"
	echo " "
	exit 0
endif


set cdir = `pwd`
set pdir = /group/clas12/clas12simulations

set file = $cdir/$1

rm -f run.sh ; touch run.sh ; chmod u+x run.sh
mkdir -p log

# start log
cat $pdir/startLog >> run.sh

set nevents = `python $pdir/parser.py $file nevents:`

# generator
set generator    = `python $pdir/parser.py $file genExecutable`
set genOptions   = `python $pdir/parser.py $file genOptions:`
set allGenOption = `echo "--trig "$nevents" --docker "$genOptions`
set genOutput    = `python $pdir/parser.py $file genOutput`

echo
echo Generator command: $generator $allGenOption" with output:"$genOutput

echo                          >> run.sh
echo $generator $allGenOption >> run.sh
echo                          >> run.sh
echo echo after generator     >> run.sh
echo ls -l                    >> run.sh

# gemc
set gcard  = `python $pdir/parser.py $file gcards:`

echo
echo GEMC command: "gemc -USE_GUI=0 -N="$nevents -INPUT_GEN_FILE=\"lund, $genOutput\""with output: " out.ev
echo
echo "Decoder output: " gemc.hipo
echo
echo "Reconstruction output: " out_gemc.hipo
echo

echo                 >> run.sh
echo "gemc -USE_GUI=0 -N="$nevents -INPUT_GEN_FILE=\"lund, $genOutput\" " "$gcard >> run.sh
echo                 >> run.sh
echo echo after gemc >> run.sh
echo ls -l           >> run.sh

# decoder
echo                    >> run.sh
echo "evio2hipo -r 11 -t -1.0 -s -1.0 -i out.ev -o gemc.hipo"  >> run.sh
echo                    >> run.sh
echo echo after decoder >> run.sh
echo ls -l              >> run.sh

# reconstruction
echo                    >> run.sh
echo "notsouseful-util -i gemc.hipo -o out_gemc.hipo -c 2"  >> run.sh
echo                    >> run.sh
echo echo after cooking >> run.sh
echo ls -l              >> run.sh
echo                    >> run.sh


# end log
cat $pdir/endLog >> run.sh

# now submitting job
condor_submit /group/clas12/clas12simulations/clas12.condor


