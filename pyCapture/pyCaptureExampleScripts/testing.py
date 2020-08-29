import numpy as np

#Loading modules from the pyCapture package
import sys
sys.path.append('/Users/esp025/Dropbox/BiologicalPaper/Python/pyCaptureDev')
from pyCapture import pyCaptureDB as pyCDB

#eta,message=pyCDB.captureEfficiencyTest(rp=0.0075,Rey=950)

#Testing estimates using arrays as incoming values for the function
#Note that output variables are numpy arrays
rpInA=np.array([0.1, 1.5, 0.7, 0.5])
reynoldsInA=np.array([1000, 0.0008, 100])
(rpOutA,reynoldsOutA,etaOutA)=pyCDB.captureEfficiencyEspinosa(rp=rpInA,Rey=reynoldsInA)

print('Testing the estimates when using several values at the same time')
print('Notice that the interpolator sorts the incoming values first')
print('So this was the incoming rpIn=')
print(rpInA)
print('And this was the actual rp array used within the function (sorted), rpOut=')
print(rpOutA)
print('.')
print('This was the incoming ReyIn=')
print(reynoldsInA)
print('And this was the actual Rey array used withing the function (sorted), ReyOut=')
print(reynoldsOutA)
print('.')
print('This is the corresponding estimated eta array')
print('Columns are for the rp (the sorted one) and Rows are for the Rey (the sorted one)')
print('etaOut=')
print(etaOutA)
print('.')
print('.')
print('.')

#Testing estimates using simple scalars as incoming values for the function
#Note that output variables are numpy arrays
rpInB=1.5
reynoldsInB=100
(rpOutB,reynoldsOutB,etaOutB)=pyCDB.captureEfficiencyEspinosa(rp=rpInB,Rey=reynoldsInB)


print('Testing the estimates when using just single scalars')
print('So this was the incoming rpIn=')
print(rpInB)
print('And this was the actual rp array used within the function, rpOut=')
print(rpOutB)
print('.')
print('This was the incoming ReyIn=')
print(reynoldsInB)
print('And this was the actual Rey array used within the function, ReyOut=')
print(reynoldsOutB)
print('.')
print('This is the corresponding estimated eta array')
print('Columns are for the rp (sorted) and Rows are for the Rey (sorted)')
print('etaOut=')
print(etaOutB)
print('Note that this value is the same as the result above etaOutA[1,3]')
print('i.e. etaOutA[2ndReynolds when ordered,4th_rp when ordered]')
print('remember that in Python, indexes start in count 0, so 2nd is index 1 and 4th is index 3')
print(etaOutA[1,3])
print('.')
print('.')
print('.')
