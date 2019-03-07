import argparse, sys, os, subprocess, socket

# declare a global dictionary to match genOutput and genExecutable to generator row
genOutput= {'clasdis': 'sidis.dat', 'dvcs': 'dvcs.dat','disrad':'dis-rad.dat'}
genExecutable =  {'clasdis': 'clasdis', 'dvcs': 'dvcsgen','disrad':'generate-dis'}

# Proper configuration of scard:
scard_key = ['group','user','nevents','generator', 'genOptions',  'gcards', 'jobs',  'project', 'luminosity', 'tcurrent',  'pcurrent']

# from https://codegolf.stackexchange.com/questions/4707/outputting-ordinal-numbers-1st-2nd-3rd#answer-4712
def ordinal(n):
    return "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])

class scard_parser:
# Default Constructor: a = scard_parser();  a.parse_scard("scard.txt")
# Parametrized Constructor:  a = scard_parser("scard.txt")
    def __init__(self, scard_filename=None):
        self.type ='scard parser'
        self.data = {}
        if scard_filename != None:
            self.parse_scard(scard_filename)

# void function for saving line into a dictionary
    def parse_scard_line(self, linenum, line):
        self.validate_scard_line(linenum, line) # 1st validating
        pos_delimeter_colon = line.find(":")
        pos_delimeter_hash = line.find("#")
        key =   line[:pos_delimeter_colon].strip()
        value=  line[pos_delimeter_colon+1:pos_delimeter_hash].strip()
        if key != scard_key[linenum]:
            print "ERROR: The " + ordinal(linenum+1) +" line of steering card starts with "+ key +"."
            print "That line must have the key " + scard_key[linenum] +"."
        self.data[key] = value

# void function for parsing scard.txt into a dictionary
    def parse_scard(self, filename, store=True):
        scard=open(filename, "r")
        for linenum, line in enumerate(scard):
            self.parse_scard_line(linenum,line)
        if store == True:
            self.store()

#void function for validating s_card
    def validate_scard_line(self, linenum, line):
        if line.count("#") ==0:
            print "Warning: No comment in "+ ordinal(linenum+1) + " line."
        elif line.count("#")>1:
            print "ERROR: number of hashes>1 at "+ordinal(linenum+1)+" line."
            print "# can be only used for a delimeter and for once. Stopped."
            exit()
        if line.count(":") ==0:
            print "ERROR: No colon in "+ ordinal(linenum+1) + " line."
            print "The data cannot be interpreted. Stopped."
            exit()
        elif line.count(":")>1:
            print "ERROR: number of colons>1 at "+ordinal(linenum+1)+" line."
            print "\':\' can be only used for a delimeter and for once. Stopped."
            exit()

def replacer(filename,old,new):
  filename = filename.replace(old,new)
  return filename

def write_clas12_condor(template_file,condor_old_vals,condor_new_vals):
    with open(template_file,"r") as tmp: str_script = tmp.read()
    for i in range(0,len(condor_old_vals)):
      str_script = replacer(str_script,condor_old_vals[i],str(condor_new_vals[i]))
    hostname = socket.gethostname()
    if hostname == "scosg16.jlab.org":
        str_script=str_script.replace("(GLIDEIN_Site == \"MIT_CampusFactory\" && BOSCOGroup == \"bosco_lns\") ","HAS_SINGULARITY == TRUE")
    print "overwrite \'clas12.condor\' in current directory ..."
    with open("clas12.condor","w") as file: file.write(str_script)
    print "Done.\n"

def write_runscript_sh(template_file,rs_old_vals,rs_new_vals):
    with open(template_file,"r") as tmp: str_script = tmp.read()
    for i in range(0,len(rs_old_vals)):
      str_script = replacer(str_script,rs_old_vals[i],str(rs_new_vals[i]))
    print "overwrite \'runscript.sh\' in current directory ..."
    with open("runscript.sh","w") as file: file.write(str_script)
    os.chmod("runscript.sh", 0775)
    print "Done.\n"

def condor_submit():
    print "submitting jobs from python script...\n"
    subprocess.call(["condor_submit","clas12.condor"])
