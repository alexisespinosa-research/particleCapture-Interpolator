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

cr1 = np.array([1,1.05,1.1,1.15,1.2])
crAll = np.array([cr1[0],cr1[1]*2,cr1[2]*3,cr1[3]*4,cr1[4]*5])
s1Palps = np.array([cr1[0],cr1[1],cr1[2],cr1[3],cr1[4]])
s2Palps = np.array([0,cr1[1],cr1[2],cr1[3],cr1[4]])
s3Palps = np.array([0,0,cr1[2],cr1[3],cr1[4]])
s4Palps = np.array([0,0,0,cr1[3],cr1[4]])
s5Palps = np.array([0,0,0,0,cr1[4]])
widthBase = 0.5
widths = np.array([widthBase/math.sqrt(1),widthBase/math.sqrt(2),widthBase/math.sqrt(3),widthBase/math.sqrt(4),widthBase/math.sqrt(5)])
bar_positions = np.arange(len(s1Palps))                

hpv_s1 = plt.bar(bar_positions, s1Palps, widths)
hpv_s2 = plt.bar(bar_positions, s2Palps, widths, bottom=s1Palps)
hpv_s3 = plt.bar(bar_positions, s3Palps, widths, bottom=s1Palps+s2Palps)
hpv_s4 = plt.bar(bar_positions, s4Palps, widths, bottom=s1Palps+s2Palps+s3Palps)
hpv_s5 = plt.bar(bar_positions, s5Palps, widths, bottom=s1Palps+s2Palps+s3Palps+s4Palps)

hpv_cr1 = plt.plot(bar_positions, cr1, color='black', marker='s', markersize=7)
hpv_crAll = plt.plot(bar_positions, crAll, color='black', marker='^', markersize=8)

plt.ylim(0,7)
plt.ylabel('$CR/CR_1$')
plt.xticks(bar_positions,bar_positions+1)
plt.xlabel('Number of divisions')
plt.title('Advantage of multiple collectors while keeping total biomass constant')                
plt.show()
