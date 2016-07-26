# -*- coding: utf-8 -*-
"""
Created on Fri May 06 13:54:39 2016

@author: egron
"""

#This function will translate the Camera taking images at each step. Calculating the center of gravitiy, 
#we can check if the camera axis of translation is aligned with the 0 degre field of view.  

import time
import subprocess
#from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf as pbp
from PIL import Image
import camera_functions as Cam
import motors_functions as Motors
import XPS_Q8_drivers 
import sys

#Check Nb_Images, NP, total_translation_of_the_Camera, and the path are the same as in the IDL file "Last Camera Alignment"

LASERexePath = "C:\\Users\\jost\\Desktop\\SourceLaser\\debug\\"

channel=1
current=43.88

LASER = subprocess.Popen(["C:\\Users\\jost\\Desktop\\SourceLaser\\debug\\SourceLaser.exe", str(channel), str(current)], 
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                        cwd=LASERexePath, bufsize=1)
current=[0,53]

nominal_motor_position=np.array([-0.257     ,  6.279     ,  6.675     ,  8.196     ,  6.393     ,
        6.175     ,  9.48622106,  6.96294184])
#Camera / L2 focus / L2 Y / L2 X / L2 y-tip / L2 x-tip / SM y-tip / SM x-tip

#Motors.Motors_Initialize()
#Motors.Motors_to_zero()
#Motors.Motors_Home()
Motors.Motors_Nominal(nominal_motor_position)
time.sleep(3)

#Images close to L3
Motors.Motor_absolute_move(1,nominal_motor_position[0]+10)     
time.sleep(3)

LASER.stdin.write(str(current[1])+"\n")
LASER.stdin.flush()       
time.sleep(3)   

Cam.Take_Image(400,5,2048,2048,'Z:\Testbeds\JOST\Alignment\data\\Camera_alignment\close_to_L3')
time.sleep(3)

LASER.stdin.write(str(current[0])+"\n")
LASER.stdin.flush()       
time.sleep(3)

Cam.Take_Image(400,5,2048,2048,'Z:\Testbeds\JOST\Alignment\\data\\Camera_alignment\\bg_close_to_L3')
time.sleep(3)    

#Images far from L3
Motors.Motor_absolute_move(1,nominal_motor_position[0]-10) 
time.sleep(3)

LASER.stdin.write(str(current[1])+"\n")
LASER.stdin.flush()       
time.sleep(3)

Cam.Take_Image(400,5,2048,2048,'Z:\Testbeds\JOST\Alignment\\data\\Camera_alignment\\far_from_L3')
time.sleep(3)    

LASER.stdin.write(str(current[0])+"\n")
LASER.stdin.flush()       
time.sleep(3)

Cam.Take_Image(400,5,2048,2048,'Z:\Testbeds\JOST\Alignment\\data\\Camera_alignment\\bg_far_from_L3')
time.sleep(3)    

subprocess.call(["C:\\Program Files\\Exelis\\IDL84\\bin\\bin.x86\\IDL.exe","-e","camera_alignment"])

LASER.stdin.write("quit\n")
LASER.stdin.close()
