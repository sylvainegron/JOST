# -*- coding: utf-8 -*-
"""
Created on Mon May 30 11:29:57 2016

@author: egron
"""

import numpy as np
#import matplotlib.pyplot as plt
#import matplotlib.backends.backend_pdf as pbp
#from PIL import Image
#import pyzdde.zdde as pyz
import zzdde_SylvainVersion as pzz
import pyao_SylvainVersion as ao
###################################################################################################
def InterMatrix_Zalignment(date_time,ConfigFile,actuator_values):
    
    
    nb_FoV = (np.size(ConfigFile)-6)/8
    Zmax = ConfigFile[4]-2
    fName_IM_firstpart="Z:\Testbeds\JOST\Alignment\data\\"+date_time+"\\InterMatrix\\"
    fName_IM_secondpart=""
    for i in range(nb_FoV):
        fName_IM_secondpart += "Field"+str(int(i+1))+"X"+str(int(ConfigFile[6+8*i]))+"_Field"+str(int(i+1))+"Y"+str(int(ConfigFile[7+8*i]))+"_"

    fName_IM_secondpart += ".txt"
    fName_IM=fName_IM_firstpart+fName_IM_secondpart


    #Interaction matrix 
    IM = np.zeros((Zmax*nb_FoV,3)) 

    for ind in range(nb_FoV):
        link = pzz.PyZZDDE()
        link.zDDEInit()
        link.zGetRefresh() 
        # get the wavelenght
        wavesTuple = link.zGetWaveTuple()
        wave = wavesTuple[0][0] * 1000.0 # unit: lambda <-> nm
        link.zSetSurfaceParameter(9, 4, -ConfigFile[6+8*ind]/1000./2.)
        link.zSetSurfaceParameter(9, 3, -ConfigFile[6+8*ind+1]/1000./2.)
        #divide by 1000 because we work with milidegrees in the text file
        #divide by two, because we have to put the half field on the surface coord breaf, for more information 
        #check google doc JOST technical report, steering mirror. 
        #L1    
        # get the push
        link.zSetSurfaceData(18, 3, actuator_values[0])
        coefZern_plus = link.zGetZernikeCoef(Zmax=153)
        # get the pull
        link.zSetSurfaceData(18, 3, -actuator_values[0])
        coefZern_minus = link.zGetZernikeCoef(Zmax=153)
        #reset
        link.zSetSurfaceData(18, 3, 0.0)
        # IM computation
        coefZern_IM = (coefZern_plus - coefZern_minus) / (2 * actuator_values[0])
        #IM filling
        IM[ind*Zmax:(ind+1)*Zmax,0] = coefZern_IM[3:Zmax+3]
    
        #L2
        # get the push
        link.zSetSurfaceData(24, 3, actuator_values[1])
        coefZern_plus = link.zGetZernikeCoef(Zmax=153)    
        # get the pull
        link.zSetSurfaceData(24, 3, -actuator_values[1])
        coefZern_minus = link.zGetZernikeCoef(Zmax=153)    
        #reset
        link.zSetSurfaceData(24, 3, 0.0)    
        # IM computation
        coefZern_IM = (coefZern_plus - coefZern_minus) / (2 * actuator_values[1])
        #IM filling
        IM[ind*Zmax:(ind+1)*Zmax,1] = coefZern_IM[3:Zmax+3]
           
        #L3   
        # get the push
        link.zSetSurfaceData(31, 3, actuator_values[2])
        coefZern_plus = link.zGetZernikeCoef(Zmax=153)
        # get the pull
        link.zSetSurfaceData(31, 3, -actuator_values[2])
        coefZern_minus = link.zGetZernikeCoef(Zmax=153)
        #reset
        link.zSetSurfaceData(31, 3, 0.0)
        # IM computation
        coefZern_IM = (coefZern_plus - coefZern_minus) / (2 * actuator_values[2])
        #IM filling
        IM[ind*Zmax:(ind+1)*Zmax,2] = coefZern_IM[3:Zmax+3]
    
        
        
        link.zSetSurfaceParameter(9, 3, 0)
        link.zSetSurfaceParameter(9, 4, 0)
        
        # close the DDE link
        status = link.zDDEClose()
     
    IM=IM*wave 
    # save the interaction matrix in a file
    with open(fName_IM, 'w') as pf:
        np.savetxt(pf, IM , fmt='%.15f')
        
    return IM
        
