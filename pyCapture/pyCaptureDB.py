import numpy as np
from scipy import interpolate
import glob,re

#Identifying the path of this script in order to find the databases
import inspect
import os
packagePath = os.path.dirname(inspect.stack()[0][1])

#Defining Data Base Directories
testDBDir=packagePath + "/pyCaptureDBData/testDB"
rho1DBDir=packagePath + "/pyCaptureDBData/rho1DB"
rhoPlusDBDir=packagePath + "/pyCaptureDBData/rhoPlusDB"

#Loading the Data Matrices
efficiencyDataZ = np.genfromtxt(rho1DBDir + "/efficiencyDataZ.csv", delimiter=',')
rpDataX = np.genfromtxt(rho1DBDir + "/rpDataX.csv", delimiter=',')
reynoldsDataY = np.genfromtxt(rho1DBDir + "/reynoldsDataY.csv", delimiter=',')

#Obtaining the logarithmic axis
#log10RpDataX = np.log10(rpDataX)
log10ReynoldsDataY = np.log10(reynoldsDataY)
lnReynoldsDataY = np.log(reynoldsDataY)

#Obtaining the interpolation function
#etaL_RBS = interpolate.RectBivariateSpline(log10RpDataX,log10ReynoldsDataY,np.transpose(efficiencyDataZ))
#etaL_I2D = interpolate.interp2d(log10RpDataX,log10ReynoldsDataY,efficiencyDataZ,kind='cubic')
#etaR_RBS = interpolate.RectBivariateSpline(rpDataX,reynoldsDataY,np.transpose(efficiencyDataZ))
#etaR_I2D = interpolate.interp2d(rpDataX,reynoldsDataY,efficiencyDataZ,kind='cubic')
#etaLRey_RBS = interpolate.RectBivariateSpline(rpDataX,log10ReynoldsDataY,np.transpose(efficiencyDataZ))
#etaLRey_I2D = interpolate.interp2d(rpDataX,log10ReynoldsDataY,efficiencyDataZ,kind='cubic')
#etaLNRey_I2D = interpolate.interp2d(rpDataX,lnReynoldsDataY,efficiencyDataZ,kind='cubic') #Chosen one
etaCFD = interpolate.interp2d(rpDataX,lnReynoldsDataY,efficiencyDataZ,kind='cubic')


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
    

#defining the interpolation function for captureEfficiencyTest
def captureEfficiencyTest(rp,RE):
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
    log10REInt=np.poly1d(np.polyfit(np.log10(the4RE),the4Eta,3))
    eta=log10REInt(np.log10(RE))
    message="eta(rp="+str(rp)+",RE="+str(RE)+")="+str(eta)
    return eta,message

#defining the interpolation function for captureEfficiency
def captureEfficiency(rpX,REY):
    rpX=rpX*1.0
    REY=REY*1.0
    if rpX>np.max(rpDataX):
        eta=-1.0
        message="Particle size ratio rp="+str(rpX)+" is above the accepted range: rp should be in [0," + str(np.max(rpDataX)) +"]. Capture efficiency can't be estimated"
        return eta,message
    if rpX<0.0:
        eta=-2.0
        message="Particle size ratio rp="+str(rpX)+" is below the accepted range: rp should be in [0," + str(np.max(rpDataX)) +"]. Capture efficiency can't be estimated"
        return eta,message
    if REY>np.max(reynoldsDataY):
        eta=-3.0
        message="Reynolds number RE="+str(REY)+" is above the accepted range: Reynolds should be in (0," + str(np.max(reynoldsDataY)) +"]. Capture efficiency can't be estimated"
        return eta,message
    if REY<=0.0:
        eta=-4.0
        message="Reynolds number RE="+str(REY)+" is below the accepted range: Reynolds should be in (0," + str(np.max(reynoldsDataY)) +"]. Capture efficiency can't be estimated"
        return eta,message

    #AEG. To be removed after test
    #print("rpDataX is:")
    #print(rpDataX)
    #print("reynoldsDataY is:")
    #print(reynoldsDataY)

    #Estimating capture efficiency
    lnREY = np.log(REY)
    if rpX==0.0:
        eta=0.0
        message="Particle is of null size. rpX="+str(rpX)
    #Using approximation based on creeping flow + hybrid approach (Espinosa et al 2012)
    elif REY < np.min(reynoldsDataY):
        fR = 0.953 * np.log(6.25 + REY) -1.62
        kR = 0.872 * np.log(19.1 + REY) -1.92
        eta = np.divide(1.0, 2.002 - lnREY + fR) * np.divide( rpX**2, np.power(1.0 + rpX, kR))
        message="Using creeping + hybrid formula of Espinosa 2012"
    else:
        eta = etaCFD(rpX,lnREY)
        message="Interpolating from CFD results of Espinosa 2012,2013"

    #AEG. To be removed after test. Obtaining the capture efficiency interpolated on the logarithmic axis both reynolds and rp
    #log10REY = np.log10(REY)   
    #print("etaCFD = ", etaCFD(rpX,lnREY))
    #print("etaLNRey_I2D = ", etaLNRey_I2D(rpX,lnREY))
    #print("etaLRey_I2D = ", etaLRey_I2D(rpX,log10REY))
    #print("etaLRey_RBS = ", np.transpose(etaLRey_RBS(rpX,np.transpose(log10REY))))

    #AEG. To be removed after test. Using approximation based on creeping flow + hybrid approach (Espinosa et al 2012)
    #fR = 0.953 * np.log(6.25 + REY) -1.62
    #kR = 0.872 * np.log(19.1 + REY) -1.92
    #etaFit = np.divide(1.0, 2.002 - lnREY + fR) * np.divide( rpX**2, np.power(1.0 + rpX, kR))
    #print("etaFit =", etaFit)

    return eta,message



    
    
    
    
    
    
        
