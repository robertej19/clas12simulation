#--------------------------------------------------------------------------
# docker image for CLAS12 Production Simulation.
#
# This Dockerfile includes the clas12tags gemc container for
# the CLAS12TAG below (current production)
#
# It relies on the gemcbatch:2.7 base image that has the necessary
# libraries to run gemc in batch mode.
# gemcbatch:2.7 has JLAB_VERSION set to 2.3
#
# Remember to find/replace gemcBatch with the newest one
#
# Remember to match clas12tags and JLAB_VERSION in environment.csh
#
# The docker image is automatically built on hub.docker for every new commit (push) of the Dockerfile.
# To build manually:
#
#   docker build -f Dockerfile -t clas12simulations:production .
#
#   docker tag clas12simulations:latest maureeungaro/clas12simulations:production
#
#   docker push maureeungaro/clas12simulations:production
#
#--------------------------------------------------------------------------
#
# To run in batch mode:
#
#  docker run -it --rm maureeungaro/clas12simulations:production bash
#
# On a mac, if you allow access from localhost with:
#
#  1. Activate the option ‘Allow connections from network clients’ in XQuartz settings (Restart XQuartz (to activate the setting)
#  2. xhost +127.0.0.1
#
# Then you can run docker and use the local X server with:
#
#  docker run -it --rm -e DISPLAY=docker.for.mac.localhost:0 maureeungaro/clas12simulations:production bash
#--------------------------------------------------------------------------

FROM jeffersonlab/gemcbatch:2.7
LABEL maintainer "Maurizio Ungaro <ungaro@jlab.org>"


# Add java support
RUN yum install -y \
	java-1.8.0-openjdk

ENV JLAB_ROOT /jlab
ENV JLAB_VERSION 2.3
ENV CLAS12TAG 4a.2.5
ENV COATJTAG 5c.6.9

WORKDIR $JLAB_ROOT

# Removing un-used tags and .git stuff
# Removing default version of temc
# Replacing the scripts in /etc and with the environment scripts
# Checking out clas12Tags and compiling CLAS12TAG
# Putting clas12 gcard in $JLAB_ROOT/work
# Getting the field maps
# $JLAB_ROOT/work is an existing directory
RUN git clone https://github.com/gemc/clas12Tags.git \
	&& cd $JLAB_ROOT/clas12Tags \
	&& rm -rf .git* `ls | grep -v goIns | grep -v $CLAS12TAG | grep -v env | grep -v REA` \
	&& source $JLAB_ROOT/$JLAB_VERSION/ce/jlab.sh \
	&& rm -rf $JLAB_ROOT/$JLAB_VERSION/$OSRELEASE/gemc \
	&& ./goInstall $CLAS12TAG \
	&& cp $JLAB_ROOT/clas12Tags/$CLAS12TAG/clas12.gcard $JLAB_ROOT/work \
	&& mkdir -p /jlab/noarch/data \
	&& cd /jlab/noarch/data \
	&& wget -q http://clasweb.jlab.org/12gev/field_maps/TorusSymmetric.dat \
	&& wget -q http://clasweb.jlab.org/12gev/field_maps/clas12NewSolenoidFieldMap.dat \
	&& rm /etc/profile.d/jlab.csh \
	&& rm /etc/profile.d/jlab.sh \
	# reconstruction, clara and coatjava
	&& mkdir -p $JLAB_SOFTWARE/clas12/lib \
	&& mkdir -p $JLAB_SOFTWARE/clas12/bin \
	&& mkdir -p $JLAB_SOFTWARE/clas12/inc \
	&& export CLARA_HOME=$JLAB_ROOT/$JLAB_VERSION/claraHome \
	&& mkdir -p $CLARA_HOME /jlab/tmp \
	&& cd /jlab/tmp \
	&& wget  --no-check-certificate https://claraweb.jlab.org/clara/_downloads/install-claracre-clas.sh \
	&& chmod u+x install-claracre-clas.sh \
	&& ./install-claracre-clas.sh -v $COATJTAG \
	&& cd /jlab \
	&& rm -rf tmp



WORKDIR $JLAB_ROOT/work
ADD environment.csh /etc/profile.d
ADD environment.sh /etc/profile.d

WORKDIR $JLAB_ROOT/work
