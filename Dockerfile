#--------------------------------------------------------------------------
# docker image for CLAS12 Production Simulation.
#
# This Dockerfile includes the clas12tags gemc container for
# - clas12tags: 4a.2.4 (current production)
#
# It relies on the gemcbatch:2.7 base image that has the necessary libraries to run gemc
# in batch mode. gemcbatch:2.7 has JLAB_VERSION set to 2.3
#
# Remember to find/replace gemcBatch with the newest one
#
# Remember to match clas12tags and JLAB_VERSION in environment.csh
#
# The docker image is automatically built on hub.docker for every new commit (push) of the Dockerfile.
# To build manually:
#
#   docker build -f Dockerfile -t clas12simproduction:latest .
#
#   docker tag clas12simproduction:latest maureeungaro/clas12simproduction:latest
#
#   docker push maureeungaro/clas12simproduction:latest
#
#--------------------------------------------------------------------------
#
# To run in batch mode:
#
#  docker run -it --rm maureeungaro/clas12simproduction:latest bash
#
#--------------------------------------------------------------------------

FROM jeffersonlab/gemcbatch:2.7
LABEL maintainer "Maurizio Ungaro <ungaro@jlab.org>"

ENV JLAB_ROOT /jlab
ENV JLAB_VERSION 2.3
ENV CLAS12TAG 4a.2.5

WORKDIR $JLAB_ROOT

# Removing un-used tags and .git stuff
# Replacing the scripts in /etc and with the environment scripts
# Checking out clas12Tags and compiling CLAS12TAG
# Putting clas12 gcard in $JLAB_ROOT/work
# Getting the field maps
# $JLAB_ROOT/work is an existing directory
RUN git clone https://github.com/gemc/clas12Tags.git \
	&& cd $JLAB_ROOT/clas12Tags \
	&& rm -rf .git* `ls | grep -v goIns | grep -v $CLAS12TAG | grep -v env | grep -v REA` \
	&& source $JLAB_ROOT/$JLAB_VERSION/ce/jlab.sh \
	&& ./goInstall $CLAS12TAG \
	&& cp $JLAB_ROOT/clas12Tags/$CLAS12TAG/clas12.gcard $JLAB_ROOT/work \
	&& mkdir -p /jlab/noarch/data \
	&& cd /jlab/noarch/data \
	&& wget -q http://clasweb.jlab.org/12gev/field_maps/TorusSymmetric.dat \
	&& wget -q http://clasweb.jlab.org/12gev/field_maps/clas12NewSolenoidFieldMap.dat \
	&& rm /etc/profile.d/jlab.csh \
	&& rm /etc/profile.d/jlab.sh


WORKDIR $JLAB_ROOT/work
ADD environment.csh /etc/profile.d
ADD environment.sh /etc/profile.d

WORKDIR $JLAB_ROOT/work
