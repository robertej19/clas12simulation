#!/bin/bash

export JLAB_ROOT=/jlab
export JLAB_VERSION=2.3
export CLAS12TAG=4a.2.5
export JRE=jre1.8.0_191

# SIDIS
export CLASDIS_PDF=/jlab/work/clasdis-nocernlib/pdf

export GEMC=/jlab/clas12Tags/$CLAS12TAG/source
export GEMC_VERSION=$CLAS12TAG

source $JLAB_ROOT/$JLAB_VERSION/ce/jlab.sh keepmine
export GEMC_DATA_DIR=/jlab/clas12Tags/$CLAS12TAG

# CLAS12 Reconstruction
export CLAS12_LIB=$JLAB_SOFTWARE/clas12/lib
export CLAS12_INC=$JLAB_SOFTWARE/clas12/inc
export CLAS12_BIN=$JLAB_SOFTWARE/clas12/bin

export COATJAVA=$JLAB_SOFTWARE/clas12/coatjava
export JAVA_HOME=$JLAB_SOFTWARE/$JRE

export PATH=${PATH}:${CLAS12_BIN}:${COATJAVA}/bin:${JAVA_HOME}/bin

set autolist
alias l='ls -l'
alias lt='ls -lt'

