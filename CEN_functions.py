# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 17:04:46 2016

@author: egron
"""
import numpy as np
import zzdde_SylvainVersion as pzz
#import zdde as pzz

def IM_CEN(field_vector,actuator_value,alignment_state):
    #nbr_zernikes is the number of zernikes calculated started with Z4
    nb_FoV=np.size(field_vector)/2
    IM_CEN = np.zeros((2*nb_FoV,4))  
    
    for ind in range(nb_FoV):
    
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
        #IM filling
        IM_CEN[ind*2:(ind+1)*2,0] = np.array([coefCENX,coefCENY])
    
        #L2
        # get the push
        link.zSetSurfaceData(24, 3,alignment_state[1]+actuator_value[1])
        link.zOptimize(1,0)
        coefCENX_plus = link.zGetOperand(1,10)
        coefCENY_plus = link.zGetOperand(2,10)    
        # get the pull
        link.zSetSurfaceData(24, 3, alignment_state[1]-actuator_value[1])
        link.zOptimize(1,0)
        coefCENX_minus = link.zGetOperand(1,10)
        coefCENY_minus = link.zGetOperand(2,10)    
        #reset
        link.zSetSurfaceData(24, 3, 0.0)    
        # IM computation
        coefCENX = (coefCENX_plus - coefCENX_minus) / (2 * actuator_value[1])
        coefCENY = (coefCENY_plus - coefCENY_minus) / (2 * actuator_value[1])
        #IM filling
        IM_CEN[ind*2:(ind+1)*2,1] = np.array([coefCENX,coefCENY])
           
        #L3   
        # get the push
        link.zSetSurfaceData(31, 3, alignment_state[2]+actuator_value[2])
        link.zOptimize(1,0)
        coefCENX_plus = link.zGetOperand(1,10)
        coefCENY_plus = link.zGetOperand(2,10)  
        # get the pull
        link.zSetSurfaceData(31, 3, alignment_state[2]-actuator_value[2])
        link.zOptimize(1,0)
        coefCENX_minus = link.zGetOperand(1,10)
        coefCENY_minus = link.zGetOperand(2,10)
        #reset
        link.zSetSurfaceData(31, 3, 0.0)
        # IM computation
        coefCENX = (coefCENX_plus - coefCENX_minus) / (2 * actuator_value[2])
        coefCENY = (coefCENY_plus - coefCENY_minus) / (2 * actuator_value[2])
        #IM filling
        IM_CEN[ind*2:(ind+1)*2,2] = np.array([coefCENX,coefCENY])
        
        #Camera    
        # get the push
        link.zSetSurfaceData(39, 3,alignment_state[3]+actuator_value[3])
        link.zOptimize(1,0)
        coefCENX_plus = link.zGetOperand(1,10)
        coefCENY_plus = link.zGetOperand(2,10)  
        # get the pull
        link.zSetSurfaceData(39, 3, alignment_state[3]-actuator_value[3])
        link.zOptimize(1,0)
        coefCENX_minus = link.zGetOperand(1,10)
        coefCENY_minus = link.zGetOperand(2,10)
        #reset
        link.zSetSurfaceData(39, 3, 0.0)
        # IM computation
        coefCENX = (coefCENX_plus - coefCENX_minus) / (2 * actuator_value[3])
        coefCENY = (coefCENY_plus - coefCENY_minus) / (2 * actuator_value[3])
        #IM filling
        IM_CEN[ind*2:(ind+1)*2,3] = np.array([coefCENX,coefCENY])
        
        
        link.zSetSurfaceParameter(9, 3, 0)
        link.zSetSurfaceParameter(9, 4, 0)
        link.zOptimize(1,0)
        # close the DDE link
        status = link.zDDEClose()
     
        
        return IM_CEN

###############################################################################################  
def simulated_CEN(field_vector,alignment_state):
    
    #nbr_zernikes is the number of zernikes calculated started with Z4
    nb_FoV=np.size(field_vector)/2 
    CEN_simulation = np.zeros((2*nb_FoV)) 
    
    for ind in range(nb_FoV):
        link = pzz.PyZZDDE()
        link.zDDEInit()
        link.zGetRefresh() 
       
        link.zSetSurfaceParameter(9, 4, -field_vector[2*ind]/1000./2.)
        link.zSetSurfaceParameter(9, 3, -field_vector[2*ind+1]/1000./2.)   
    
        
        ########################################################################################################
        # Move the the elements
        
        # Move the elements   
        link.zSetSurfaceData(18, 3, alignment_state[0] )
        link.zSetSurfaceData(24, 3, alignment_state[1])  
        link.zSetSurfaceData(31, 3, alignment_state[2]) 
        link.zSetSurfaceData(39, 3, alignment_state[3])         
        link.zOptimize(1,0)

        coefCENX = link.zGetOperand(1,10)
        coefCENY = link.zGetOperand(2,10)
        

        #IM filling
        CEN_simulation[ind*2:(ind+1)*2] = np.array([coefCENX,coefCENY])
        #Reset positions      
        link.zSetSurfaceParameter(9, 4, 0)
        link.zSetSurfaceParameter(9, 3, 0)    
        link.zSetSurfaceData(18, 3, 0 )
        link.zSetSurfaceData(24, 3, 0 )  
        link.zSetSurfaceData(31, 3, 0 ) 
        link.zSetSurfaceData(39, 3, 0 ) 
        link.zOptimize(1,0)
        # close the DDE link
        status = link.zDDEClose()
           
    return CEN_simulation