#######################################################################################################
#######################################################################################################        
        
def Residual_Wavefront_Zalignment(date_time,ConfigFile):
    
    nb_FoV = (np.size(ConfigFile)-6)/8
    Zmax = ConfigFile[4]-2
    fName_Residual_Wavefront_firstpart="Z:\Testbeds\JOST\Alignment\data\\"+date_time+"\\Residual_Wavefront\\"
    fName_Residual_Wavefront_secondpart = ""
    for i in range(nb_FoV):
        fName_Residual_Wavefront_secondpart += "Field"+str(int(i+1))+"X"+str(int(ConfigFile[6+8*i]))+"_Field"+str(int(i+1))+"Y"+str(int(ConfigFile[7+8*i]))+"_"

    fName_Residual_Wavefront_secondpart += ".txt"
    fName_Residual_Wavefront=fName_Residual_Wavefront_firstpart+fName_Residual_Wavefront_secondpart


    #Interaction matrix 
    wf_residual = np.zeros((Zmax*nb_FoV)) 
    
    for ind in range(nb_FoV):
        link = pzz.PyZZDDE()
        link.zDDEInit()
        link.zGetRefresh() 
        # get the wavelenght
        wavesTuple = link.zGetWaveTuple()
        wave = wavesTuple[0][0] * 1000.0 # unit: lambda <-> nm
        link.zSetSurfaceParameter(9, 4, -ConfigFile[6+8*ind]/1000./2.)
        link.zSetSurfaceParameter(9, 3, -ConfigFile[6+8*ind+1]/1000./2.)           
        
        # get the wavelenght
        wavesTuple = link.zGetWaveTuple()
        wave = wavesTuple[0][0] * 1000.0 # unit: lambda <-> nm
        
        #Get the Wavefront
        coefZern = link.zGetZernikeCoef(Zmax=153)
          
        # Matrix filling
        wf_residual[ind*Zmax:(ind+1)*Zmax]=coefZern[3:Zmax+3]
    
        #Reset positions      
        #Reset positions      
        link.zSetSurfaceParameter(9, 4, 0)
        link.zSetSurfaceParameter(9, 3, 0)    
     
        
        # close the DDE link
        status = link.zDDEClose()
        
    wf_residual=wf_residual*wave
    # save the interaction matrix in a file
    with open(fName_Residual_Wavefront, 'w') as pf:
        np.savetxt(pf, wf_residual, fmt='%.15f')
        
    return wf_residual

#######################################################################################################
def Simulated_Wavefront_Zalignment(date_time,ConfigFile,misalignment):
    
    nb_FoV = (np.size(ConfigFile)-6)/8
    Zmax = ConfigFile[4]-2
    fName_Simulated_Wavefront_firstpart="Z:\Testbeds\JOST\Alignment\data\\"+date_time+"\\PhaseDiversity_Calculation\\"
    fName_Simulated_Wavefront_secondpart = ""
    for i in range(nb_FoV):
        fName_Simulated_Wavefront_secondpart += "Field"+str(int(i+1))+"X"+str(int(ConfigFile[6+8*i]))+"_Field"+str(int(i+2))+"Y"+str(int(ConfigFile[7+8*i]))+"_"

    fName_Simulated_Wavefront_secondpart += ".txt"
    fName_Simulated_Wavefront=fName_Simulated_Wavefront_firstpart+fName_Simulated_Wavefront_secondpart    
    
    #Interaction matrix 
    wf_simulation = np.zeros((Zmax*nb_FoV)) 
    
    for ind in range(nb_FoV):
        link = pzz.PyZZDDE()
        link.zDDEInit()
        link.zGetRefresh() 
        # get the wavelenght
        wavesTuple = link.zGetWaveTuple()
        wave = wavesTuple[0][0] * 1000.0 # unit: lambda <-> nm
        link.zSetSurfaceParameter(9, 4, -ConfigFile[6+8*ind]/1000./2.)
        link.zSetSurfaceParameter(9, 3, -ConfigFile[6+8*ind+1]/1000./2.)   
    
        # get the wavelenght
        wavesTuple = link.zGetWaveTuple()
        wave = wavesTuple[0][0] * 1000.0 # unit: lambda <-> nm
        
        ########################################################################################################
        # Mov the the elements
        
        # Move the elements   
        link.zSetSurfaceData(18, 3, misalignment[0] )
        link.zSetSurfaceData(24, 3, misalignment[1])  
        link.zSetSurfaceData(31, 3, misalignment[2]) 
      
       
       #Get the Wavefront
        coefZern = link.zGetZernikeCoef(Zmax=153)
          
        # Matrix filling
        wf_simulation[ind*Zmax:(ind+1)*Zmax]=coefZern[3:Zmax+3]
    
        #Reset positions      
        link.zSetSurfaceParameter(9, 4, 0)
        link.zSetSurfaceParameter(9, 3, 0)    
        link.zSetSurfaceData(18, 3, 0 )
        link.zSetSurfaceData(24, 3, 0 )  
        link.zSetSurfaceData(31, 3, 0 ) 
        link.zSetSurfaceData(39, 3, 0 ) 
        
        # close the DDE link
        status = link.zDDEClose()
    
    wf_simulation=wf_simulation*wave
    # save the interaction matrix in a file
    with open(fName_Simulated_Wavefront, 'w') as pf:
        np.savetxt(pf, wf_simulation, fmt='%.15f')
        
    return wf_simulation
