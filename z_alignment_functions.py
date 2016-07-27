# -*- coding: utf-8 -*-
"""
Created on Mon Apr 04 09:47:29 2016

@author: egron
"""

import numpy as np
import zzdde_SylvainVersion as pzz
import pyao_SylvainVersion as ao

########################################################################################################

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
    
    
###################################################################################################################    
def set_field_on_zemax(link,field_vector,field_index):
    #field_vector must be in degrees
    link.zSetSurfaceParameter(9, 4, -field_vector[2*field_index]/2.)
    link.zSetSurfaceParameter(9, 3, -field_vector[2*field_index+1]/2.)
    
    return    
    
####################################################################################################################
def reset_positions_on_zemax(link):
    link.zSetSurfaceParameter(9, 4, 0)
    link.zSetSurfaceParameter(9, 3, 0)    
    link.zSetSurfaceData(18, 3, 0 )
    link.zSetSurfaceData(24, 3, 0 )  
    link.zSetSurfaceData(31, 3, 0 ) 
    link.zSetSurfaceData(39, 3, 0 ) 
    return   
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
        
        set_field_on_zemax(link,field_vector,ind)

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
        
        
        reset_positions_on_zemax(link)
        
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
        
        set_field_on_zemax(link,field_vector,ind)
    
        ########################################################################################################       
        # Move the elements   
        link.zSetSurfaceData(18, 3, alignment_state[0] )
        link.zSetSurfaceData(24, 3, alignment_state[1])  
        link.zSetSurfaceData(31, 3, alignment_state[2]) 
        link.zSetSurfaceData(39, 3, alignment_state[3])         
       
        #Get the Wavefront
        coefZern = link.zGetZernikeCoef(Zmax=153)
          
        # Vector filling
        wf_simulation[ind*nbr_zernikes:(ind+1)*nbr_zernikes]=coefZern[3:nbr_zernikes+3]
        
        #reset position
        reset_positions_on_zemax(link) 
        
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