# Sample of read from database
import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect('TimeLog.db')
c = conn.cursor()

def grab_data():
    c.execute('SELECT initialization, generation, gemc, evio2hipo, reconstruction, total FROM JobLog')
    dba = list(c.fetchall())
    return dba

comps = ['initialization', 'generation', 'gemc', 'evio2hipo', 'reconstruction', 'total']
sv = grab_data()

#print " number of events: {0} \n number of jobs: {1}".format(scard_values[1],scard_values[2])


for i in range(0,49):
  y = sv[i]
  print(y)
  z = tuple([x/3600 for x in y])
  w=[z[0]]
  for i in range(1,len(z)):
    w.append(z[i]+w[i-1])
  #for j in range(0,len(y)):
  #  y[j] = y[j]/3600
  plt.plot(comps, w)
plt.show()
