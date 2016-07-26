# -*- coding: utf-8 -*-
"""
Created on Mon Apr 04 09:47:29 2016

@author: egron
"""

import numpy as np
import zzdde_SylvainVersion as pzz

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
    IM = np.zeros((Zmax*nb_FoV,4)) 

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
        
        #Camera    
        # get the push
        link.zSetSurfaceData(39, 3, actuator_values[3])
        coefZern_plus = link.zGetZernikeCoef(Zmax=153)
        # get the pull
        link.zSetSurfaceData(39, 3, -actuator_values[3])
        coefZern_minus = link.zGetZernikeCoef(Zmax=153)
        #reset
        link.zSetSurfaceData(39, 3, 0.0)
        # IM computation
        coefZern_IM = (coefZern_plus - coefZern_minus) / (2 * actuator_values[3])
        #IM filling
        IM[ind*Zmax:(ind+1)*Zmax,3] = coefZern_IM[3:Zmax+3]  
        
        
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
        link.zSetSurfaceData(39, 3, misalignment[3])         
       
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
        Measure_all_fields[i*Zmax:(i+1)*Zmax]=Measure[2:] #We don't take the tip and tilt coef values of the measure vector
        
       
        
        
    with open(fName_measure_all_fields, 'w') as pf:
        np.savetxt(pf, Measure_all_fields , fmt='%.15f')
    
    return Measure_all_fields
    
########################################################################################################
def Misalignment_from_Zemax_to_Labview_Zalignment(pert):
 
    perturbation=np.zeros([4])
    perturbation[0]=pert[0]
    perturbation[1]=pert[1]
    perturbation[2]=-pert[2]
    perturbation[3]=-pert[3]
 
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
    
