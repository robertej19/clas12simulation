# SQLite DB Schema
See https://dbdiagram.io/d/5c9b829bf7c5bb70c72f6c34

# scard.txt

The first row 'project' was changed to 'group' because there is one more project at scard. If scard is in different format, parser.py will print ERROR and halt.

# Submit_Job.py
Executing `python src/Submit_Job.py` from the main directory will run all core functions, this can be used for testing purposes. Run `python src/Submit_Job.py -h` to see options that can be passed. Importantly, -d 1 will turn on some debugging messages, and -d 2 will turn on all debugging messages. 
 
# clas12.condor
condor_submit clas12.condor will submit a job.

# run_job.sh
an executable called by clas12.condor. It will call condor_wrapper.

# condor_wrapper
a script called by run_job.sh. It will call runscript.sh

# runscript.sh
This is a main script which calls generator, GEMC, decoder, and reconstruction. submit.py will update runscript.sh regarding scard.txt

# Generator Option

To see genOptions, please look at followings:<br />
SIDIS: https://github.com/JeffersonLab/clasdis-nocernlib/blob/master/README.md<br />
DVCS: https://github.com/JeffersonLab/dvcsgen/blob/master/README.md<br />
DIS-RAD: https://github.com/JeffersonLab/inclusive-dis-rad/blob/master/README.md

# condorHelp
Quickstart: https://support.opensciencegrid.org/support/solutions/articles/5000633410-osg-connect-quickstart


To submit a job:
----------------

condor_submit condorTemplate.submit


Troubleshooting:

 condor_q -better-analyze JOBID


History:
--------

condor_history mauri

for details:

condor_history -long mauri

condor_q - Lists the jobs in the queue. Can be invoked with your username:

condor_q mauri



https://support.opensciencegrid.org/support/solutions/articles/5000623439-osg-xsede-user-guide


Guidelines for data management: https://support.opensciencegrid.org/support/solutions/articles/12000006512-guidelines-for-data-managment-in-osg-storage-and-transfer<br />
OSG Helpdesk: https://support.opensciencegrid.org/support/home

HTCondor: https://research.cs.wisc.edu/htcondor/index.html

Condor Documentation: https://research.cs.wisc.edu/htcondor/manual/


To run the singularity container:

singularity shell --home ${PWD}:/srv --pwd /srv --bind /cvmfs --contain --ipc --pid /cvmfs/singularity.opensciencegrid.org/maureeungaro/clas12simulations:production


Managing Jobs:
-------------

On hold:

condor_q  -hold

Removing a job (by ID)

condor_rm ID

# clas12 Simulations Software Distribution


This repo contains the dockerfile used to build the production version of the CLAS12 simulation + reconstruction packages. It contains:


- the production version of the [gemc clas12tag](https://github.com/gemc/clas12Tags)
- the production version of the [reconstruction software](https://github.com/JeffersonLab/clas12-offline-software)

This repo is linked to the hub.docker.com repo: [maureeungaro/clas12simulations](https://hub.docker.com/u/maureeungaro/)
Any changes to Dockerfile will trigger a new docker image creation.

## Open Source Grid

Any changes to the docker image in the hub.docker.com repository will trigger the creation of the singularity image within about one hour.

The image is loaded in:

```/cvmfs/singularity.opensciencegrid.org/maureeungaro/```

