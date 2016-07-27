# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 15:01:54 2016

@author: egron
"""

from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf as pbp
from PIL import Image
#import pyzdde.zdde as pyz
#import zzdde_SylvainVersion as pzz

#import PyWFS as pwf
#import pyao_SylvainVersion as ao


###############################################################################
######                             SVD Study                                ######
###############################################################################


##############################################################################
#Definition of the properties of the system: 

#FoV to define the Interaction matrix, and simulate images from a pertubation vector
nb_WFS = 4

Zmax = 18

Pmax = 16
###############################################################################
# Inter Matrix
fName_IM = "Z:\Testbeds\JOST\Alignment\data\20160519\InterMatrix"
fName_IM += "\Field1X0_Field1Y0.txt"

with open(fName_IM, 'r') as pf:
        IM = np.loadtxt(pf)

U,S,V=np.linalg.svd(IM)
#IM_rec=np.dot(np.dot(U,np.diag(S)),V)
qwerty = "Z:\Testbeds\JOST\Linear_Control"
qwerty += "\SVD.txt"
with open(qwerty, 'a') as pf:
        np.savetxt(pf, V, fmt='%.15f')
    
cond_val=0.01
MI=np.linalg.pinv(IM, cond_val)

#Looking at focus only, for top left corner (field -1000,-1000,  +0.5,+0.5 on Zemax)
A=np.array(([589,-462.6,-103],[-6.51,7.66,-0.71]))
U,S,V=np.linalg.svd(A)
cond_val=0.01
Ainv=np.linalg.pinv(A, cond_val)
phi=np.array([105.8,-30.2])
phi_residual=np.array([11.48,-11.35])
P=np.dot(Ainv,phi-phi_residual)
np.set_printoptions(precision=2)