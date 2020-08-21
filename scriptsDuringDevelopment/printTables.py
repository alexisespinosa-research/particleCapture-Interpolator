import numpy as np
import csv

#The capture efficiency function
def ceff(RE,rp):
    eta=0.224*(RE**0.718)*(rp**2.08)
    return eta

#The rp's to ask
rps=np.arange(0.0,0.01,0.001,dtype=float)
print(rps,rps.shape)

#The Re's to ask
REs=np.array([100,200,300,400,500,600,700,800,900,1000],dtype=float,ndmin=1)
print(REs,REs.shape)

#Directory to save the tables
tablesDir="../captureDB/testDB"
dbFilePrefix="eta=(rp,RE="

#Generating the tables
for REi in REs:
    fileName=tablesDir+"/"+dbFilePrefix+str(REi)+").csv"
    myData=np.empty((rps.size,2),dtype=float)
    print(myData,myData.shape,myData.size)
    for row in range(0,rps.size):        
        myData[row][0]=rps[row]
        myData[row][1]=ceff(REi,rps[row])
        print(myData[row][:])
    myFile = open(fileName, 'w')
    with myFile:
        writer = csv.writer(myFile)
        writer.writerows(myData)