###############################################################################################################################
def loop_zemax(date_time,ConfigFile,noise_level,pert,measure_vect,residual_vect,actuator_values,nbr_iterations):
    
    nb_FoV = (np.size(ConfigFile)-6)/8  
    Zmax = ConfigFile[4]-2

   
    IM = np.zeros((Zmax*nb_FoV,4))
    # Getting the noise covarience matrix 
    Cn = np.diag(np.ones(nb_FoV*Zmax)*noise_level )  # size: 2D nb_WFS * Zmax , nb_WFS * Zmax
    
    wf_simulation = np.zeros((Zmax*nb_FoV,nbr_iterations+1)) 
    wf_simulation[:,0]=residual_vect
    misalignment=   np.zeros((4,nbr_iterations))  
    Misalignment_SVD=   np.zeros((4,nbr_iterations))  
   
    for iteration in range(nbr_iterations):
        
                
        # Getting the cobariance Matrices    
        # Getting the pertubation covariance matrix
       
       
        Cpsi = np.diag(pert**2) # size: 2D Pmax , Pmax        

        for ind in range(nb_FoV):
        
            #Creating IM for each iteration        
            link = pzz.PyZZDDE()
            link.zDDEInit()
            link.zGetRefresh() 
            # get the wavelenght
            wavesTuple = link.zGetWaveTuple()
            wave = wavesTuple[0][0] * 1000.0 # unit: lambda <-> nm
            link.zSetSurfaceParameter(9, 4, -ConfigFile[6+8*ind]/1000./2.)
            link.zSetSurfaceParameter(9, 3, -ConfigFile[6+8*ind+1]/1000./2.)
           
            actuator_values=actuator_values
            #divide by 1000 because we work with milidegrees in the text file
            #divide by two, because we have to put the half field on the surface coord breaf, for more information 
            #check google doc JOST technical report, steering mirror. 
            #L1    
            # get the push
            link.zSetSurfaceData(18, 3, np.sum(misalignment[0,:])+actuator_values[0])
            coefZern_plus = link.zGetZernikeCoef(Zmax=153)
            # get the pull
            link.zSetSurfaceData(18, 3, np.sum(misalignment[0,:])-actuator_values[0])
            coefZern_minus = link.zGetZernikeCoef(Zmax=153)
            #reset
            link.zSetSurfaceData(18, 3, 0.0)
            # IM computation
            coefZern_IM = (coefZern_plus - coefZern_minus) / (2 * actuator_values[0])
            #IM filling
            IM[ind*Zmax:(ind+1)*Zmax,0] = coefZern_IM[3:Zmax+3]
        
            #L2
            # get the push
            link.zSetSurfaceData(24, 3, np.sum(misalignment[1,:])+actuator_values[1])
            coefZern_plus = link.zGetZernikeCoef(Zmax=153)    
            # get the pull
            link.zSetSurfaceData(24, 3, np.sum(misalignment[1,:])-actuator_values[1])
            coefZern_minus = link.zGetZernikeCoef(Zmax=153)    
            #reset
            link.zSetSurfaceData(24, 3, 0.0)    
            # IM computation
            coefZern_IM = (coefZern_plus - coefZern_minus) / (2 * actuator_values[1])
            #IM filling
            IM[ind*Zmax:(ind+1)*Zmax,1] = coefZern_IM[3:Zmax+3]
               
            #L3   
            # get the push
            link.zSetSurfaceData(31, 3, np.sum(misalignment[2,:])+actuator_values[2])
            coefZern_plus = link.zGetZernikeCoef(Zmax=153)
            # get the pull
            link.zSetSurfaceData(31, 3, np.sum(misalignment[2,:])-actuator_values[2])
            coefZern_minus = link.zGetZernikeCoef(Zmax=153)
            #reset
            link.zSetSurfaceData(31, 3, 0.0)
            # IM computation
            coefZern_IM = (coefZern_plus - coefZern_minus) / (2 * actuator_values[2])
            #IM filling
            IM[ind*Zmax:(ind+1)*Zmax,2] = coefZern_IM[3:Zmax+3]
            
            #Camera    
            # get the push
            link.zSetSurfaceData(39, 3, np.sum(misalignment[3,:])+actuator_values[3])
            coefZern_plus = link.zGetZernikeCoef(Zmax=153)
            # get the pull
            link.zSetSurfaceData(39, 3, np.sum(misalignment[3,:])-actuator_values[3])
            coefZern_minus = link.zGetZernikeCoef(Zmax=153)
            #reset
            link.zSetSurfaceData(39, 3, 0.0)
            # IM computation
            coefZern_IM = (coefZern_plus - coefZern_minus) / (2 * actuator_values[3])
            #IM filling
            IM[ind*Zmax:(ind+1)*Zmax,3] = coefZern_IM[3:Zmax+3]  
            
            
            link.zSetSurfaceParameter(9, 3, 0)
            link.zSetSurfaceParameter(9, 4, 0)
            
            # close the DDE link
            status = link.zDDEClose()
         
            IM=IM*wave 
            
            
            
            # Creation of the classe estimator MMSEEstimator
            estim = ao.MMSEEstimator(IM, Cn, Cpsi)
            misalignment[:,iteration] = estim.reconstruct(wf_simulation[:,iteration]-measure_vect)    # size: 1D Pmax  
           
            U,S,Vt=np.linalg.svd(IM, full_matrices=False)
            cond_val=0.1
            MI=np.linalg.pinv(IM, cond_val)
            Misalignment_SVD[:,iteration]=np.dot(MI,measure_vect-residual_vect)
        
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
            link.zSetSurfaceData(39, 3, np.sum(misalignment[3,:]))         
           
           #Get the Wavefront
            coefZern = link.zGetZernikeCoef(Zmax=153)
              
            # Matrix filling
            wf_simulation[ind*Zmax:(ind+1)*Zmax,iteration+1]=coefZern[3:Zmax+3]
        
            #Reset positions      
            link.zSetSurfaceParameter(9, 4, 0)
            link.zSetSurfaceParameter(9, 3, 0)    
            link.zSetSurfaceData(18, 3, 0 )
            link.zSetSurfaceData(24, 3, 0 )  
            link.zSetSurfaceData(31, 3, 0 ) 
            link.zSetSurfaceData(39, 3, 0 ) 
            
            # close the DDE link
            status = link.zDDEClose()
        
            wf_simulation[ind*Zmax:(ind+1)*Zmax,iteration+1]=wf_simulation[ind*Zmax:(ind+1)*Zmax,iteration+1]*wave
        
        final_misalignment=np.zeros((4)) 
        final_misalignment[0]=np.sum(misalignment[0,:])
        final_misalignment[1]=np.sum(misalignment[1,:])
        final_misalignment[2]=np.sum(misalignment[2,:])
        final_misalignment[3]=np.sum(misalignment[3,:])          
            
    return wf_simulation,misalignment,final_misalignment
   
