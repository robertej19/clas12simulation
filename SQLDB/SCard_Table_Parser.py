from parser import *
import sqlite3

#Need to put genexecutable in somewhere

conn = sqlite3.connect('CLAS12_OCRDB.db')
c = conn.cursor()

def grab_condor_data():
    c.execute('SELECT Project, Jobs, Cores_Req, Mem_Req FROM Scards')
    nevents = list(c.fetchall())
    return nevents

def grab_runscript_data():
    c.execute("""SELECT Group_name, User, Nevents,Generator,
              GenOptions, Gcards, Tcurrent, Pcurrent FROM Scards""")
    dba = list(c.fetchall())
    return dba


condor_new_vals = grab_condor_data()[-1] #For now, just grab the most recent entry in the database
runscript = grab_runscript_data()[-1] #For now, just grab the most recent entry in the database

group = runscript[0]
user = runscript[1]
nevents = str(runscript[2])
genExecutable = runscript[3]
genOptions = runscript[4]
genOutput = 'sidis.dat'
gcards = runscript[5]
tcurrent = str(runscript[6])
pcurrent = str(runscript[7])
runscript = runscript + ('sidis.dat',)

condor_overwrite_vals=('project_scard','jobs_scard','cores_req_scard','mem_req_scard')
write_clas12_condor("clas12.condor.template",condor_overwrite_vals,condor_new_vals)
#overwrite runscript.sh
rs_overwrite_vals = ('group_scard','user_scard','genExecutable_scard','nevents_scard',
                    'genOptions_scard','genOutput_scard','gcards_scard','tcurrent_scard',
                    'pcurrent_scard')
write_runscript_sh("runscript.sh.template",rs_overwrite_vals,runscript)
