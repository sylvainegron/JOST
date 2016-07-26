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



######################################################################################################################
#GETTING THE IMAGES

# INITIALIZE SOURCE LASER:
channel=1
current=0.0
LASERexePath = "C:\\Users\\jost\\Desktop\\SourceLaser\\debug\\"
LASER = subprocess.Popen(["C:\\Users\\jost\\Desktop\\SourceLaser\\debug\\SourceLaser.exe", str(channel), str(current)], 
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                        cwd=LASERexePath, bufsize=1)
current=[0,48.7,48.7]


## INITIALIZE IRISAO D.M.:
#disableHardware = "false"
#DMexePath = "C:\\Users\\jost\\Desktop\\Control DM\\Code\\release"
#DM = subprocess.Popen(["C:\\Users\\jost\\Desktop\\Control DM\\Code\\release\\DM_Control.exe", disableHardware], 
#                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
#                        cwd=DMexePath, bufsize=1)



try:

#    DM.stdin.write("config\n")
#    DM.stdin.flush()

    #Original reference
    #nominal_motor_position=np.array([-0.159,5.003,6.675,8.196,6.393,6.175,9.413,6.927])
    # New ref 
    nominal_motor_position=np.array([-0.257     ,  6.279     ,  6.675     ,  8.196     ,  6.393     ,
            6.175     ,  9.48622106,  6.96294184])    #nominal_motor_position=np.array([-0.257,6.279,6.675,8.196,6.393,6.175,9.413,6.927])
    # New bis ref 
    #nominal_motor_position=np.array([-0.235,7.521,6.675,8.196,6.393,6.175,9.413,6.927])
    #Camera / L2 focus / L2 Y / L2 X / L2 y-tip / L2 x-tip / SM y-tip / SM x-tip
    
    
    Motors.Motors_Initialize()
    Motors.Motors_to_zero()
    Motors.Motors_Home()
    Motors.Motors_Nominal(nominal_motor_position)
    
    time.sleep(3)
    
    
    #run IDL Main_1
    subprocess.call(["C:\\Program Files\\Exelis\\IDL84\\bin\\bin.x86\\IDL.exe","-e","z_alignment_main1"])
    
    #Definition of the properties of the system: 
    with open('Z:\\Testbeds\\JOST\\Alignment\\data\\date_for_python.txt', 'r') as pf:
        Date_ = np.loadtxt(pf)

    Date=str(int(Date_[0]))+'-'+str(int(Date_[1]))+'-'+str(int(Date_[2]))+'-'+str(int(Date_[3]))+'h-'+str(int(Date_[4]))+'min'
        
    with open('Z:\Testbeds\JOST\Alignment\data\\'+Date+'\\python_config_file_'+Date+'.txt', 'r') as pf:
        configFile_python = np.loadtxt(pf)
        
    #FoV to define the Interaction matrix, and simulate images from a pertubation vector
    nb_FoV = (np.size(configFile_python)-6)/8
    
    #get all the images
    for ind in range(nb_FoV):
       
        #Steering mirror x-tip    
        Motors.Motor_absolute_move(8,nominal_motor_position[7]+configFile_python[8+ind*8])    
        #Steering mirror y-tip 
        Motors.Motor_absolute_move(7,nominal_motor_position[6]+configFile_python[9+ind*8])   
       
        #Images at Focus
        Motors.Motor_absolute_move(1,nominal_motor_position[0])     
        time.sleep(3) 
    
        LASER.stdin.write(str(current[1])+"\n")
        LASER.stdin.flush()       
        time.sleep(3)    
                
        Cam.Camera_Exposure(Date,configFile_python,Field_Number=ind+1,Type="Focus")
        time.sleep(3)
        
        LASER.stdin.write(str(current[0])+"\n")  
        LASER.stdin.flush()     
        time.sleep(3)    
            
        Cam.Camera_Exposure(Date,configFile_python,Field_Number=ind+1,Type="bg_Focus")
        time.sleep(3)         
       
        #Images at Defocus
        Motors.Motor_absolute_move(1,nominal_motor_position[0]-10.571) 
        time.sleep(3)
        
        LASER.stdin.write(str(current[2])+"\n")  
        LASER.stdin.flush()     
        time.sleep(3)    
                
        Cam.Camera_Exposure(Date,configFile_python,Field_Number=ind+1,Type="Defocus")
        time.sleep(3)    

    
        LASER.stdin.write(str(current[0])+"\n")       
        LASER.stdin.flush()
        time.sleep(3)    
               
        Cam.Camera_Exposure(Date,configFile_python,Field_Number=ind+1,Type="bg_Defocus")
        time.sleep(3)

    
    ##############################################################################################################################
    #PHASE DIVERSITY CALCULATION
    #run IDL Main_2
    subprocess.call(["C:\\Program Files\\Exelis\\IDL84\\bin\\bin.x86\\IDL.exe","-e","z_alignment_main2"])
    
    
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
    sensing_modes=sensing_modes+1
    nbr_sensing_modes=np.count_nonzero(sensing_modes)
    
    IM_bis=Zalign.decoup_line(IM,sensing_modes)
    measure_vect_bis=Zalign.decoup_element(measure_vect,sensing_modes)
    residual_vect_bis=Zalign.decoup_element(residual_vect,sensing_modes)    
    
    MMSE=np.zeros((4,nbr_iterations))
    LS=np.zeros((4,nbr_iterations))
    
    error_rms_MMSE=np.zeros((nbr_iterations))
    error_rms_LS=np.zeros((nbr_iterations))
    
    residual_vect_MMSE=np.zeros((nbr_zernikes*nb_FoV,nbr_iterations+1))
    residual_vect_MMSE[:,0]=residual_vect_bis
    residual_vect_LS=np.zeros((nbr_zernikes*nb_FoV,nbr_iterations+1))
    residual_vect_LS[:,0]=residual_vect_bis    
    
    
    #Loop on Zemax
    for ind in range(nbr_iterations):
    
        #For MMSE       
        MMSE[:,ind]=Zalign.MMSE_reconstruction_on_vectors(nb_FoV,noise_level,pert,IM_bis,measure_vect_bis,residual_vect_bis[:,ind])
        #WF simulated
        residual_vect_LS[:,ind+1]=Zalign.decoup_element(Zalign.Simulated_Wavefront_Zalignment_on_vector(field_vector,LS[:,ind],nbr_zernikes),sensing_modes)    
        #Correction quality
        error_rms_LS[ind]=result.distance(Zalign.Simulated_Wavefront_Zalignment_on_vector(field_vector,MMSE[:,ind],nbr_zernikes),measure_vect)
        
        #For LS        
        LS[:,ind]=Zalign.LS_reconstruction_on_vectors(cond_val,IM_bis,measure_vect_bis,residual_vect_bis[:,ind])
        #WF simulated
        residual_vect_LS[:,ind+1]=Zalign.decoup_element(Zalign.Simulated_Wavefront_Zalignment_on_vector(field_vector,LS[:,ind],nbr_zernikes),sensing_modes)    
        #Correction quality
        error_rms_LS[ind]=result.distance(Zalign.Simulated_Wavefront_Zalignment_on_vector(field_vector,LS[:,ind],nbr_zernikes),measure_vect)
        
    ################################################################################################################################
    
except: print "ENCOUNTERED PROBLEM, SHUTTING DOWN."


#raw_input("Press enter before shutting down")
   
## QUIT IRISAO DM:
#DM.stdin.write("quit\n")
#DM.stdin.close()   
#for line in DM.stdout: 
#    print line

# QUIT LASER SOURCE: 
LASER.stdin.write("quit\n")
LASER.stdin.close()
for line in LASER.stdout:
    print line
    