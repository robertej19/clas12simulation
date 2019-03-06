#!/bin/csh

set script_start  = `date`

echo " ==== PWD"
pwd

echo " ==== ./"
ls -lhrt ./

echo " ==== /etc/profile.d/"
ls -lhrt /etc/profile.d/

echo " ==== ENV"
env

set ClusterId = ` awk -F '=' '/^ClusterId/ {print $2}' $PWD/.job.ad`
echo ClusterId $ClusterId


set ProcId = ` awk -F '=' '/^ProcId/ {print $2}' $PWD/.job.ad`
echo ProcId $ProcId

mkdir out_dir$ClusterId


# initial job log
printf "Start time: "; /bin/date
printf "Job is running on node: "; /bin/hostname
printf "Job running as user: "; /usr/bin/id
printf "Job is running in directory: "; /bin/pwd


echo
echo JLAB_ROOT: $JLAB_ROOT
echo

echo starting files
ls -l
set generator_start  = `date`
clasdis --trig 10 --docker --t 20 25
#dvcsgen --trig 71 --docker

echo after generator
echo test finish
ls -l
set gemc_start = `date`
gemc -USE_GUI=0 -N=10 -INPUT_GEN_FILE="lund, sidis.dat"  /jlab/work/clas12.gcard

echo after gemc
ls -l


set evio2hipo_start = `date`
evio2hipo -r 11 -t -1.0 -s -1.0 -i out.ev -o gemc.hipo

echo after decoder
ls -l

set notsouseful_start = `date`
notsouseful-util -i gemc.hipo -o out_gemc.hipo -c 2

echo after cooking
ls -l


echo Moving file
echo $ClusterId
mv gemc.hipo gemc.$ProcId.hipo
echo File moved
echo `basename gemc.$ProcId.hipo`

echo creating directory
mkdir out_dir$ClusterId
echo moving file
mv gemc.$ProcId.hipo out_dir$ClusterId
mv out_gemc.hipo out_gemc.10.clasdis.$ProcId.hipo
mv out_gemc.10.clasdis.$ProcId.hipo out_dir$ClusterId

#clearing log files
rm -f gemc.log
rm -f e2h.log

#final job log
printf "Job finished time: "; /bin/date

echo "script started at" $script_start
echo "generator started at" $generator_start
echo "gemc started at" $gemc_start
echo "evio2hipo started at" $evio2hipo_start
echo "notsouseful started at" $notsouseful_start
