# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 19:16:46 2016

@author: egron
"""


import time
import subprocess
#from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf as pbp
from PIL import Image
import pyzdde.zdde as pyz
import zzdde_SylvainVersion as pzz
import Last_Camera_Function_good_date as Cam
import Last_Motor_Function as Motors
import XPS_Q8_drivers 
import sys
import z_alignment_functions_no_camera as Zalign

#Definition of the properties of the system: 
with open('Z:\\Testbeds\\JOST\\Alignment\\data\\date_for_python.txt', 'r') as pf:
    Date_ = np.loadtxt(pf)

Date=str(int(Date_[0]))+'-'+str(int(Date_[1]))+'-'+str(int(Date_[2]))+'-'+str(int(Date_[3]))+'h-'+str(int(Date_[4]))+'min'
    
with open('Z:\Testbeds\JOST\Alignment\data\\'+Date+'\\python_config_file_'+Date+'.txt', 'r') as pf:
    configFile_python = np.loadtxt(pf)
    
  #number_of_zernike = configFile_python[4]   
zmax = configFile_python[4]+3
actuator_value=np.array([0.5,0.5,0.5])

# Getting the Interaction Matrix Vector
IM=Zalign.InterMatrix_Zalignment(Date,configFile_python,actuator_value)


#Getting the measured vector
measure_vect=Zalign.Compute_measure_vector(Date,configFile_python)
#Simulated measures
#measure_vect=Zalign.Simulated_Wavefront_Zalignment(ConfigFile)

#Getting the residual wavefront vector
residual_vect=Zalign.Residual_Wavefront_Zalignment(Date,configFile_python)


#For MMSE
noise_level=2.
pert=np.array([0.5,0.5,0.5])

Misalignment,Misalignment_motor_motion=Zalign.MMSE_reconstruction(Date,configFile_python,noise_level,pert,IM,measure_vect,residual_vect)

relative_difference=Zalign.relative_difference(Date,configFile_python,residual_vect,measure_vect)
print "LLens misalignment in Zemax)"
print "move L1 by ",Misalignment[0],"mm"    
print "move L2 by ",Misalignment[1],"mm"    
print "move L3 by ",Misalignment[2],"mm"    