#################################################################################################################     
def MMSE_reconstruction_on_vectors(nb_FoV,noise_level,pert,IM,measure_vect,residual_vect):

    nbr_zernikes=np.size(measure_vect)
    # Getting the covariance Matrices    
    # Getting the pertubation covariance matrix
    Cpsi = np.diag(pert**2) # size: 2D Pmax , Pmax
    
    # Getting the noise covarience matrix 
    Cn = np.diag(np.ones(nb_FoV*nbr_zernikes)*noise_level )  # size: 2D nb_WFS * Zmax , nb_WFS * Zmax
    
    # Creation of the classe estimator MMSEEstimator
    estim = ao.MMSEEstimator(IM, Cn, Cpsi)
    
    misalignment = estim.reconstruct(measure_vect- residual_vect)    # size: 1D Pmax
        
    return misalignment
    
##################################################################################################################
def LS_reconstruction_on_vectors(cond_val,IM,measure_vect,residual_vect):
    
    U,S,Vt=np.linalg.svd(IM, full_matrices=False)
    MI=np.linalg.pinv(IM, cond_val)
    misalignment_LS=np.dot(MI,measure_vect- residual_vect)
    
    return misalignment_LS 
    
####################################################################################################################
def IM_on_vectors(field_vector,actuator_value,alignment_state,nbr_zernikes):
    #nbr_zernikes is the number of zernikes calculated started with Z4
    nb_FoV=np.size(field_vector)/2
    IM = np.zeros((nbr_zernikes*nb_FoV,4))  
    
    for ind in range(nb_FoV):
    
        #Creating IM for each iteration        
        link = pzz.PyZZDDE()
        link.zDDEInit()
        link.zGetRefresh() 
        # get the wavelenght
        wavesTuple = link.zGetWaveTuple()
        wave = wavesTuple[0][0] * 1000.0 # unit: lambda <-> nm
        link.zSetSurfaceParameter(9, 4, -field_vector[2*ind]/1000./2.)
        link.zSetSurfaceParameter(9, 3, -field_vector[2*ind+1]/1000./2.)


        #divide by 1000 because we work with milidegrees in the text file
        #divide by two, because we have to put the half field on the surface coord breaf, for more information 
        #check google doc JOST technical report, steering mirror. 
        #L1    
        # get the push
        link.zSetSurfaceData(18, 3, alignment_state[0]+actuator_value[0])
        coefZern_plus = link.zGetZernikeCoef(Zmax=153)
        # get the pull
        link.zSetSurfaceData(18, 3, alignment_state[0]-actuator_value[0])
        coefZern_minus = link.zGetZernikeCoef(Zmax=153)
        #reset
        link.zSetSurfaceData(18, 3, 0.0)
        # IM computation
        coefZern_IM = (coefZern_plus - coefZern_minus) / (2 * actuator_value[0])
        #IM filling
        IM[ind*nbr_zernikes:(ind+1)*nbr_zernikes,0] = coefZern_IM[3:nbr_zernikes+3]
    
        #L2
        # get the push
        link.zSetSurfaceData(24, 3,alignment_state[1]+actuator_value[1])
        coefZern_plus = link.zGetZernikeCoef(Zmax=153)    
        # get the pull
        link.zSetSurfaceData(24, 3, alignment_state[1]-actuator_value[1])
        coefZern_minus = link.zGetZernikeCoef(Zmax=153)    
        #reset
        link.zSetSurfaceData(24, 3, 0.0)    
        # IM computation
        coefZern_IM = (coefZern_plus - coefZern_minus) / (2 * actuator_value[1])
        #IM filling
        IM[ind*nbr_zernikes:(ind+1)*nbr_zernikes,1] = coefZern_IM[3:nbr_zernikes+3]
           
        #L3   
        # get the push
        link.zSetSurfaceData(31, 3, alignment_state[2]+actuator_value[2])
        coefZern_plus = link.zGetZernikeCoef(Zmax=153)
        # get the pull
        link.zSetSurfaceData(31, 3, alignment_state[2]-actuator_value[2])
        coefZern_minus = link.zGetZernikeCoef(Zmax=153)
        #reset
        link.zSetSurfaceData(31, 3, 0.0)
        # IM computation
        coefZern_IM = (coefZern_plus - coefZern_minus) / (2 * actuator_value[2])
        #IM filling
        IM[ind*nbr_zernikes:(ind+1)*nbr_zernikes,2] = coefZern_IM[3:nbr_zernikes+3]
        
        #Camera    
        # get the push
        link.zSetSurfaceData(39, 3,alignment_state[3]+actuator_value[3])
        coefZern_plus = link.zGetZernikeCoef(Zmax=153)
        # get the pull
        link.zSetSurfaceData(39, 3, alignment_state[3]-actuator_value[3])
        coefZern_minus = link.zGetZernikeCoef(Zmax=153)
        #reset
        link.zSetSurfaceData(39, 3, 0.0)
        # IM computation
        coefZern_IM = (coefZern_plus - coefZern_minus) / (2 * actuator_value[3])
        #IM filling
        IM[ind*nbr_zernikes:(ind+1)*nbr_zernikes,3] = coefZern_IM[3:nbr_zernikes+3]  
        
        
        link.zSetSurfaceParameter(9, 3, 0)
        link.zSetSurfaceParameter(9, 4, 0)
        
        # close the DDE link
        status = link.zDDEClose()
     
        IM=IM*wave 
        
        return IM
        
