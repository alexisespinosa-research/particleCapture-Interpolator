"""
=================
Example of the use of the python function for estimates of capture efficiency by direct interception:
pyCaptureDB.captureEfficiencyDI

This tool has been provided as additional material of the journal paper:
Espinosa-Gayosso A., Ghisalberti M., Shimeta J. & Ivey G.N. "On predicting particle capture rates in aquatic systems"
Submited to PLOSOne on September2020.
=================

This example recreates the Fig.10 from the manuscript.

For a basic example on how to use the function, check the script "basicUse.py"

For an easy to use Graphical User Interface, execute "calculatorGUI.py"
"""

#Loading needed dependencies
import matplotlib.pyplot as plt
import math
import numpy as np

#Identifying the path of this script in order to load pyCapture
import inspect
import os
scriptPath = os.path.dirname(inspect.stack()[0][1])

#Defining the path to add to python in order to recognize the pyCapture package:
pyCapturePath=scriptPath + '/../../../pyCaptureDev' #Definition as relative path to this script
#pyCapturePath='/Users/esp025/Dropbox/BiologicalPaper/Python/pyCaptureDev' #Definition as absolute path in your own computer

#Loading modules from the pyCapture package
import sys
sys.path.append(pyCapturePath)
from pyCapture import pyCaptureDB

#Define constant parameters as described in the manuscript
Dc1 = 100E-6 #[m] #Collector diameter for the single collector with the total mass (no divisions)
Dp = 25E-6 #[m] # Constant particle size (same for all groups)
U = 0.06 #[m/s] #Incoming velocity (same for all groups)

#Define additional parameters (assumed in the manuscript)
nu = 1E-6 #[m^2/s] #Dynamics viscosity of water (same for all groups)

#Define additional parameters (not relevant as their values does not affect the normalized results at all)
h = 5*Dc1 #[m] #Collectors heights (same for all groups)
Cp = 1000 #[particles/m^3] #Particle concentration (same for all groups)
rhoCollector = 1020 #[kg/m^3] #Density of the collector material (same for all groups)

#Estimate parameters from the problem definition above
Rey1 = U*Dc1/nu #[-] #Reynolds number for the single collector with the total mass (no divisions)
totalVolume = math.pi*(Dc1**2/4)*h # [m^3] #Constant total volume (same for all groups)
totalMass = rhoCollector*totalVolume #[kg] #Constant total mass (same for all groups)

#Obtain arrays of the values for groups of collectors with same total constant biomass
divisions = np.array([1,2,3,4,5]) #This array represents the division factor of the total biomass in each group
print("The number of divisions (collectors) keeping original total mass constant, divisions=")
print(divisions)
NDivs = len(divisions)
Dc = np.sqrt(np.divide(totalVolume,divisions)*4/h/math.pi) #Array with diameters of collector of each group after division
rpIn = np.divide(Dp,Dc) #Array with the particleSizeRatio that varies for each group depending on the diameter of the collector
print("The particle size ratios are rpIn=")
print(rpIn)
ReyIn = U*Dc/nu #Array with the Reynolds number for each group depending on the diameter of the collector
print("The Reynolds numbers are ReyIn=")
print(ReyIn)

#Obtain the capture efficiency for a collector in each group (It may be less confusing to work element by element)
Eff = np.full(divisions.shape,-1.0)
for i in range (0,NDivs):
    (rpOutHere,ReyOutHere,EffOutHere) = pyCaptureDB.captureEfficiencyDI(rp=rpIn[i],Rey=ReyIn[i])
    Eff[i]=EffOutHere[0] #EffOutHere is a numpy array, even if it has only one element
print("The capture efficiencies are Eff=")
print(Eff)

#(Or:)
#Obtain the capture efficiency using the arrays directly in the function (we need to extract the desired values from output arrays)
##(rpOut,ReyOut,EffOut) = pyCaptureDB.captureEfficiencyDI(rp=rpIn,Rey=ReyIn)
##print("Note that rpIn and ReyIn are sorted within the function before estimating efficiency (this is a Python thing)")
##print("rpIn:")
##print(rpIn)
##print("rpOut:")
##print(rpOut)
##print("ReyIn:")
##print(ReyIn)
##print("ReyOut:")
##print(ReyOut)
##print("And this is the efficiency array (in the order used by the function)")
##print("EffOut:")
##print(EffOut)
##print("Then, elements needed are EffOut[4,0],EffOut[3,1],EffOut[2,2],EffOut[1,3],EffOut[0,4]")
##Eff = np.full(divisions.shape,-1.0)
##for i in range (0,NDivs):
##    rpI=np.where(rpOut==rpIn[i])
##    ReyI=np.where(ReyOut==ReyIn[i])
##    Eff[i]=EffOut[ReyI,rpI]
##print("The capture efficiencies are Eff:")
##print(Eff)

#Obtain the volumetric capture rates
CR = Cp*h*U*(np.multiply(Dc,Eff)) #Capture Rate for one collector in each group
CRNorm = np.divide(CR,CR[0]) #Normalised capture with respect to the total mass with just 1 palp (no division)
print('The normalised capture rates for a single collector are, CRNorm=')
print(CRNorm)
CRGroup = np.multiply(CR,divisions) #Capture Rate for the whole group (all collectors with group total mass constant)
CRGroupNorm = np.multiply(CRNorm,divisions) #Normalised capture for the group
print('The normalised capture rates for the whole group are, CRGroupNorm=')
print(CRGroupNorm)

#Create a list of arrays with the values for each stack bar level
CapByPalps = []
for i in range (0,NDivs):
    CapByPalps.append(np.concatenate((np.full((i,),0.0),CRNorm[i:NDivs]),axis=None))

#Create the array of the widths for the bars representing the groups of palps
widthBase = 0.5
widths = widthBase * np.divide(Dc,Dc[0])

#Plotting the stacked bars
bar = []
bottomLast = np.full(divisions.shape,0.0)
for i in range (0,NDivs):
    bar = plt.bar(divisions, CapByPalps[i], widths, bottom=bottomLast)
    bottomLast = bottomLast + CapByPalps[i]

line_single = plt.plot(divisions, CRNorm, color='black', marker='s', markersize=7)
line_group = plt.plot(divisions, CRGroupNorm, color='black', marker='^', markersize=8)

plt.ylim(0,7)
plt.ylabel('$CR/CR_1$')
plt.xticks(divisions,divisions)
plt.xlabel('Number of divisions')
plt.title('Advantage of multiple collectors while keeping total biomass constant')                
plt.show()
