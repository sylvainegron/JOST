# -*- coding: utf-8 -*-
"""
Created on Wed May 11 16:46:56 2016

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

#Check Nb_Images, NP, total_translation_of_the_Camera, and the path are the same as in the IDL file "Last Field Alignment"


LASERexePath = "C:\\Users\\jost\\Desktop\\SourceLaser\\debug\\"

channel=1
current=43.88

LASER = subprocess.Popen(["C:\\Users\\jost\\Desktop\\SourceLaser\\debug\\SourceLaser.exe", str(channel), str(current)], 
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                        cwd=LASERexePath, bufsize=1)
current=[0,49]

nominal_motor_position=np.array([-0.257     ,  6.279     ,  6.675     ,  8.196     ,  6.393     ,
        6.175     ,  9.48622106,  6.96294184])
#Camera / L2 focus / L2 Y / L2 X / L2 y-tip / L2 x-tip / SM y-tip / SM x-tip

Motors.Motors_Initialize()
Motors.Motors_to_zero()
Motors.Motors_Home()
Motors.Motors_Nominal(nominal_motor_position)

time.sleep(3)

LASER.stdin.write(str(current[1])+"\n")
LASER.stdin.flush()       
time.sleep(3)   

Cam.Take_Image(1000,5,2048,2048,'Z:\Testbeds\JOST\Alignment\\data\\Field_alignment\\image')
time.sleep(3)


LASER.stdin.write(str(current[0])+"\n")
LASER.stdin.flush()       
time.sleep(3)

Cam.Take_Image(1000,5,2048,2048,'Z:\Testbeds\JOST\Alignment\\data\\Field_alignment\\bg')
time.sleep(3)    


subprocess.call(["C:\\Program Files\\Exelis\\IDL84\\bin\\bin.x86\\IDL.exe","-e","LLField_alignment"])

with open('Z:\Testbeds\JOST\Alignment\\data\\Field_alignment\\Field_Alignment_for_Python.txt', 'r') as pf:
    Field_alignment = np.loadtxt(pf)



        
nominal_motor_position[6]=nominal_motor_position[6]+Field_alignment[1]
nominal_motor_position[7]=nominal_motor_position[7]+Field_alignment[0]

Motors.Motors_Initialize()
Motors.Motors_to_zero()
Motors.Motors_Home()
Motors.Motors_Nominal(nominal_motor_position)
time.sleep(3)

LASER.stdin.write(str(current[1])+"\n")
LASER.stdin.flush()       
time.sleep(3)

Cam.Take_Image(1000,5,2048,2048,'Z:\Testbeds\JOST\Alignment\\data\\Field_alignment\\Result')
time.sleep(3)


LASER.stdin.write("quit\n")
LASER.stdin.close()
