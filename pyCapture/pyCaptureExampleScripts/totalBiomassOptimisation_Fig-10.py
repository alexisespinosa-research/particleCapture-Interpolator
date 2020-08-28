"""
=================
Example of the use of pyticleCapture estimator
=================

This example recreates the Fig.10 from the manuscript:
Espinosa-Gayosso A., Ghisalberti M., Shimeta J. & Ivey G.N. "On predicting particle capture rates in aquatic systems"
Submited to PLOSOne on August2020.
"""

import matplotlib.pyplot as plt
import math
import numpy as np

#Loading modules from the pyCapture package
import sys
sys.path.append('/Users/esp025/Dropbox/BiologicalPaper/Python/pyCaptureDev')
from pyCapture import pyCaptureDB as pyCDB

#Define constant parameters as described in the manuscript
Dc1 = 100E-6 #[m] #Collector diameter for the single collector
Dp = 25E-6 #[m] # Constant particle size
Rey1 = 60 #[-] #Reynolds number for the single collector
h = 5*Dc1 #[m] #Collectors heights
nu = 1E-6 #[m^2/s] #Dynamics viscosity of water

U = Rey1*nu/Dc1 #[m/s] #Incoming velocity
rp1 = Dp/Dc1 #[-] #Particle size ration for single collector
mass1 = math.pi*(Dc1**2/4)*h #The volume is a measure of the total biomass

#Obtain arrays of the values for groups of collectors with same total constant biomass
divisions = np.array([1,2,3,4,5]) #This array represents the division factor of the total biomass in each group
NDivs = len(divisions)
Dc = np.sqrt(np.divide(mass1,divisions)*4/h/math.pi)
rp = np.divide(Dp,Dc)
Rey = U*Dc/nu

#Obtain the capture efficiency for a collector in each group
Eff = np.full(divisions.shape,-1.0)
for i in range (0,NDivs):
    (EffHere,message) = pyCDB.captureEfficiency(rp=rp[i],RE=Rey[i])
    Eff[i]=EffHere
    print(Eff, message)

#Obtain the volumetric capture rates
CapVol = h*U*(np.multiply(Dc,Eff)) #Volumetric capture for a collector 
CapVolNorm = np.divide(CapVol,CapVol[0]) #Normalised capture with respect to group with a just 1 palp (no division)
CapVolGroup = np.multiply(CapVol,divisions)
CapVolGroupNorm = np.multiply(CapVolNorm,divisions)

#Create a list of arrays with the values for each stack bar level
CapByPalps = []
for i in range (0,NDivs):
    CapByPalps.append(np.concatenate((np.full((i,),0.0),CapVolNorm[i:NDivs]),axis=None))

#Create the array of the widths for the bars representing the groups of palps
widthBase = 0.5
widths = widthBase * np.divide(Dc,Dc[0])

#Plotting the stacked bars
bar = []
bottomLast = np.full(divisions.shape,0.0)
for i in range (0,NDivs):
    bar = plt.bar(divisions, CapByPalps[i], widths, bottom=bottomLast)
    bottomLast = bottomLast + CapByPalps[i]

line_single = plt.plot(divisions, CapVolNorm, color='black', marker='s', markersize=7)
line_group = plt.plot(divisions, CapVolGroupNorm, color='black', marker='^', markersize=8)

plt.ylim(0,7)
plt.ylabel('$CR/CR_1$')
plt.xticks(divisions,divisions)
plt.xlabel('Number of divisions')
plt.title('Advantage of multiple collectors while keeping total biomass constant')                
plt.show()
