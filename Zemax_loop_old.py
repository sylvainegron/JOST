# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 17:06:51 2016

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

measure_vect=Zalign.Compute_measure_vector(Date,configFile_python)
residual_vect=Zalign.Residual_Wavefront_Zalignment(Date,configFile_python)



number_of_zernike = configFile_python[4]   
Zmax = configFile_python[4]-2
actuator_value=np.array([1.,1.,1.,1.])
noise_level=2.

IM = np.zeros((Zmax*nb_FoV,4))
# Getting the noise covarience matrix 
Cn = np.diag(np.ones(nb_FoV*Zmax)*noise_level )  # size: 2D nb_WFS * Zmax , nb_WFS * Zmax


nbr_iterations=4
wf_simulation = np.zeros((Zmax*nb_FoV,nbr_iterations+1)) 
wf_simulation[:,0]=residual_vect
misalignment=   np.zeros((4,nbr_iterations))  
Misalignment_SVD=   np.zeros((4,nbr_iterations))  
   
for iteration in range(nbr_iterations):
    
            
    # Getting the cobariance Matrices    
    # Getting the pertubation covariance matrix
   
   
    Cpsi = np.diag(pert**2) # size: 2D Pmax , Pmax        

    for ind in range(nb_FoV):
    
        #Creating IM for each iteration        
        link = pzz.PyZZDDE()
        link.zDDEInit()
        link.zGetRefresh() 
        # get the wavelenght
        wavesTuple = link.zGetWaveTuple()
        wave = wavesTuple[0][0] * 1000.0 # unit: lambda <-> nm
        link.zSetSurfaceParameter(9, 4, -ConfigFile[6+8*ind]/1000./2.)
        link.zSetSurfaceParameter(9, 3, -ConfigFile[6+8*ind+1]/1000./2.)
       
        actuator_values=actuator_values
        #divide by 1000 because we work with milidegrees in the text file
        #divide by two, because we have to put the half field on the surface coord breaf, for more information 
        #check google doc JOST technical report, steering mirror. 
        #L1    
        # get the push
        link.zSetSurfaceData(18, 3, np.sum(misalignment[0,:])+actuator_values[0])
        coefZern_plus = link.zGetZernikeCoef(Zmax=153)
        # get the pull
        link.zSetSurfaceData(18, 3, np.sum(misalignment[0,:])-actuator_values[0])
        coefZern_minus = link.zGetZernikeCoef(Zmax=153)
        #reset
        link.zSetSurfaceData(18, 3, 0.0)
        # IM computation
        coefZern_IM = (coefZern_plus - coefZern_minus) / (2 * actuator_values[0])
        #IM filling
        IM[ind*Zmax:(ind+1)*Zmax,0] = coefZern_IM[3:Zmax+3]
    
        #L2
        # get the push
        link.zSetSurfaceData(24, 3, np.sum(misalignment[1,:])+actuator_values[1])
        coefZern_plus = link.zGetZernikeCoef(Zmax=153)    
        # get the pull
        link.zSetSurfaceData(24, 3, np.sum(misalignment[1,:])-actuator_values[1])
        coefZern_minus = link.zGetZernikeCoef(Zmax=153)    
        #reset
        link.zSetSurfaceData(24, 3, 0.0)    
        # IM computation
        coefZern_IM = (coefZern_plus - coefZern_minus) / (2 * actuator_values[1])
        #IM filling
        IM[ind*Zmax:(ind+1)*Zmax,1] = coefZern_IM[3:Zmax+3]
           
        #L3   
        # get the push
        link.zSetSurfaceData(31, 3, np.sum(misalignment[2,:])+actuator_values[2])
        coefZern_plus = link.zGetZernikeCoef(Zmax=153)
        # get the pull
        link.zSetSurfaceData(31, 3, np.sum(misalignment[2,:])-actuator_values[2])
        coefZern_minus = link.zGetZernikeCoef(Zmax=153)
        #reset
        link.zSetSurfaceData(31, 3, 0.0)
        # IM computation
        coefZern_IM = (coefZern_plus - coefZern_minus) / (2 * actuator_values[2])
        #IM filling
        IM[ind*Zmax:(ind+1)*Zmax,2] = coefZern_IM[3:Zmax+3]
        
        #Camera    
        # get the push
        link.zSetSurfaceData(39, 3, np.sum(misalignment[3,:])+actuator_values[3])
        coefZern_plus = link.zGetZernikeCoef(Zmax=153)
        # get the pull
        link.zSetSurfaceData(39, 3, np.sum(misalignment[3,:])-actuator_values[3])
        coefZern_minus = link.zGetZernikeCoef(Zmax=153)
        #reset
        link.zSetSurfaceData(39, 3, 0.0)
        # IM computation
        coefZern_IM = (coefZern_plus - coefZern_minus) / (2 * actuator_values[3])
        #IM filling
        IM[ind*Zmax:(ind+1)*Zmax,3] = coefZern_IM[3:Zmax+3]  
        
        
        link.zSetSurfaceParameter(9, 3, 0)
        link.zSetSurfaceParameter(9, 4, 0)
        
        # close the DDE link
        status = link.zDDEClose()
     
        IM=IM*wave 
        
        
        
        # Creation of the classe estimator MMSEEstimator
        estim = ao.MMSEEstimator(IM, Cn, Cpsi)
        misalignment[:,iteration] = estim.reconstruct(wf_simulation[:,iteration]-measure_vect)    # size: 1D Pmax  
       
        U,S,Vt=np.linalg.svd(IM, full_matrices=False)
        cond_val=0.1
        MI=np.linalg.pinv(IM, cond_val)
        Misalignment_SVD[:,iteration]=np.dot(MI,measure_vect-residual_vect)
    
    for ind in range(nb_FoV):
        link = pzz.PyZZDDE()
        link.zDDEInit()
        link.zGetRefresh() 
        # get the wavelenght
        wavesTuple = link.zGetWaveTuple()     
        wave = wavesTuple[0][0] * 1000.0 # unit: lambda <-> nm
        link.zSetSurfaceParameter(9, 4, ConfigFile[6+8*ind]/1000./2.)
        link.zSetSurfaceParameter(9, 3, -ConfigFile[6+8*ind+1]/1000./2.)   
        
        ########################################################################################################
        # Mov the the elements
        
        # Move the elements   
        link.zSetSurfaceData(18, 3, np.sum(misalignment[0,:]))
        link.zSetSurfaceData(24, 3, np.sum(misalignment[1,:]))  
        link.zSetSurfaceData(31, 3, np.sum(misalignment[2,:])) 
        link.zSetSurfaceData(39, 3, np.sum(misalignment[3,:]))         
       
       #Get the Wavefront
        coefZern = link.zGetZernikeCoef(Zmax=153)
          
        # Matrix filling
        wf_simulation[ind*Zmax:(ind+1)*Zmax,iteration+1]=coefZern[3:Zmax+3]
    
        #Reset positions      
        link.zSetSurfaceParameter(9, 4, 0)
        link.zSetSurfaceParameter(9, 3, 0)    
        link.zSetSurfaceData(18, 3, 0 )
        link.zSetSurfaceData(24, 3, 0 )  
        link.zSetSurfaceData(31, 3, 0 ) 
        link.zSetSurfaceData(39, 3, 0 ) 
        
        # close the DDE link
        status = link.zDDEClose()
    
        wf_simulation[ind*Zmax:(ind+1)*Zmax,iteration+1]=wf_simulation[ind*Zmax:(ind+1)*Zmax,iteration+1]*wave
    
    final_misalignment=np.zeros((4)) 
    final_misalignment[0]=np.sum(misalignment[0,:])
    final_misalignment[1]=np.sum(misalignment[1,:])
    final_misalignment[2]=np.sum(misalignment[2,:])
    final_misalignment[3]=np.sum(misalignment[3,:])          