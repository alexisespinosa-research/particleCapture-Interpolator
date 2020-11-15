"""
=================
Example of the basic usage of the python function for estimates of capture efficiency by direct interception:
pyCaptureDB.captureEfficiencyDI

This tool has been provided as additional material of the journal paper:
Espinosa-Gayosso A., Ghisalberti M., Shimeta J. & Ivey G.N. "On predicting particle capture rates in aquatic systems"
Submited to PLOSOne on September2020.
=================

The logic in this example can then be used for your own purposes in other scripts.

For a more elaborated usage example, check the script "totalBiomassOptimisation_Fig10.py"

For an easy to use Graphical User Interface, execute "calculatorGUI.py"
"""

"""
=================
Explanation of the function:
pyCaptureDB.captureEfficiencyDI

The function Receives two input arguments:
-rp (which is the particle size ratio)
-Rey (which is the Reynolds number)
These can be numpy arrays, lists or single scalars.

It is VERY IMPORTANT to note that, if the input is not a numpy array,
then it will be converted into a numpy array internally before proceeding.

It is also VERY IMPORTANT to note that both input arrays will be SORTED before proceeding.
So the results given back will be ordered according to the sorted arrays.

The accepted values for rp are in the range [0,1.5]
The accepted values for Rey are in the range [0,1000]

As the function converts the input into sorted numpy arrays, the function Returns three numpy arrays:
-rp (the actual sorted numpy array used for the estimates)
-Rey (the actual sorted numpy array used for the estimates)
-eta (the estimates of capture efficiency by direct interception) (result of the interpolation from the input sorted arrays)

=================
"""

#Import needed dependencies
import numpy as np

#Identifying the path of this script in order to load pyCapture
#import inspect
import os
scriptPath = os.getcwd()

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
print('First, will test the estimates when using just single scalars.')
print('--------------------------------------------------------')
print('')
print('')
input('PRESS ENTER TO CONTINUE')
print('')
print('')
print('This is the original input value for the Particle Size Ratio:')
print('rpInA=',rpInA)
print('And this is the actual SORTED array used internally by the function (which is returned back by the function for user\'s information):')
print('rpOutA=',rpOutA)
print('')
print('This is the original input value for the Reynolds number:')
print('reynoldsInA=', reynoldsInA)
print('And this is the actual SORTED array used internally by the function (which is returned back by the function for user\'s information):')
print('reynoldsOutA=',reynoldsOutA)
print('')
print('This is the resulting numpy array of Capture Efficiency estimates (in this case, it has just one element):')
print('etaOutA=',etaOutA)
print('')
print('')
input('PRESS ENTER TO CONTINUE')



#Testing estimates using arrays as incoming values for the function
#Note that output variables are numpy arrays
rpInB=np.array([0.4, 0.8, 0.01, 0.15 ])
reynoldsInB=np.array([1000, 0.0008, 100 ])
(rpOutB,reynoldsOutB,etaOutB)=pyCaptureDB.captureEfficiencyDI(rp=rpInB,Rey=reynoldsInB)

print('--------------------------------------------------------')
print('Second, will test estimates when using several input values at the same time (in arrays)')
print('--------------------------------------------------------')
print('Notice that python interpolator sorts the input arrays before the actual interpolation operation.')
print('This is an intrinsic operation of the scipy.interpolate.interp2d')
print('For this reason, our estimate function returns those sorted input arrays for user\'s information')
print('--------------------------------------------------------')
print('')
print('')
input('PRESS ENTER TO CONTINUE')
print('')
print('')
print('This is the original input array of Reynolds Numbers:')
print('reynoldsInB=',reynoldsInB)
print('And this is the actual SORTED array used internally by the function (which is returned back by the function for user\'s information):')
print('reynoldsOutB=',reynoldsOutB)
print('')
print('This is the original input array of Particle Size Ratios:')
print('rpInB=',rpInB)
print('And this is the actual SORTED array used internally by the function (which is returned back by the function for user\'s information):')
print('rpOutB=',rpOutB)
print('')
print('This is the resulting numpy array of Capture Efficiency etimates:')
print('Rows are for the reynolds (the sorted one) and Columns are for the rp (the sorted one):')
print('etaOutB=',etaOutB)
print('')
print('Note that if we want to know the value for rp=0.8 and reynolds=100, as in the single scalar test above,')
print('Then we need to identify the position of these values within the sorted arrays (not in the original input)')
print('So, the sorted array reynoldsOutB has the value of 100 in the 2nd place (index 1 for python):')
print(np.where(reynoldsOutB == 100)[0])
print('And the sorted array rpOutB has the value of 0.8 in the 4th place (index 3 for python):')
print(np.where(rpOutB == 0.8)[0])
print('(Remember that in Python, array indexes start in count=0.)')
print('Then, the value we are looking for is:')
print('etaOutB[1,3]=',etaOutB[1,3])
print('')
print('')
input('PRESS ENTER TO CONTINUE')


