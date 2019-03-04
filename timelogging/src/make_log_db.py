import sqlite3

conn = sqlite3.connect('TimeLog.db')
c = conn.cursor()

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS JobLog(jobID integer primary key autoincrement,jobnumber TEXT, initialization INT,generation INT,gemc INT,evio2hipo INT,reconstruction INT,total INT)')

create_table()

c.close()
conn.close()
