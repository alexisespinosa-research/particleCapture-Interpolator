import numpy as np
import glob,re

#Identifying the path of this script in order to find the databases
import inspect
import os
packagePath = os.path.dirname(inspect.stack()[0][1])


#Defining Data Base Directories
testDBDir=packagePath + "/pyCaptureDBData/testDB"
rho1DBDir=packagePath + "/pyCaptureDBData/rho1DB"
rhoPlusDBDir=packagePath + "/pyCaptureDBData/rhoPlusDB"

#Defining the numerical pattern to find files
patternNum="[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?"

#defining a function for finding the right tables by name
def getExistingCSV(mainName):
    #print('Finding the available files with mainName=',mainName)
    dbFiles=glob.glob(mainName+'*).csv')
    #print('found',dbFiles)
    return dbFiles

#defining a function for finding the 4 closest points
def find4ClosestIndexes(inArray,value):
    minorEqual=np.where(inArray<=value)[0][:]
    major=np.where(inArray>value)[0][:]
    #print("minorEqual=",minorEqual)
    #print("major=",major)
    if minorEqual.size >= 2 and major.size >= 2:
        iLow=minorEqual[-2]
        iHigh=major[1]
    elif minorEqual.size == 1 and major.size >=3:
        iLow=minorEqual[-1]
        iHigh=major[2]
    elif minorEqual.size == 0 and major.size >=4:
        iLow=major[0]
        iHigh=major[3]
    elif minorEqual.size >=3 and major.size == 1:
        iLow=minorEqual[-3]
        iHigh=major[0]
    elif minorEqual.size >=4 and major.size == 0:
        iLow=minorEqual[-4]
        iHigh=minorEqual[-1]
    else:
        iLow=NaN
        iHigh=NaN
        print("There is a problem with the input array, for find4Closest")
        print("inArray=",inArray)
    #print("iLow=",iLow,"iHigh=",iHigh)
    return iLow,iHigh
    

#defining the interpolation function for captureEfficiency
def captureEfficiency(rp,RE):
    if rp>1.5:
        eta=-1.0
        message="Particle size ratio rp="+str(rp)+" is out of range: rp should be in [0,1.5]. Capture efficiency can't be estimated"
        return eta,message
    if RE>1000.0:
        eta=-2.0
        message="Reynolds number RE="+str(RE)+" is out of range: Reynolds should be in [0,1000.0]. Capture efficiency can't be estimated"
        return eta,message
    #Checking existing tables for Reynolds
    dbDir=testDBDir
    dbFilePrefix=dbDir+"/"+"eta=(rp,RE="
    REFiles=getExistingCSV(dbFilePrefix)

    #Generating the array of existing RE
    RENumbers=np.array([],dtype=float)
    for ff in REFiles:
        #print(ff)
        floats=[float(j) for j in re.findall(patternNum,ff)]
        RENumbers=np.append(RENumbers,[floats[-1]])
    ind=np.argsort(RENumbers)
    RENumbers=RENumbers[ind]
    #print("RENumbers=",RENumbers)

    #Find 4 closest points for RE
    iLow,iHigh=find4ClosestIndexes(RENumbers,RE)
    the4RE=RENumbers[iLow:iHigh+1]
    #print("the4RE=",the4RE)

    #Obtaining capture efficiency values for the 4 RE@rp
    the4Eta=np.array([],dtype=float)
    for REi in the4RE:
        fileI=dbFilePrefix+str(REi)+").csv"
        arrayI=np.genfromtxt(fileI, delimiter=',')
        #print("arrayI=",arrayI)
        jLow,jHigh=find4ClosestIndexes(arrayI[:,0],rp)
        x=arrayI[jLow:jHigh+1,0]
        y=arrayI[jLow:jHigh+1,1]
        #print("x=",x)
        #print("y=",y)
        #Interpolating into a cubic polynomial
        rpInt=np.poly1d(np.polyfit(x,y,3))
        etaI=rpInt(rp)
        the4Eta=np.append(the4Eta,[etaI])
    #print("the4Eta=",the4Eta)

    #Obtaining the capture efficiency interpolated on log(RE)
    logREInt=np.poly1d(np.polyfit(np.log10(the4RE),the4Eta,3))
    eta=logREInt(np.log10(RE))
    message="eta(rp="+str(rp)+",RE="+str(RE)+")="+str(eta)
    return eta,message


    
    
    
    
        
