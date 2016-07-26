# -*- coding: utf-8 -*-
"""
Created on Mon May 30 14:30:03 2016

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
import pylab as pylab

 #Definition of the properties of the system: 
with open('Z:\\Testbeds\\JOST\\Alignment\\data\\date_for_python.txt', 'r') as pf:
    Date_ = np.loadtxt(pf)

Date=str(int(Date_[0]))+'-'+str(int(Date_[1]))+'-'+str(int(Date_[2]))+'-'+str(int(Date_[3]))+'h-'+str(int(Date_[4]))+'min'
    
with open('Z:\Testbeds\JOST\Alignment\data\\'+Date+'\\python_config_file_'+Date+'.txt', 'r') as pf:
    configFile_python = np.loadtxt(pf)
    
#FoV to define the Interaction matrix, and simulate images from a pertubation vector
nb_FoV = (np.size(configFile_python)-6)/8

   

#Number of Zernikes to descibre the Wavefront (Piston, Tip and Tilt are not included): 
#It's number of zernike I get from the phase diversity. 
number_of_zernike = configFile_python[4]   
zmax = configFile_python[4]+3
actuator_value=np.array([1.,1.,1.,1.])

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
pert=np.array([1.,1.,1.,1.])
nombre_iterations=5
Misalignment,Misalignment_motor_motion=Zalign.MMSE_reconstruction(Date,configFile_python,noise_level,pert,IM,measure_vect,residual_vect)
wf,mis,m=Zalign.loop_zemax(Date,configFile_python,noise_level,pert,measure_vect,residual_vect,actuator_value,nombre_iterations)

x=range(nombre_iterations)
pylab.plot(x,mis[0,:],'-b', label='L1')
pylab.plot(x,mis[1,:],'-r', label='L2')
pylab.plot(x,mis[2,:],'-c', label='L3')
pylab.plot(x,mis[3,:],'-g', label='Camera')
pylab.legend(loc='upper right')
pylab.xlabel('iteration number')
pylab.ylabel('longitudinal shift (mm)')


#x2=np.array([4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19])
#pylab.plot(x2,measure_vect,'-b', label='measure')
#pylab.plot(x2,wf[:,5],'-c', label='simulated')
#pylab.legend(loc='upper right')
#pylab.xlabel('zernike coefficient')
#pylab.ylabel('aberration in nm')
#SVD

U,S,Vt=np.linalg.svd(IM, full_matrices=False)
cond_val=0.1
MI=np.linalg.pinv(IM, cond_val)
Misalignment_SVD=np.dot(MI,measure_vect-residual_vect)

relative_difference=Zalign.relative_difference(Date,configFile_python,residual_vect,measure_vect)
print "Lens shift to apply (values are given in the actauator space reference)"
print "move L1 by ",Misalignment[0],"mm"    
print "move L2 by ",Misalignment[1],"mm"    
print "move L3 by ",Misalignment[2],"mm"    

print "SVD results"
print Misalignment_SVD[0]
print Misalignment_SVD[1]
print Misalignment_SVD[2]