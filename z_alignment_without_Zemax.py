# -*- coding: utf-8 -*-
"""
Created on Mon May 09 14:11:07 2016

@author: jost
"""


import time
import subprocess
#from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf as pbp
from PIL import Image
import Last_Camera_Function as Cam
import Last_Motor_Function as Motors
import XPS_Q8_drivers 
import sys


######################################################################################################################
#GETTING THE IMAGES

#Connect to DM and Laser

LASERexePath = "C:\\Users\\jost\\Desktop\\SourceLaser\\debug\\"

channel=1
current=43.88

LASER = subprocess.Popen(["C:\\Users\\jost\\Desktop\\SourceLaser\\debug\\SourceLaser.exe", str(channel), str(current)], 
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                        cwd=LASERexePath, bufsize=1)
current=[0,50,53]
####DM Initialisation
#disableHardware = "false"
#DMexePath = "C:\\Users\\jost\\Desktop\\Control DM\\Code\\release"
#DM = subprocess.Popen(["C:\\Users\\jost\\Desktop\\Control DM\\Code\\release\\DM_Control.exe", disableHardware], 
#                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
#                        cwd=DMexePath, bufsize=1)
#
#DM.stdin.write("config\n")
#DM.stdin.flush()



#Original reference
#nominal_motor_position=np.array([-0.159,5.003,6.675,8.196,6.393,6.175,9.413,6.927])
# New ref 
nominal_motor_position=np.array([-0.257,6.279,6.675,8.196,6.393,6.175,9.413,6.927])
# New bis ref 
#nominal_motor_position=np.array([-0.235,7.521,6.675,8.196,6.393,6.175,9.413,6.927])
#Camera / L2 focus / L2 Y / L2 X / L2 y-tip / L2 x-tip / SM y-tip / SM x-tip

#Original
#L1 5.478
#L3 7.265

# New ref 
#L1 6.401
#L3 8.011

# New bis ref 
#L1 7.311
#L3 8.945



#Motors.Motors_Initialize()
#Motors.Motors_to_zero()
#Motors.Motors_Home()
Motors.Motors_Nominal(nominal_motor_position)

time.sleep(3)


#run IDL Main_1
subprocess.call(["C:\\Program Files\\Exelis\\IDL84\\bin\\bin.x86\\IDL.exe","-e","Zalignment_main1"])

#Definition of the properties of the system: 
with open('Z:\Testbeds\JOST\Alignment\data\ConfigFile_read.txt', 'r') as pf:
    ConfigFile = np.loadtxt(pf)

with open('Z:\Testbeds\JOST\Alignment\data\\'+str(int(ConfigFile[0]))+'\\ConfigFile_Labview_'+str(int(ConfigFile[0]))+'.txt', 'r') as pf:
    ConfigFile_Labview = np.loadtxt(pf)

#FoV to define the Interaction matrix, and simulate images from a pertubation vector
nb_FoV = (np.size(ConfigFile)-7)/2

#get backgroung images
#Cam.Camera_Exposure(ConfigFile_Labview,Field_Number=1,Type="bg")
#time.sleep(2)
#Cam.Camera_Exposure(ConfigFile_Labview,Field_Number=1,Type="bg")

#get all the images
for ind in range(nb_FoV):
   
    #Steering mirror x-tip    
    Motors.Motor_absolute_move(8,nominal_motor_position[7]+ConfigFile_Labview[9+ind*8])    
    #Steering mirror y-tip 
    Motors.Motor_absolute_move(7,nominal_motor_position[6]+ConfigFile_Labview[10+ind*8])   
   
    #Images at Focus
    Motors.Motor_absolute_move(1,nominal_motor_position[0])     
    time.sleep(3) 

    LASER.stdin.write(str(current[1])+"\n")
    LASER.stdin.flush()       
    time.sleep(3)    
            
    Cam.Camera_Exposure(ConfigFile_Labview,Field_Number=ind+1,Type="Focus")
    time.sleep(3)
    Cam.Camera_Exposure(ConfigFile_Labview,Field_Number=ind+1,Type="Focus")
    time.sleep(3)
    
    LASER.stdin.write(str(current[0])+"\n")  
    LASER.stdin.flush()     
    time.sleep(3)    
        
    Cam.Camera_Exposure(ConfigFile_Labview,Field_Number=ind+1,Type="bg_Focus")
    time.sleep(3)
    Cam.Camera_Exposure(ConfigFile_Labview,Field_Number=ind+1,Type="bg_Focus")
    
    #Images at Defocus
    Motors.Motor_absolute_move(1,nominal_motor_position[0]-10.571) 
    time.sleep(3)
    
    LASER.stdin.write(str(current[2])+"\n")  
    LASER.stdin.flush()     
    time.sleep(3)    
            
    Cam.Camera_Exposure(ConfigFile_Labview,Field_Number=ind+1,Type="Defocus")
    time.sleep(3)    
    Cam.Camera_Exposure(ConfigFile_Labview,Field_Number=ind+1,Type="Defocus")
    time.sleep(3)

    LASER.stdin.write(str(current[0])+"\n")       
    LASER.stdin.flush()
    time.sleep(3)    
           
    Cam.Camera_Exposure(ConfigFile_Labview,Field_Number=ind+1,Type="bg_Defocus")
    time.sleep(3)    
    Cam.Camera_Exposure(ConfigFile_Labview,Field_Number=ind+1,Type="bg_Defocus")


##############################################################################################################################
#PHASE DIVERSITY CALCULATION
#run IDL Main_2
subprocess.call(["C:\\Program Files\\Exelis\\IDL84\\bin\\bin.x86\\IDL.exe","-e","LLZalignment_main2"])




#DM
#creation fichier .ini fonction python Charles
#move DM
#DM.stdin.write("config\n")
#DM.stdin.flush()
#fin de boucle close DM
#DM.stdin.write("quit\n")
#DM.stdin.close()
#
#for line in DM.stdout: 
#    print line

LASER.stdin.write("quit\n")
LASER.stdin.close()