# Sample of read from database
import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect('TimeLog.db')
c = conn.cursor()

def grab_color():
    c.execute('SELECT nevents FROM JobLog')
    nevents = list(c.fetchall())
    return nevents

def grab_data():
    c.execute('SELECT initialization, generation, gemc, evio2hipo, reconstruction FROM JobLog')
    dba = list(c.fetchall())
    return dba

comps = ['initialization', 'generation', 'gemc', 'evio2hipo', 'reconstruction','completion']
sv = grab_data()
colorbook = grab_color()
#print " number of events: {0} \n number of jobs: {1}".format(scard_values[1],scard_values[2])

colors = ['k','r','b']
colornum = [1000,2000,4000]

init4=[]
gen4 = []
gemc4 = []
evio4 = []
recon4 = []
init2=[]
gen2 = []
gemc2 = []
evio2 = []
recon2 = []
init1=[]
gen1 = []
gemc1 = []
evio1 = []
recon1 = []
for i in range(0,49):
  if colorbook[i][0] == 1000:
    init1.append(sv[i][0])
    gen1.append(sv[i][1])
    gemc1.append(sv[i][2])
    evio1.append(sv[i][3])
    recon1.append(sv[i][4])
  elif colorbook[i][0] == 2000:
    init2.append(sv[i][0])
    gen2.append(sv[i][1])
    gemc2.append(sv[i][2])
    evio2.append(sv[i][3])
    recon2.append(sv[i][4])
  elif colorbook[i][0] == 4000:
    init4.append(sv[i][0])
    gen4.append(sv[i][1])
    gemc4.append(sv[i][2])
    evio4.append(sv[i][3])
    recon4.append(sv[i][4])
  y = (0,)+sv[i]
  line_color = colors[colornum.index(colorbook[i][0])]
  print(y)
  z = tuple([x/3600 for x in y])
  w=[z[0]]
  for i in range(1,len(z)):
    w.append(z[i]+w[i-1])
  #for j in range(0,len(y)):
  #  y[j] = y[j]/3600
  plt.plot(comps, w, color = line_color)
plt.title('Processing Time for Simulation Runs', fontsize=24)
plt.ylabel("Real Time (Hours)", fontsize=22)
#plt.xlabel("Computation Process", fontsize=18)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
#plt.legend(loc="best")
plt.tight_layout()
plt.show()

def avs(array):
  ave = sum(array)/len(array)
  return ave

labels = comps[:-1]

a = avs(init4)
b = avs(gen4)
c = avs(gemc4)
d = avs(evio4)
e = avs(recon4)

sizes = [a,b,c,d,e]
colors = ['black','gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
explode = (0.1,0.1,0,0.1,0)  # explode 1st slice

# Plot
#plt.pie(sizes, explode=explode, labels=labels, colors=colors,
#autopct='%1.1f%%', shadow=True, startangle=140)
plt.pie(sizes, explode=explode,colors=colors, startangle=90)

plt.axis('equal')
plt.show()

print('SIZEES')
for i in range(0,len(sizes)):
  print(sizes[i]/sum(sizes)*100)
sizes1 = [0,a,b,c,d,e]


plt.plot(comps, sizes1, color = 'b')
plt.title('Processing Time for Simulation Runs', fontsize=24)
plt.ylabel("Real Time (Hours)", fontsize=22)
#plt.xlabel("Computation Process", fontsize=18)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
#plt.legend(loc="best")
plt.tight_layout()
plt.show()
