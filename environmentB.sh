#!/bin/bash

export JLAB_ROOT=/jlab
export JLAB_VERSION=2.3
export CLAS12TAG=4a.2.5
export JRE=jre1.8.0_191

# sidis, inclusive dis with rad correction, dvcs
export CLASDIS_PDF=/jlab/work/clasdis-nocernlib/pdf
export DISRAD_PDF=/jlab/work/inclusive-dis-rad
export CLASDVCS_PDF=/jlab/work/dvcsgen

export GEMC=/jlab/clas12Tags/$CLAS12TAG/source
export GEMC_VERSION=$CLAS12TAG

source $JLAB_ROOT/$JLAB_VERSION/ce/jlab.sh keepmine
export GEMC_DATA_DIR=/jlab/clas12Tags/$CLAS12TAG

# CLAS12 Reconstruction
export CLAS12_LIB=$JLAB_SOFTWARE/clas12/lib
export CLAS12_INC=$JLAB_SOFTWARE/clas12/inc
export CLAS12_BIN=$JLAB_SOFTWARE/clas12/bin

export GEOMDBVAR=may_2018_engineers
export COATJAVA=$JLAB_SOFTWARE/clas12/coatjava
export JAVA_HOME=$JLAB_SOFTWARE/$JRE

export PATH=${JAVA_HOME}/bin:${PATH}:${CLAS12_BIN}:${COATJAVA}/bin

set autolist
alias l='ls -l'
alias lt='ls -lt'

