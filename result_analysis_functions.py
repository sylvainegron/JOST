# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 10:41:08 2016

@author: egron
"""

import numpy as np
import zzdde_SylvainVersion as pzz
from sklearn.metrics import mean_squared_error



###################################################################################################
def from_radian_to_nm(vector,wavelength_nm):
    
    new_vect=vector*wavelength_nm/2/np.pi    
    
    return new_vect
    
###################################################################################################
def from_nm_to_radian(vector,wavelength_nm):
    
    new_vect=2*np.pi*vector/wavelength_nm    
    
    return new_vect
 
###################################################################################################   
def error_rms(simulated_wf,measured_wf):
    #mean square error on all the zernikes  (not exclusively the one used for the IM)  
    rms = np.sqrt(np.mean(np.square(simulated_wf-measured_wf)))
    
    return rms
   
###################################################################################################   
def distance(simulated_wf,measured_wf):
      #distance on all the zernikes  (not exclusively the one used for the IM)   
    d = np.sqrt(np.sum(np.square(simulated_wf-measured_wf)))
    
    return d  
    
        