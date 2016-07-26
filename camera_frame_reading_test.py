# -*- coding: utf-8 -*-
"""
Created on Tue May 24 11:31:10 2016

@author: jost
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


channel=1
current=0.0
LASERexePath = "C:\\Users\\jost\\Desktop\\SourceLaser\\debug\\"
LASER = subprocess.Popen(["C:\\Users\\jost\\Desktop\\SourceLaser\\debug\\SourceLaser.exe", str(channel), str(current)], 
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                        cwd=LASERexePath, bufsize=1)
current=[0,48.7,50.0]

nominal_motor_position=np.array([-0.257     ,  6.279     ,  6.675     ,  8.196     ,  6.393     ,
            6.175     ,  9.48622106,  6.96294184])
Motors.Motors_Nominal(nominal_motor_position)

print "a"
LASER.stdin.write(str(current[1])+"\n")
LASER.stdin.flush()       
time.sleep(20)    
        
Cam.Take_Image_no_time_sleep(100,90,2048,2048,'Z:\Testbeds\JOST\Alignment\\data\\test_focus')
time.sleep(3)
Cam.Take_Image_no_time_sleep(100,90,2048,2048,'Z:\Testbeds\JOST\Alignment\\data\\test_focus')
time.sleep(3)

LASER.stdin.write(str(current[0])+"\n")  
LASER.stdin.flush()     
time.sleep(3)    
    
Cam.Take_Image_no_time_sleep(100,90,2048,2048,'Z:\Testbeds\JOST\Alignment\\data\\test_bg_focus')
time.sleep(3) 
Cam.Take_Image_no_time_sleep(100,90,2048,2048,'Z:\Testbeds\JOST\Alignment\\data\\test_bg_focus')
time.sleep(3)         

#Images at Defocus
Motors.Motor_absolute_move(1,nominal_motor_position[0]-10.571) 
time.sleep(3)

LASER.stdin.write(str(current[2])+"\n")  
LASER.stdin.flush()     
time.sleep(3)    
        
Cam.Take_Image_no_time_sleep(100,90,2048,2048,'Z:\Testbeds\JOST\Alignment\\data\\test_defocus')
time.sleep(3)    
Cam.Take_Image_no_time_sleep(100,90,2048,2048,'Z:\Testbeds\JOST\Alignment\\data\\test_defocus')
time.sleep(3) 

LASER.stdin.write(str(current[0])+"\n")       
LASER.stdin.flush()
time.sleep(3)    
       
Cam.Take_Image_no_time_sleep(100,90,2048,2048,'Z:\Testbeds\JOST\Alignment\\data\\test_bg_defocus')
time.sleep(3)
Cam.Take_Image_no_time_sleep(100,90,2048,2048,'Z:\Testbeds\JOST\Alignment\\data\\test_bg_defocus')
time.sleep(3)    

LASER.stdin.write("quit\n")
LASER.stdin.close()
for line in LASER.stdout:
    print line
