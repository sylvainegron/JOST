# -*- coding: utf-8 -*-
"""
Created on Wed Jun 01 11:00:06 2016

@author: jost
"""


import time
import subprocess
#from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf as pbp
from PIL import Image
#import pyzdde.zdde as pyz
#import zzdde_SylvainVersion as pzz
import camera_functions as Cam
import motors_functions as Motors
import XPS_Q8_drivers 
import sys
#import Last_z_alignment_functions as Zalign



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

print 'yaaa'

try:

#    DM.stdin.write("config\n")
#    DM.stdin.flush()

   
    nominal_motor_position=np.array([-0.257     ,  6.279     ,  6.675     ,  8.196     ,  6.393     ,
            6.175     ,  9.48622106,  6.96294184])   
   
    #Camera / L2 focus / L2 Y / L2 X / L2 y-tip / L2 x-tip / SM y-tip / SM x-tip
    
    
    Motors.Motors_Initialize()
    Motors.Motors_to_zero()
    Motors.Motors_Home()
    Motors.Motors_Nominal(nominal_motor_position)
    
    time.sleep(3)
    
    Field=np.array([0.,0.])
    NP=200
    nb_images=30
    NM=20
    nb_steps=11
    total_translation=0.6
    Defocus = np.zeros((nb_steps,NM)) 
    print 'oupla'
    #Steering mirror x-tip    
    Motors.Motor_absolute_move(8,nominal_motor_position[7]-Field[0]*525./1000/1000)    
    #Steering mirror y-tip 
    Motors.Motor_absolute_move(7,nominal_motor_position[6]-Field[1]*525./1000/1000)   
    
    print 'hep'
    time.sleep(1)

    #Moving L2 along the z axis, getting all the images
    for ind in range(nb_steps):
        #L2 motion       
        print 'wert'
        time.sleep(1)        
        Motors.Motor_absolute_move(2,nominal_motor_position[1]-total_translation/2.+total_translation*ind/(nb_steps-1))
                
        time.sleep(3)  
        print 'voila!'
        time.sleep(1)
        #Images at Focus
        Motors.Motor_absolute_move(1,nominal_motor_position[0])     
        time.sleep(3) 
        print 'yo'
        LASER.stdin.write(str(current[1])+"\n")
        LASER.stdin.flush()       
        time.sleep(3)    
                
        Cam.Take_Image(NP,nb_images,2048-NP/2.+Field[0]*1.1935,2048-NP/2.+Field[1]*1.1935,"Z:\Testbeds\JOST\Alignment\\data\\aberration_vs_L2_motion\\Focus_step"+str(int(ind+1))+"_frame")
        time.sleep(3)
        
        LASER.stdin.write(str(current[0])+"\n")  
        LASER.stdin.flush()     
        time.sleep(3)    
            
        Cam.Take_Image(NP,nb_images,2048-NP/2.+Field[0]*1.1935,2048-NP/2.+Field[1]*1.1935,"Z:\Testbeds\JOST\Alignment\\data\\aberration_vs_L2_motion\\bg_Focus_step"+str(int(ind+1))+"_frame")
        time.sleep(3)         
       
        #Images at Defocus
        Motors.Motor_absolute_move(1,nominal_motor_position[0]-10.571) 
        time.sleep(3)
        
        LASER.stdin.write(str(current[2])+"\n")  
        LASER.stdin.flush()     
        time.sleep(3)    
                
        Cam.Take_Image(NP,nb_images,2048-NP/2.+Field[0]*1.254,2048-NP/2.+Field[1]*1.254,"Z:\Testbeds\JOST\Alignment\\data\\aberration_vs_L2_motion\\Defocus_step"+str(int(ind+1))+"_frame")
        time.sleep(3)    
    
    
        LASER.stdin.write(str(current[0])+"\n")       
        LASER.stdin.flush()
        time.sleep(3)    
               
        Cam.Take_Image(NP,nb_images,2048-NP/2.+Field[0]*1.254,2048-NP/2.+Field[1]*1.254,"Z:\Testbeds\JOST\Alignment\\data\\aberration_vs_L2_motion\\bg_Defocus_step"+str(int(ind+1))+"_frame")
        time.sleep(3)
    
        
    ##############################################################################################################################
    #PHASE DIVERSITY CALCULATION
    #run IDL Main_2
    subprocess.call(["C:\\Program Files\\Exelis\\IDL84\\bin\\bin.x86\\IDL.exe","-e","jacobian_experimental"])
    
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
    