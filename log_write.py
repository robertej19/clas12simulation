from timeparser import *

import sqlite3

conn = sqlite3.connect('TimeLog.db')
c = conn.cursor()

def dynamic_data_entry(jobnumber,timearray):
    ta = timearray
    c.execute("INSERT INTO JobLog(jobnumber, initialization, generation, gemc, evio2hipo, reconstruction, total) VALUES (?,?,?,?,?,?,?)",
              (jobnumber,ta[0],ta[1],ta[2],ta[3],ta[4],ta[5]))
    conn.commit()
    print("Record added to DB from "+jobnumber)
    c.close()
    conn.close()

def write_record(jobnumber):
  dynamic_data_entry(jobnumber,parse_times(jobnumber)) #technically this writes the job.jobnumber.out to the record, but oh well. Will fix later.