#####################################################################################################################        
def Simulated_Wavefront_Zalignment_on_vector(field_vector,alignment_state,nbr_zernikes):
    
    #nbr_zernikes is the number of zernikes calculated started with Z4
    nb_FoV=np.size(field_vector)/2 
    wf_simulation = np.zeros((nbr_zernikes*nb_FoV)) 
    
    for ind in range(nb_FoV):
        link = pzz.PyZZDDE()
        link.zDDEInit()
        link.zGetRefresh() 
        # get the wavelenght
        wavesTuple = link.zGetWaveTuple()
        wave = wavesTuple[0][0] * 1000.0 # unit: lambda <-> nm
        link.zSetSurfaceParameter(9, 4, -field_vector[2*ind]/1000./2.)
        link.zSetSurfaceParameter(9, 3, -field_vector[2*ind+1]/1000./2.)   
    
        # get the wavelenght
        wavesTuple = link.zGetWaveTuple()
        wave = wavesTuple[0][0] * 1000.0 # unit: lambda <-> nm
        
        ########################################################################################################
        # Mov the the elements
        
        # Move the elements   
        link.zSetSurfaceData(18, 3, alignment_state[0] )
        link.zSetSurfaceData(24, 3, alignment_state[1])  
        link.zSetSurfaceData(31, 3, alignment_state[2]) 
        link.zSetSurfaceData(39, 3, alignment_state[3])         
       
       #Get the Wavefront
        coefZern = link.zGetZernikeCoef(Zmax=153)
          
        # Matrix filling
        wf_simulation[ind*nbr_zernikes:(ind+1)*nbr_zernikes]=coefZern[3:nbr_zernikes+3]
    
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

        
    return wf_simulation
    
###################################################################################################################
def diversity_wavefront(camera_translation_mm,field_vector,nbr_zernikes):
    #10.571 est la valeur actuelle
    focus=np.array([0.,0.,0.,0.])    
    defocus=np.array([0.,0.,0.,camera_translation_mm])   
    wf_defocus=Simulated_Wavefront_Zalignment_on_vector(field_vector,defocus,nbr_zernikes)
    wf_focus=Simulated_Wavefront_Zalignment_on_vector(field_vector,focus,nbr_zernikes)
    wf=wf_defocus-wf_focus
    
    return wf

##################################################################################################################
def diversity_for_WFS(wavelength_microns,pixel_size_microns,surech,camera_translation_mm):
    
    N = 2*surech*pixel_size_microns/wavelength_microns
    defoc = -camera_translation_mm*1000*np.pi/N/N/wavelength_microns/8./np.sqrt(3.)
    
    return defoc
###################################################################################################################    
def decoup_line(matrix,vect):
#This is for matrix !!!!!!!!!!!    
    #This function removes some of the lines of the matrix
    # vect is a vector with 0 and 1, it has as many elements, as the number of lines of the matrix. 
    #There is a 0 to remove the line and a 1 to keep it
    non_zero=np.count_nonzero(vect)
    decouped_matrix=np.zeros((non_zero,np.size(matrix)/np.size(vect)))
    a=0
    for i in range(np.size(vect)):     
        if vect[i]==1:        
            decouped_matrix[a]=matrix[i]
            a=a+1
            
    return decouped_matrix
    
###################################################################################################################    
def decoup_element(matrix,vect):
    #This is for vector !!!!!!!!!!!
    #This function removes some elements of a vector
    # vect is a vector with 0 and 1, it has as many elements, as the number of elements of the vector. 
    #There is a 0 to remove the element and a 1 to keep it
    non_zero=np.count_nonzero(vect)
    decouped_matrix=np.zeros((non_zero))
    a=0
    for i in range(np.size(vect)):     
        if vect[i]==1:        
            decouped_matrix[a]=matrix[i]
            a=a+1
            
    return decouped_matrix