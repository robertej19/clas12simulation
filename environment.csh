#!/bin/csh

setenv JLAB_ROOT /jlab
setenv JLAB_VERSION 2.3
setenv CLAS12TAG 4a.2.5

setenv GEMC /jlab/clas12Tags/$CLAS12TAG/source
setenv GEMC_VERSION $CLAS12TAG

source $JLAB_ROOT/$JLAB_VERSION/ce/jlab.csh keepmine
setenv GEMC_DATA_DIR /jlab/clas12Tags/$CLAS12TAG

# CLAS12 Reconstruction
setenv CLAS12_LIB $JLAB_SOFTWARE/clas12/lib
setenv CLAS12_INC $JLAB_SOFTWARE/clas12/inc
setenv CLAS12_BIN $JLAB_SOFTWARE/clas12/bin

setenv CLARA_HOME $JLAB_ROOT/$JLAB_VERSION/claraHome
setenv COATJAVA   $CLARA_HOME/plugins/clas12

setenv PATH ${PATH}:${CLAS12_BIN}:${COATJAVA}/bin:${CLARA_HOME}/bin

set autolist
alias l ls -l
alias lt ls -lt

