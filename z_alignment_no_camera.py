# -*- coding: utf-8 -*-
"""
Created on Mon May 30 11:27:34 2016

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
import z_alignment_functions_no_camera as Zalign



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
            6.175     ,  9.48622106,  6.96294184])
    #nominal_motor_position=np.array([-0.257,6.279,6.675,8.196,6.393,6.175,9.413,6.927])
    # New bis ref 
    #nominal_motor_position=np.array([-0.235,7.521,6.675,8.196,6.393,6.175,9.413,6.927])
    #Camera / L2 focus / L2 Y / L2 X / L2 y-tip / L2 x-tip / SM y-tip / SM x-t♥ip


    
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
    

        #Number of Zernikes to descibre the Wavefront (Piston, Tip and Tilt are not included): 
        #It's number of zernike I get from the phase diversity. 
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
    print "lens alignment Zemaxe)"
    print "move L1 by ",Misalignment[0],"mm"    
    print "move L2 by ",Misalignment[1],"mm"    
    print "move L3 by ",Misalignment[2],"mm"    
    
    
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
    