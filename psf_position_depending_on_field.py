# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 14:43:48 2016

@author: egron
"""
import numpy as np
import CEN_functions as CEN
import pylab as pylab
#give the position of the PSF depending on the field of veiw, can be helpfull for the crop of the images

pixel_size=0.009

#For focus images
field_vector=np.array([0,0,0.1,0.1,0.2,0.2,0.3,0.3,0.4,0.4,0.5,0.5,0.6,0.6,0.7,0.7,0.8,0.8,0.9,0.9,1.,1.])
A=CEN.simulated_CEN(field_vector,np.array([0,0,0,0]))
B=np.zeros((11))
C=np.zeros((11))
abscisse=np.zeros((11))
for i in range (11):
    B[i]=A[2*i]
    C[i]=A[2*i+1]
    abscisse[i]=field_vector[2*i]
    
pylab.plot(abscisse, B, '-b')

pente_focus=B[10]-B[0]
pente_focus_pxl=pente_focus/pixel_size
#C[10]-C[0] and B[10]-B[0] give the pente of the curve, so if you divide it by the pixel size,
# you should get the position of the center of the crop that we calculate on IDL. 
#That should happen at least when the testbed is aligned. OUr calcualtion show that 
#The IDL value 'from_field_angle_in_degree_to_focus_psf_position_in_pixel' should be 1.16

#For defocus images
camera_translation=10.571
field_vector=np.array([0,0,0.1,0.1,0.2,0.2,0.3,0.3,0.4,0.4,0.5,0.5,0.6,0.6,0.7,0.7,0.8,0.8,0.9,0.9,1.,1.])
AA=CEN.simulated_CEN(field_vector,np.array([0,0,0,camera_translation]))
BB=np.zeros((11))
CC=np.zeros((11))
abscisse=np.zeros((11))
for i in range (11):
    BB[i]=AA[2*i]
    CC[i]=AA[2*i+1]
    abscisse[i]=field_vector[2*i]
    
pylab.plot(abscisse, BB, '-b')
pente_defocus=BB[10]-BB[0]
pente_defocus_pxl=pente_defocus/pixel_size
#pente defocus=1.22