########################################################################################################
def Compute_measure_vector(date_time,ConfigFile):

    nb_FoV = (np.size(ConfigFile)-6)/8  
    Zmax = ConfigFile[4]-2
    fName_measure_secondpart = ""
    for i in range(nb_FoV):
        fName_measure_secondpart += "Field"+str(int(i+1))+"X"+str(int(ConfigFile[6+8*i]))+"_Field"+str(int(i+1))+"Y"+str(int(ConfigFile[7+8*i]))+"_"
    #Getting measure vector
    fName_measure_all_fields="Z:\Testbeds\JOST\Alignment\data\\"+date_time+'\\PhaseDiversity_Calculation\\'+fName_measure_secondpart+'.txt'
    fName_measure=np.array((4))
    Measure_all_fields=np.zeros((Zmax*nb_FoV))
    for i in range(nb_FoV):
        fName_measure="Z:\Testbeds\JOST\Alignment\data\\"+date_time+"\\PhaseDiversity_Calculation\\FieldX"+str(int(ConfigFile[6+8*i]))+"_FieldY"+str(int(ConfigFile[7+8*i]))+".txt" 
        with open(fName_measure, 'r') as pf:
            Measure = np.loadtxt(pf)
        Measure_all_fields[i*Zmax:(i+1)*Zmax]=Measure[2:] 
        #We don't take the tip and tilt coef values of the measure vector
        
        
    with open(fName_measure_all_fields, 'w') as pf:
        np.savetxt(pf, Measure_all_fields , fmt='%.15f')
    
    return Measure_all_fields
    
########################################################################################################
def Misalignment_from_Zemax_to_Labview_Zalignment(pert):
 
    perturbation=np.zeros([3])
    perturbation[0]=pert[0]
    perturbation[1]=pert[1]
    perturbation[2]=-pert[2]

    return perturbation

#########################################################################################################
def MMSE_reconstruction(date_time,ConfigFile,noise_level,pert,IM,measure_vect,residual_vect):
    
    nb_FoV = (np.size(ConfigFile)-6)/8  
    Zmax = ConfigFile[4]-2

    # Getting the cobariance Matrices    
    # Getting the pertubation covariance matrix
    Cpsi = np.diag(pert**2) # size: 2D Pmax , Pmax
    
    # Getting the noise covarience matrix 
    Cn = np.diag(np.ones(nb_FoV*Zmax)*noise_level )  # size: 2D nb_WFS * Zmax , nb_WFS * Zmax
    
    # Creation of the classe estimator MMSEEstimator
    estim = ao.MMSEEstimator(IM, Cn, Cpsi)
    
    misalignment = estim.reconstruct( measure_vect- residual_vect)    # size: 1D Pmax

    misalignment_motor_motion = Misalignment_from_Zemax_to_Labview_Zalignment(misalignment)
    
    fName_misalignment="Z:\Testbeds\JOST\Alignment\data\\"+date_time+"\LinearControl_Calculation\Misalignment.txt"
    fName_misalignment_motor_motion="Z:\Testbeds\JOST\Alignment\data\\"+date_time+"\LinearControl_Calculation\Motor_motion_to_correct_alignment.txt"
    
    with open(fName_misalignment, 'w') as pf:
        np.savetxt(pf, misalignment , fmt='%.15f')

    with open(fName_misalignment_motor_motion, 'w') as pf:
        np.savetxt(pf, misalignment_motor_motion , fmt='%.15f')
        
    return misalignment, misalignment_motor_motion
