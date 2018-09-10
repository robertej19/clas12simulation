#--------------------------------------------------------------------------
# docker image for CLAS12 Production Simulation.
#
# This Dockerfile describes the clas12tags gemc containers for
# - JLAB_VERSION 2.2
# - clas12tags: 4a.2.4 (current production)
#
# It relies on the jlabce base image for CLHEP, GEANT4, and ROOT as well as several system
# packages. This is based on David Lawrence docker builds in https://gitlab.com/ESC/containers.git
#
# This will create a docker image that includes both a noVNC-webserver
# and VNC-server that can be used to view graphics on the host using
# either a native webrowser (HTML5 enabled) or a native VNC viewer. This
# includes the ability to view OpenGL graphics.
#
# Remember to find/replace the <tag> and JLAB_VERSION with the newest one
#
# Remember to match clas12tags and JLAB_VERSION in environment.csh
#
# The docker image is automatically built on hub.docker for every new commit (push) of the Dockerfile.
# To build manually:
#
#   docker build -f Dockerfile -t clas12simproduction
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

FROM jeffersonlab/jlabce:2.2
LABEL maintainer "Maurizio Ungaro <ungaro@jlab.org>"

ENV JLAB_ROOT /jlab
ENV JLAB_VERSION 2.2
ENV CLAS12TAG 4a.2.4

WORKDIR $JLAB_ROOT

# Notice: we need a symbolic link to the mlibrary include as it was missing.
# Should not be needed in 2.3 and up (we also need to fix it there)
# Also notice: the TorusSymmetric.dat field is downloaded manually. It will be downloaded with go_field in the installation
# Removing un-used tags and .git stuff as well
RUN git clone https://github.com/gemc/clas12Tags.git \
	&& source $JLAB_ROOT/$JLAB_VERSION/ce/jlab.sh \
	&& cd $MLIBRARY \
	&& mkdir -p cadmesh \
	&& cd cadmesh \
	&& ln -s ../include . \
	&& cd $JLAB_ROOT/clas12Tags \
	&& rm -rf .git* `ls | grep -v goIns | grep -v $CLAS12TAG | grep -v env | grep -v REA` \
	&& cp $GEMC/physics/PhysicsList.cc $CLAS12TAG/source/physics/ \
	&& ./goInstall $CLAS12TAG \
	&& rm /etc/profile.d/jlab.csh \
	&& rm /etc/profile.d/jlab.sh \
	&& mkdir $JLAB_ROOT/workdir \
	&& cp $JLAB_ROOT/clas12Tags/$CLAS12TAG/clas12.gcard $JLAB_ROOT/workdir \
	&& cd /jlab/noarch/data \
	&& rm clas12TorusOriginalMap.dat \
	&& wget -q http://clasweb.jlab.org/12gev/field_maps/TorusSymmetric.dat \
	&& wget -q http://clasweb.jlab.org/12gev/field_maps/clas12NewSolenoidFieldMap.dat \
	&& rm /jlab/noarch/data/clas12SolenoidFieldMap.dat

WORKDIR $JLAB_ROOT/workdir
ADD environment.csh /etc/profile.d
ADD environment.sh /etc/profile.d

# The jlab.sh in 2.2 is not working properly. Installing the latest one instead
ADD jlab.sh /jlab/2.2/ce
