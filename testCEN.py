# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 16:34:11 2016

@author: egron
"""

import numpy as np
import zzdde_SylvainVersion as pzz

actuator_value=np.array([0.5,0.5,0.5,0.5])
alignment_state=np.zeros((4)) 

ind=0
field_vector=np.array([1000.,1000.])

#Creating IM for each iteration        
link = pzz.PyZZDDE()
link.zDDEInit()
link.zGetRefresh() 

#Set the field
link.zSetSurfaceParameter(9, 4, -field_vector[2*ind]/1000./2.)
link.zSetSurfaceParameter(9, 3, -field_vector[2*ind+1]/1000./2.)


#divide by 1000 because we work with milidegrees in the text file
#divide by two, because we have to put the half field on the surface coord breaf, for more information 
#check google doc JOST technical report, steering mirror. 
#L1    
# get the push
link.zSetSurfaceData(18, 3, alignment_state[0]+actuator_value[0])
link.zOptimize(1,0)
coefCENX_plus = link.zGetOperand(1,10)
coefCENY_plus = link.zGetOperand(2,10)
# get the pull
link.zSetSurfaceData(18, 3, alignment_state[0]-actuator_value[0])
link.zOptimize(1,0)
coefCENX_minus = link.zGetOperand(1,10)
coefCENY_minus = link.zGetOperand(2,10)
#reset
link.zSetSurfaceData(18, 3, 0.0)

# IM computation
coefCENX = (coefCENX_plus - coefCENX_minus) / (2 * actuator_value[0])
coefCENY = (coefCENY_plus - coefCENY_minus) / (2 * actuator_value[0])

link.zSetSurfaceParameter(9, 3, 0)
link.zSetSurfaceParameter(9, 4, 0)
link.zOptimize(1,0)
# close the DDE link
status = link.zDDEClose()