########################################################################################################
def relative_difference (date_time,ConfigFile,first_vector,second_vector):

    relative_diff=(first_vector-second_vector)
    
    fName_relative_diff='Z:\Testbeds\JOST\Alignment\data\\'+date_time+'\\LinearControl_Calculation\\relative_errors_before_correcting.txt'
    
    with open(fName_relative_diff, 'w') as pf:
        np.savetxt(pf, relative_diff , fmt='%.15f')
        
    return relative_diff

############################################################################################################    
def loop_zemax(date_time,ConfigFile,noise_level,pert,IM,measure_vect,residual_vect,actuator_values,nbr_iterations):
    
    nb_FoV = (np.size(ConfigFile)-6)/8  
    Zmax = ConfigFile[4]-2

    # Getting the cobariance Matrices    
    # Getting the pertubation covariance matrix
    Cpsi = np.diag(pert**2) # size: 2D Pmax , Pmax
    
    # Getting the noise covarience matrix 
    Cn = np.diag(np.ones(nb_FoV*Zmax)*noise_level )  # size: 2D nb_WFS * Zmax , nb_WFS * Zmax
    
    wf_simulation = np.zeros((Zmax*nb_FoV,nbr_iterations+1)) 
    wf_simulation[:,0]=residual_vect
    misalignment=   np.zeros((3,nbr_iterations))  
    
    
    for iteration in range(nbr_iterations):
        IM=InterMatrix_Zalignment(date_time,ConfigFile,actuator_values)
        # Creation of the classe estimator MMSEEstimator
        estim = ao.MMSEEstimator(IM, Cn, Cpsi)
        misalignment[:,iteration] = estim.reconstruct( measure_vect- wf_simulation[:,iteration])    # size: 1D Pmax       
        
        for ind in range(nb_FoV):
            link = pzz.PyZZDDE()
            link.zDDEInit()
            link.zGetRefresh() 
            # get the wavelenght
            wavesTuple = link.zGetWaveTuple()
            wave = wavesTuple[0][0] * 1000.0 # unit: lambda <-> nm
            link.zSetSurfaceParameter(9, 4, ConfigFile[6+8*ind]/1000./2.)
            link.zSetSurfaceParameter(9, 3, -ConfigFile[6+8*ind+1]/1000./2.)   
            
            ########################################################################################################
            # Mov the the elements
            
            # Move the elements   
            link.zSetSurfaceData(18, 3, np.sum(misalignment[0,:]))
            link.zSetSurfaceData(24, 3, np.sum(misalignment[1,:]))  
            link.zSetSurfaceData(31, 3, np.sum(misalignment[2,:])) 
                   
           
           #Get the Wavefront
            coefZern = link.zGetZernikeCoef(Zmax=153)
              
            # Matrix filling
            wf_simulation[ind*Zmax:(ind+1)*Zmax,iteration+1]=coefZern[3:Zmax+3]
        
            #Reset positions      
            #link.zSetSurfaceParameter(9, 4, 0)
            #link.zSetSurfaceParameter(9, 3, 0)    
            #link.zSetSurfaceData(18, 3, 0 )
            #link.zSetSurfaceData(24, 3, 0 )  
            #link.zSetSurfaceData(31, 3, 0 ) 
        
            wf_simulation[ind*Zmax:(ind+1)*Zmax,iteration+1]=wf_simulation[ind*Zmax:(ind+1)*Zmax,iteration+1]*wave
            
        # close the DDE link
        status = link.zDDEClose()
    return wf_simulation,misalignment
        
    