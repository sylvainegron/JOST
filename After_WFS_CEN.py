# -*- coding: utf-8 -*-
"""
Created on Mon May 30 14:30:03 2016

@author: egron
"""

# -*- coding: utf-8 -*-
"""
Created on Fri May 20 17:18:24 2016

@author: egron
"""
#ca va le faire

import time
import subprocess
#from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf as pbp
from PIL import Image
import pyzdde.zdde as pyz
import zzdde_SylvainVersion as pzz
import camera_functions as Cam
import motors_functions as Motors
import XPS_Q8_drivers 
import sys
import z_alignment_functions as Zalign
import result_analysis_functions as result
import CEN_functions as CEN

#testes
#Definition of the properties of the system: 
with open('Z:\\Testbeds\\JOST\\Alignment\\data\\date_for_python.txt', 'r') as pf:
    Date_ = np.loadtxt(pf)

Date=str(int(Date_[0]))+'-'+str(int(Date_[1]))+'-'+str(int(Date_[2]))+'-'+str(int(Date_[3]))+'h-'+str(int(Date_[4]))+'min'
    
with open('Z:\Testbeds\JOST\Alignment\data\\'+Date+'\\python_config_file_'+Date+'.txt', 'r') as pf:
    configFile_python = np.loadtxt(pf)

with open('Z:\Testbeds\JOST\Alignment\data\\'+Date+'\\psf_position.txt', 'r') as pf:
    psf_position = np.loadtxt(pf)
    
#FoV to define the Interaction matrix, and simulate images from a pertubation vector
nb_FoV = (np.size(configFile_python)-6)/8

   
##############################################################################################################################
#LINEAR CONTROL CALCULATION
#Getting field vector
field_vector=np.zeros((2*nb_FoV))
for ind in range(nb_FoV):
    field_vector[2*ind]=configFile_python[6+ind*8]
    field_vector[2*ind+1]=configFile_python[7+ind*8]
    
#Number of Zernikes to descibre the Wavefront (Piston, Tip and Tilt are not included): 
#It's number of zernike I get from the phase diversity. 
nbr_zernikes = configFile_python[4]-2
cond_val=0.1

nbr_iterations=5

noise_level=2.
pert=np.array([1.,1.,1.,1.])  
   
actuator_value=np.array([0.5,0.5,0.5,0.5])

# Getting the Interaction Matrix Vector        
aligned_state=np.zeros((4))   
  
IM=Zalign.IM_on_vectors(field_vector,actuator_value,aligned_state,nbr_zernikes)
IM_CEN=CEN.IM_CEN(field_vector,actuator_value,aligned_state)
#Getting the measured vector : stacks the wavefront measured for all the fields, and removes the tip-tilt values
measure_vect=Zalign.Compute_measure_vector(Date,configFile_python)
measure_vect_CEN=psf_position

#Getting the residual wavefront vector
residual_vect=Zalign.Simulated_Wavefront_Zalignment_on_vector(field_vector,aligned_state,nbr_zernikes)
residual_vect_CEN=CEN.simulated_CEN(field_vector,aligned_state)
###########################################################################################################
#Choosing the sensing modes:    put 1 if you want to keep the mode, 0 if you want to reject it
sensing_modes=np.zeros((nbr_zernikes))
sensing_modes[0]=1
sensing_modes[2]=1
sensing_modes[4]=1
sensing_modes[8]=1
sensing_modes[9]=1
nbr_sensing_modes=np.count_nonzero(sensing_modes)

IM_bis=Zalign.decoup_line(IM,sensing_modes)
measure_vect_bis=Zalign.decoup_element(measure_vect,sensing_modes)
residual_vect_bis=Zalign.decoup_element(residual_vect,sensing_modes)  

#adding CEN
IM_final=np.concatenate((Zalign.decoup_line(IM,sensing_modes),IM_CEN),axis=0)
measure_vect_final=np.concatenate((Zalign.decoup_element(measure_vect,sensing_modes),measure_vect_CEN),axis=0)
residual_vect_final=np.concatenate((Zalign.decoup_element(residual_vect,sensing_modes),residual_vect_CEN),axis=0)
    

MMSE=Zalign.MMSE_reconstruction_on_vectors(nb_FoV,noise_level,pert,IM_final,measure_vect_final,residual_vect_final)
LS=Zalign.LS_reconstruction_on_vectors(cond_val,IM_final,measure_vect_final,residual_vect_final)
U,S,Vt=np.linalg.svd(IM_final, full_matrices=False)
