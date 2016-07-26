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


#Definition of the properties of the system: 
with open('Z:\\Testbeds\\JOST\\Alignment\\data\\date_for_python.txt', 'r') as pf:
    Date_ = np.loadtxt(pf)

Date=str(int(Date_[0]))+'-'+str(int(Date_[1]))+'-'+str(int(Date_[2]))+'-'+str(int(Date_[3]))+'h-'+str(int(Date_[4]))+'min'
    
with open('Z:\Testbeds\JOST\Alignment\data\\'+Date+'\\python_config_file_'+Date+'.txt', 'r') as pf:
    configFile_python = np.loadtxt(pf)
    
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

#Getting the measured vector : stacks the wavefront measured for all the fields, and removes the tip-tilt values
measure_vect=Zalign.Compute_measure_vector(Date,configFile_python)

#Getting the residual wavefront vector
residual_vect=Zalign.Simulated_Wavefront_Zalignment_on_vector(field_vector,aligned_state,nbr_zernikes)

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

MMSE=np.zeros((4,nbr_iterations+1))
MMSE[:,0]=np.zeros((4))
LS=np.zeros((4,nbr_iterations+1))
LS[:,0]=np.zeros((4))

error_distance_MMSE=np.zeros((nbr_iterations+1))
error_distance_MMSE[0]=result.distance(Zalign.Simulated_Wavefront_Zalignment_on_vector(field_vector,MMSE[:,0],nbr_zernikes),measure_vect)
error_distance_LS=np.zeros((nbr_iterations+1))
error_distance_LS[0]=result.distance(Zalign.Simulated_Wavefront_Zalignment_on_vector(field_vector,LS[:,0],nbr_zernikes),measure_vect)

residual_vect_MMSE_bis=np.zeros((nbr_sensing_modes*nb_FoV,nbr_iterations+1))
residual_vect_MMSE_bis[:,0]=residual_vect_bis
residual_vect_LS_bis=np.zeros((nbr_sensing_modes*nb_FoV,nbr_iterations+1))
residual_vect_LS_bis[:,0]=residual_vect_bis    


#Loop on Zemax
for ind in range(nbr_iterations):

    #For MMSE       
    MMSE[:,ind+1]=Zalign.MMSE_reconstruction_on_vectors(nb_FoV,noise_level,pert,IM_bis,measure_vect_bis,residual_vect_MMSE_bis[:,ind])
    MMSE[:,ind+1]= MMSE[:,ind+1]+MMSE[:,ind] #add the correction to the former one, MMSE should converge to right result
    #WF simulated
    residual_vect_MMSE_bis[:,ind+1]=Zalign.decoup_element(Zalign.Simulated_Wavefront_Zalignment_on_vector(field_vector,MMSE[:,ind+1],nbr_zernikes),sensing_modes)    
    #Correction quality
    error_distance_MMSE[ind+1]=result.distance(Zalign.Simulated_Wavefront_Zalignment_on_vector(field_vector,MMSE[:,ind+1],nbr_zernikes),measure_vect)
    
    #For LS        
    LS[:,ind+1]=Zalign.LS_reconstruction_on_vectors(cond_val,IM_bis,measure_vect_bis,residual_vect_LS_bis[:,ind])
    LS[:,ind+1]= LS[:,ind+1]+LS[:,ind] #add the correction to the former one, LS should converge to right result    
    #WF simulated
    residual_vect_LS_bis[:,ind+1]=Zalign.decoup_element(Zalign.Simulated_Wavefront_Zalignment_on_vector(field_vector,LS[:,ind+1],nbr_zernikes),sensing_modes)    
    #Correction quality
    error_distance_LS[ind+1]=result.distance(Zalign.Simulated_Wavefront_Zalignment_on_vector(field_vector,LS[:,ind+1],nbr_zernikes),measure_vect)
