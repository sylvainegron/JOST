# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 09:24:21 2016

@author: egron
"""


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf as pbp
from PIL import Image
import pylab as pylab

# FOR  DEGREE FoV
nb_steps=11
total_translation=0.6
abscisse=np.arange(nb_steps)*total_translation/(nb_steps-1)-total_translation/2.

#Zemax simulations
with open('Z:\\Testbeds\\JOST\\Alignment\\data\\2016-6-16-16h-28min\\InterMatrix\\Field1X0_Field1Y0_Field2X1000_Field2Y-1000_Field3X-1000_Field3Y-1000_Field4X1000_Field4Y1000_Field5X-1000_Field5Y1000_.txt', 'r') as pf:
    IM = np.loadtxt(pf)
    
with open('Z:\\Testbeds\\JOST\Alignment\\data\\2016-6-16-16h-28min\\Residual_Wavefront\\Field1X0_Field1Y0_Field2X1000_Field2Y-1000_Field3X-1000_Field3Y-1000_Field4X1000_Field4Y1000_Field5X-1000_Field5Y1000_.txt', 'r') as pf:
    phi_0 = np.loadtxt(pf)
#Zernike=4
#Lens=2
#Z4L2 = IM[Zernike-4,Lens-1]*abscisse+phi_0[Zernike-4]
Z4L1 = IM[4-4+18,1-1]*abscisse+phi_0[4-4+18]
Z4L2 = IM[4-4+18,2-1]*abscisse+phi_0[4-4+18]
Z4L3 = IM[4-4+18,3-1]*abscisse+phi_0[4-4+18]

Z5L1 = IM[5-4+18,1-1]*abscisse+phi_0[5-4+18]
Z5L2 = IM[5-4+18,2-1]*abscisse+phi_0[5-4+18]
Z5L3 = IM[5-4+18,3-1]*abscisse+phi_0[5-4+18]

x=abscisse
#y=Z4L1
#plt.plot(x, y)
#plt.ylabel('Wavefront Peak to Valley (nm)')
#plt.xlabel('Lens position (mm). The origin is the position of the aligned lens')

pylab.plot(x, Z4L1, '-b', label='L1')
pylab.plot(x, Z4L2, '-r', label='L2')
pylab.plot(x, Z4L3, '-c', label='L3')
pylab.legend(loc='upper left')
pylab.xlabel('Longitudinal shift (mm)')
pylab.ylabel('Z4 defocus aberration in Peak to Valley (nm)')
pylab.xlim(-0.3, 0.3)

pylab.plot(x, Z5L1, '-b', label='L1')
pylab.plot(x, Z5L2, '-r', label='L2')
pylab.plot(x, Z5L3, '-c', label='L3')
pylab.legend(loc='upper left')
pylab.xlabel('Longitudinal shift (mm)')
pylab.ylabel('Z5 astigmatism aberration in Peak to Valley (nm)')
pylab.xlim(-0.3, 0.3)


def get_data(Name_of_the_folder, number_of_figures_per_text_file,number_of_textfile):
     
    data_in_matrix=np.zeros((number_of_figures_per_text_file,number_of_textfile))
    for i in range(number_of_textfile):
        fName_measure=Name_of_the_folder+str(i+1)+'.txt'
        with open(fName_measure, 'r') as pf:
            data = np.loadtxt(pf)
        data_in_matrix[:,i]=data #We don't take the tip and tilt coef values of the measure vector   
       
    return data_in_matrix

    
data_in_matrix=get_data('Z:\\Testbeds\\JOST\\Alignment\\data\\aberration_vs_L2_motion\\aberration_vs_L2_motion_step',20,11)
plt.plot(data_in_matrix[2,:])

data_in_matrix_bis=get_data('Z:\\Testbeds\\JOST\\Alignment\\data\\aberration_vs_L2_motion\\result6-17-16\\aberration_vs_L2_motion_step',20,11)
plt.plot(data_in_matrix_bis[2,:]) 

#older version: 
zemax=np.array([52,25,-2,-29,-56])
plt.plot(zemax)
plt.plot(data_in_matrix[2,3:7])
zemax=np.array([133,106,79,52,25,-2,-29,-56,-83,-110,-137])
plt.plot(zemax)
plt.plot(data_in_matrix[2,3:8])
zemax=np.array([52,25,-2,-29,-56])
plt.plot(zemax)
