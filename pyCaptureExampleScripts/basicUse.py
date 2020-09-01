"""
=================
Example of the use of the python function for estimates of capture efficiency by direct interception:
pyCaptureDB.captureEfficiencyDI

This tool has been provided as additional material of the journal paper:
Espinosa-Gayosso A., Ghisalberti M., Shimeta J. & Ivey G.N. "On predicting particle capture rates in aquatic systems"
Submited to PLOSOne on September2020.
=================

The logic in this example can then be used for your own purposes in other scripts.

For a more elaborated usage example, check the script "totalBiomassOptimisation_Fig10.py"

For an easy to use Graphical User Interface, execute "calculatorGUI.py"
"""
#Import needed dependencies
import numpy as np

#Identifying the path of this script in order to load pyCapture
import inspect
import os
scriptPath = os.path.dirname(inspect.stack()[0][1])

#Defining the path to add to python in order to recognize the pyCapture package:
pyCapturePath=scriptPath + '/../../pyCaptureDev' #Definition as relative path to this script
#pyCapturePath='/Users/esp025/Dropbox/BiologicalPaper/Python/pyCaptureDev' #Definition as absolute path in your own computer

#Loading modules from the pyCapture package
import sys
sys.path.append(pyCapturePath)
from pyCapture import pyCaptureDB

#Testing estimates using simple scalars as incoming values for the function
#Note that output variables are numpy arrays
rpInA=0.8
reynoldsInA=100
(rpOutA,reynoldsOutA,etaOutA)=pyCaptureDB.captureEfficiencyDI(rp=rpInA,Rey=reynoldsInA)

print('--------------------------------------------------------')
print('Testing the estimates when using just single scalars')
print('--------------------------------------------------------')
print('This was the incoming reynoldsInA=')
print(reynoldsInA)
print('And this was the actual reynoldsOutA array used internally by the function, reynoldsOutA=')
print(reynoldsOutA)
print('This was the incoming rpInA=')
print(rpInA)
print('And this was the actual rp array used internally by the function, rpOutA=')
print(rpOutA)
print('.')
print('This is the corresponding estimated etaOutA array (it has a single element)')
print('etaOutA=')
print(etaOutA)
print('.')
print('.')

#Testing estimates using arrays as incoming values for the function
#Note that output variables are numpy arrays
rpInB=np.array([0.4, 0.8, 0.01, 0.15])
reynoldsInB=np.array([1000, 0.0008, 100])
(rpOutB,reynoldsOutB,etaOutB)=pyCaptureDB.captureEfficiencyDI(rp=rpInB,Rey=reynoldsInB)

print('--------------------------------------------------------')
print('Testing the estimates when using several input values at the same time (in arrays)')
print('--------------------------------------------------------')
print('Notice that python interpolator sorts the incoming values before returning the interpolated values.')
print('This is an intrinsic operation of the scipy.interpolate.interp2d')
print('--------------------------------------------------------')
print('.')
print('So this was the incoming rpInB=')
print(rpInB)
print('And this was the actual rp array used within the function (sorted), rpOutB=')
print(rpOutB)
print('.')
print('This was the incoming reynoldsInB=')
print(reynoldsInB)
print('And this was the actual reynolds array used withing the function (sorted), reynoldsOutB=')
print(reynoldsOutB)
print('.')
print('This is the corresponding estimated etaOutB array')
print('Columns are for the rp (the sorted one) and Rows are for the reynolds (the sorted one)')
print('etaOutB=')
print(etaOutB)
print('Note that if we want to know the value for rp=1.5 and reynolds=100, as in the single scalar test above,')
print('Then we need to identify the position of these values within the sorted arrays (not in the original input)')
print('So, the sorted array reynoldsOutB has the value of 100 in the 2nd place (index 1):')
print(np.where(reynoldsOutB == 100)[0])
print('And the sorted array rpOutB has the value of 1.5 in the 4th place (index 3):')
print(np.where(rpOutB == 0.8)[0])
print('So, the value we are looking for is in etaOutB[2ndReynolds when ordered,4th_rp when ordered]')
print('remember that in Python, indexes start in count 0, so 2nd is index 1 and 4th is index 3')
print('i.e. etaOutB[1,3]=')
print(etaOutB[1,3])


