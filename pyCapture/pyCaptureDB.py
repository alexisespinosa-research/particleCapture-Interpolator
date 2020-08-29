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
etaCFD = interpolate.interp2d(rpDataX,lnReynoldsDataY,efficiencyDataZ,kind='cubic',fill_value=-16.0)

#defining the interpolation function for captureEfficiency
def captureEfficiencyEspinosa(rp: np.ndarray, Rey: np.ndarray) -> (np.ndarray,np.ndarray,np.ndarray):
    #Checking type for rp
    if isinstance(rp, np.ndarray):
        #print('Incoming rp is a numpy array')
        rp=rp
    elif isinstance(rp, list):
        #print('Incoming rp is a list, converting it to a numpy array')
        rp=np.array(rp)
    elif isinstance(rp, (int,float)):
        #print('Incoming rp is a scalar, converting it to a numpy array')
        rp=np.array([rp])
    else:
        raise TypeError('Wrong Type for rp parameter')
    #Checking type for Rey
    if isinstance(Rey, np.ndarray):
        #print('Rey is a good parameter numpy array')
        Rey=Rey
    elif isinstance(Rey, list):
        #print('Rey is a list, converting it to a numpy array')
        Rey=np.array(Rey)
    elif isinstance(Rey, (int,float)):
        #print('Rey is a scalar, converting it to a numpy array')
        Rey=np.array([Rey])
    else:
        raise TypeError('Wrong Type for Rey parameter')

    #Converting everything to floats
    rp=rp*1.0
    Rey=Rey*1.0

    #Sorting rp and Reynolds (because the interpolating algorthm sorts the input arrays anyway)
    #So, it is better to have them as they are going to be used
    rp = np.sort(rp)
    Rey = np.sort(Rey)

    #Checking that ranges of the parameters are correct
    if (rp>np.max(rpDataX)).all():
        errorMessage="Particle size ratio rp="+str(rp)+" is above the accepted range: rp should be in [0," + str(np.max(rpDataX)) +"]. Capture efficiency can't be estimated"
        raise TypeError(errorMessage)
    if (rp<0.0).all():
        errorMessage="Particle size ratio rp="+str(rp)+" is below the accepted range: rp should be in [0," + str(np.max(rpDataX)) +"]. Capture efficiency can't be estimated"
        raise TypeError(errorMessage)
    if (Rey>np.max(reynoldsDataY)).all():
        errorMessage="Reynolds number Rey="+str(Rey)+" is above the accepted range: Reynolds should be in (0," + str(np.max(reynoldsDataY)) +"]. Capture efficiency can't be estimated"
        raise TypeError(errorMessage)
    if (Rey<=0.0).all():
        errorMessage="Reynolds number Rey="+str(Rey)+" is below the accepted range: Reynolds should be in (0," + str(np.max(reynoldsDataY)) +"]. Capture efficiency can't be estimated"
        raise TypeError(errorMessage)

    #AEG. To be removed/commented after test
    #print("rpDataX is:")
    #print(rpDataX)
    #print("reynoldsDataY is:")
    #print(reynoldsDataY)

    #Estimating capture efficiency
    lnRey = np.log(Rey)
    eta = etaCFD(rp,lnRey)
    
    #AEG. To be removed/commented after test. Obtaining the capture efficiency interpolated on the logarithmic axis both reynolds and rp
    #log10Rey = np.log10(Rey)   
    #print("etaCFD = ", etaCFD(rp,lnRey))
    #print("etaLNRey_I2D = ", etaLNRey_I2D(rp,lnRey))
    #print("etaLRey_I2D = ", etaLRey_I2D(rp,log10Rey))
    #print("etaLRey_RBS = ", np.transpose(etaLRey_RBS(rp,np.transpose(log10Rey))))    

    #When estimates are for very low Reynolds, use the creeping flow formulation
    if (Rey < np.min(reynoldsDataY)).any():
        #Creating the XX,YY masks
        maskRp = np.full(rp.shape,1.0)
        maskReyLower = (Rey < np.min(reynoldsDataY))*1.0
        maskReyHigher = (Rey >= np.min(reynoldsDataY))*1.0
        maskRpXX, maskReyLowerYY = np.meshgrid(maskRp,maskReyLower)
        maskRpXX, maskReyHigherYY = np.meshgrid(maskRp,maskReyHigher)

        #Applying the formula to the meshgridded values
        rpXX, ReyYY = np.meshgrid(rp,Rey)
        lnReyYY = np.log(ReyYY)
        fR = 0.953 * np.log(6.25 + ReyYY) -1.62
        kR = 0.872 * np.log(19.1 + ReyYY) -1.92
        etaZZ = np.divide(1.0, 2.002 - lnReyYY + fR) * np.divide( rpXX**2, np.power(1.0 + rpXX, kR))

        #Appying masks and merging results
        etaZZ=np.multiply(etaZZ,maskReyLowerYY)
        eta=np.multiply(eta,maskReyHigherYY)
        eta=eta+etaZZ


    #Correcting to exact zeros for those etas with rp=0.0
    if (rp == 0.0).any():
        maskRp = (rp != 0.0)*1.0;
        maskRey = np.full(Rey.shape,1.0);
        maskRpXX, maskReyYY = np.meshgrid(maskRp,maskRey)
        eta = np.multiply(eta,maskRpXX)

    return rp,Rey,eta
    
    
    
    
    
        
