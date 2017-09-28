#!/usr/bin/env python
import numpy as np
from scipy import ndimage
toK_scale = 0.04
toC_shift = 273.15
from skimage import morphology
def ConvertFlirOutput2temperature(imgFlir):
    imgTemperature = imgFlir*toK_scale-toC_shift
    return imgTemperature

def dynamicThreshold(imgFlir, degAboveMedian, degDiff, rRemoveSky, rot90ImageK=0, connectComponent = False):
    # Crop away sky
    nRemoveSky = int(float(imgFlir.shape[0])*rRemoveSky)
    
    # Convert values from temperature (Kelvin/Celsius) to flir camera values. 
    aboveMedian = degAboveMedian/toK_scale
    diff = degDiff/toK_scale
    
    
    # Flip image
    if rot90ImageK > 0:
        imgFlir = np.rot90(imgFlir,k=rot90ImageK)
    
    # Determine median of area not being sky
    medianTemp = np.median(imgFlir[nRemoveSky:,:])
    
    
    # Clip values and Scale values between 0 and 255
    out = ((np.clip(imgFlir-medianTemp-aboveMedian,0.0,diff)/diff)*255.0).astype(np.uint8)
    
    # Use max value of connected components
    if connectComponent:
        bwImg = out>0.0
        #bwImg = ndimage.binary_opening(bwImg, structure=np.ones((5,5))).astype(np.int)
        #bwImg = morphology.remove_small_objects(bwImg, min_size=10, connectivity=2)
        blobs_labels,n = ndimage.measurements.label(bwImg)
        slicers = ndimage.find_objects(blobs_labels)    
        
        for slicer in slicers:
            outSlice = out[slicer]
            outSlice[outSlice>0] = np.max(outSlice)
            out[slicer] = outSlice
    return out,nRemoveSky
    
    
