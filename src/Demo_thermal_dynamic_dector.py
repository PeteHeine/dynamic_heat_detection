#!/usr/bin/env python

#import rospy

import cv2
import time
import numpy as np
import matplotlib.pyplot as plt
import thermal_dynamic_detector as dd
from scipy import ndimage

imgTemperature = np.load('/home/pistol/thermal_raw.npy')

rSky = 0.2 # Area not to be used in the in determining the median temperature. 
degAboveMedian = 3.0 # 
degDiff = 30.0
rot90ImageK = 2
connectComponents = True

t0 = time.time()
out,nRemoveSky = dd.dynamicThreshold(imgTemperature,degAboveMedian,degDiff,rSky,rot90ImageK,connectComponents)
print "Processing time: ", (time.time()-t0)*1000, "ms"


            
# Convert to temperatures (however this is wasted calculations)
#imgTemperature = imgF*0.04-273.15

imgTemperature = dd.ConvertFlirOutput2temperature(imgTemperature)
imgTemperature = np.rot90(imgTemperature,k=2)

imgTemperature[nRemoveSky:nRemoveSky+2,:] = np.max(imgTemperature)
#plt.figure();
#plt.imshow(imgTemperature)
#plt.colorbar()
#
#
#plt.figure();
#plt.imshow(out)
#plt.colorbar()


## Figures for illutration 
plt.figure();
plt.imshow(imgTemperature)
plt.colorbar()

nRemoveSky = int(float(imgTemperature.shape[0])*rSky)

# Determine median of area not being sky
medianTemp = np.median(imgTemperature[nRemoveSky:,:])
print "medianTemp: ", medianTemp

imgTemperature2 = np.clip(imgTemperature-medianTemp-degAboveMedian,0.0,degDiff)

plt.figure();
plt.imshow(imgTemperature2)
plt.colorbar()

plt.figure();
plt.imshow(out.astype(np.float32)/255)
plt.colorbar()