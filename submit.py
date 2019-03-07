#!/usr/bin/env python
from parser import *

# define program's arguments
argparser = argparse.ArgumentParser()
argparser.add_argument('steering_card', default='scard.txt', help='file name of scard')
argparser.add_argument('key', nargs='?', default=None, help='each column item name. If called, print correspinding item\'s value. If omitted, s')
argparser.add_argument('-s', '--submit', help= 'submit.',action="store_true")
args = argparser.parse_args()

# rename variables for human-readability
filename = args.steering_card
specific_key = args.key

# Collecting info from scard
# If scard is not in a proper format, the class scard_parser should stop the script.
scard = scard_parser(filename) # parse scard. scard is called only once at this line.
data_scard = scard.data # This is dictionary which has every data from scard.
group = scard.group  # Alternatively, they can be called in single name.
user = scard.user
nevents = scard.nevents
generator = scard.generator
genOptions = scard.genOptions
gcards = scard.gcards
jobs = scard.jobs
project = scard.project
luminosity =  '%1.2f'(124000 * float(scard.luminosity))
if float(scard.luminosity) == 0:
    print "Warning: luminosity is 0. GEMC will run with 100% luminosity."
    luminosity = 124000
tcurrent = '%1.2f'%(float(scard.tcurrent)/100.)
if float(scard.tcurrent)%10==0:
    tcurrent = '%1.1f'%(float(scard.tcurrent)/100.)
pcurrent = '%1.2f'%(float(scard.pcurrent)/100.)
if float(scard.pcurrent)%10==0:
    pcurrent = '%1.1f'%(float(scard.pcurrent)/100.)
genOutput = scard.genOutput
genExecutable = scard.genExecutable

hostname = socket.gethostname()
if hostname == "submit.mit.edu":
    # str_script=str_script.replace("(GLIDEIN_Site == \"MIT_CampusFactory\" && BOSCOGroup == \"bosco_lns\") ","HAS_SINGULARITY == TRUE")
    #give executable permission
    subprocess.call(["cp",parser_path+"/run_job.sh","."])
    os.chmod("run_job.sh", 0775)
    subprocess.call(["cp",parser_path+"/condor_wrapper","."])
    os.chmod("condor_wrapper", 0775)
    # overwrite clas12.condor
    write_clas12_condor(project,jobs)
    #overwrite runscript.sh
    write_runscript_sh(group,user,genExecutable, nevents, genOptions, genOutput, gcards, luminosity, tcurrent, pcurrent)
elif hostname == "scosg16.jlab.org":
    write_clas12_osg_condor(project,jobs)
    write_runscript_osg_sh(group,user,genExecutable, nevents, genOptions, genOutput, gcards, luminosity, tcurrent, pcurrent)
else:
    # str_script=str_script.replace("(GLIDEIN_Site == \"MIT_CampusFactory\" && BOSCOGroup == \"bosco_lns\") ","HAS_SINGULARITY == TRUE")
    #give executable permission
    os.chmod("run_job.sh", 0775)
    os.chmod("condor_wrapper", 0775)
    # overwrite clas12.condor
    write_clas12_condor(project,jobs)
    #overwrite runscript.sh
    write_runscript_sh(group,user,genExecutable, nevents, genOptions, genOutput, gcards, tcurrent, pcurrent)
print "Event generator"
print genExecutable+" --trig " +nevents +" --docker "+ genOptions
print "\nGEMC"
print "gemc -USE_GUI=0 -N="+nevents+" -INPUT_GEN_FILE=\"lund, "+genOutput+"\" "+  gcards
print "\nDecoder"
print "evio2hipo -r 11 -t " +tcurrent+" -s "+ pcurrent+" -i out.ev -o gemc.hipo"
print "\nCooking"
print "notsouseful-util -i gemc.hipo -o out_gemc.hipo -c 2"
#if submit flag turned on, submit
if args.submit:
    #make log directory
    subprocess.call(["mkdir","-p","log"])
    if hostname == "submit.mit.edu":
        condor_submit()
    elif hostname == "scosg16.jlab.org":
        condor_osg_submit()
    else:
        print "You are not on any pool. Please ssh into farms. If you are not authorized, please contact maurizio at ungaro@jlab.org"
#if not, print some messages
else:
    print "The scripts \'clas12.condor\' and \'runscript.sh\' are updated based on \'"+filename+".\'"
    print "Please turn on -s flag for job submission e.g.) python submit.py -s scard.txt\n"
