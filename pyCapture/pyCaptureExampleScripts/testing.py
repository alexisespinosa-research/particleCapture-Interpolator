#Loading modules from the pyCapture package
import sys
sys.path.append('/Users/esp025/Dropbox/BiologicalPaper/Python/pyCaptureDev')
from pyCapture import pyCaptureDB as pyCDB

#eta,message=pyCDB.captureEfficiencyTest(rp=0.0075,RE=950)

eta,message=pyCDB.captureEfficiency(rpX=0,REY=0.0009)

print(eta,message)
