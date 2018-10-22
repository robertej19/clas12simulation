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


