# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 11:49:13 2016

@author: egron
"""

import numpy as np
import z_alignment_functions as Zalign

#Definition of the properties of the system: 
with open('Z:\\Testbeds\\JOST\\Alignment\\data\\date_for_python.txt', 'r') as pf:
    Date_ = np.loadtxt(pf)

Date=str(int(Date_[0]))+'-'+str(int(Date_[1]))+'-'+str(int(Date_[2]))+'-'+str(int(Date_[3]))+'h-'+str(int(Date_[4]))+'min'
    
with open('Z:\Testbeds\JOST\Alignment\data\\'+Date+'\\python_config_file_'+Date+'.txt', 'r') as pf:
    configFile_python = np.loadtxt(pf)
    
#Getting the data
measure_vect=Zalign.Compute_measure_vector(Date,configFile_python)
residual_vect=Zalign.Residual_Wavefront_Zalignment(Date,configFile_python)

field_vector=np.array([0,0])
nb_FoV=np.size(field_vector)/2
actuator_value=np.array([1,1,1,1])
alignment_state=np.array([0,0,0,0])
nbr_zernikes=np.size(residual_vect)
cond_val=0.1

noise_level=2.
pert=np.array([1.,1.,1.,1.])
decoup_vector=np.zeros((np.size(residual_vect)))
decoup_vector[0]=1
decoup_vector[2]=1
decoup_vector[4]=1
decoup_vector[8]=1
final_number_zernikes=np.count_nonzero(decoup_vector)
#zernike_I_choose=np.array([0,2,4,7,8])

measure_vect=Zalign.decoup_element(measure_vect,decoup_vector)
residual_vect=Zalign.decoup_element(residual_vect,decoup_vector)
#measure_vect=np.array([measure_vect[zernike_I_choose[0]],measure_vect[zernike_I_choose[1]],measure_vect[zernike_I_choose[2]],measure_vect[zernike_I_choose[4]]])
#residual_vect=np.array([residual_vect[zernike_I_choose[0]],residual_vect[zernike_I_choose[1]],residual_vect[zernike_I_choose[2]],residual_vect[zernike_I_choose[4]]])

IM=Zalign.IM_on_vectors(field_vector,actuator_value,alignment_state,nbr_zernikes)
IM=Zalign.decoup_line(IM,decoup_vector)


MMSE=Zalign.MMSE_reconstruction_on_vectors(nb_FoV,noise_level,pert,IM,measure_vect,residual_vect)

LS=Zalign.LS_reconstruction_on_vectors(cond_val,IM,measure_vect,residual_vect)
U,S,Vt=np.linalg.svd(IM, full_matrices=False)

###############################################################################
#Firt iteration of the loop
#MMSE
IM1_MMSE=Zalign.IM_on_vectors(field_vector,actuator_value,MMSE,nbr_zernikes)
IM1_MMSE=Zalign.decoup_line(IM1_MMSE,decoup_vector)
#IM1_MMSE=np.array([IM1_MMSE[zernike_I_choose[0],:],IM1_MMSE[zernike_I_choose[1],:],IM1_MMSE[zernike_I_choose[2],:],IM1_MMSE[zernike_I_choose[4],:]])

WF1_MMSE=Zalign.Simulated_Wavefront_Zalignment_on_vector(field_vector,MMSE,nbr_zernikes)
WF1_MMSE=Zalign.decoup_element(WF1_MMSE,decoup_vector)
#WF1_MMSE=np.array([WF1_MMSE[zernike_I_choose[0]],WF1_MMSE[zernike_I_choose[1]],WF1_MMSE[zernike_I_choose[2]],WF1_MMSE[zernike_I_choose[4]]])


MMSE1=Zalign.MMSE_reconstruction_on_vectors(nb_FoV,noise_level,pert/2.,IM1_MMSE,measure_vect,WF1_MMSE)

#LS
IM1_LS=Zalign.IM_on_vectors(field_vector,actuator_value,LS,nbr_zernikes)
IM1_LS=Zalign.decoup_line(IM1_LS,decoup_vector)
#IM1_LS=np.array([IM1_LS[zernike_I_choose[0],:],IM1_LS[zernike_I_choose[1],:],IM1_LS[zernike_I_choose[2],:],IM1_LS[zernike_I_choose[4],:]])

WF1_LS=Zalign.Simulated_Wavefront_Zalignment_on_vector(field_vector,LS,nbr_zernikes)
WF1_LS=Zalign.decoup_element(WF1_LS,decoup_vector)
#WF1_LS=np.array([WF1_LS[zernike_I_choose[0]],WF1_LS[zernike_I_choose[1]],WF1_LS[zernike_I_choose[2]],WF1_LS[zernike_I_choose[4]]])


LS1=Zalign.LS_reconstruction_on_vectors(cond_val,IM1_LS,measure_vect,WF1_LS)


###############################################################################
#Second iteration of the loop
#MMSE
IM2_MMSE=Zalign.IM_on_vectors(field_vector,actuator_value,MMSE1+MMSE,nbr_zernikes)
IM2_MMSE=Zalign.decoup_line(IM2_MMSE,decoup_vector)
#IM2_MMSE=np.array([IM2_MMSE[zernike_I_choose[0],:],IM2_MMSE[zernike_I_choose[1],:],IM2_MMSE[zernike_I_choose[2],:],IM2_MMSE[zernike_I_choose[4],:]])

WF2_MMSE=Zalign.Simulated_Wavefront_Zalignment_on_vector(field_vector,MMSE+MMSE1,nbr_zernikes)
WF2_MMSE=Zalign.decoup_element(WF2_MMSE,decoup_vector)
#WF2_MMSE=np.array([WF2_MMSE[zernike_I_choose[0]],WF2_MMSE[zernike_I_choose[1]],WF2_MMSE[zernike_I_choose[2]],WF2_MMSE[zernike_I_choose[4]]])


MMSE2=Zalign.MMSE_reconstruction_on_vectors(nb_FoV,noise_level,pert/4.,IM2_MMSE,measure_vect,WF2_MMSE)

#LS
IM2_LS=Zalign.IM_on_vectors(field_vector,actuator_value,LS1+LS,nbr_zernikes)
IM2_LS=Zalign.decoup_line(IM2_LS,decoup_vector)
#IM2_LS=np.array([IM2_LS[zernike_I_choose[0],:],IM2_LS[zernike_I_choose[1],:],IM2_LS[zernike_I_choose[2],:],IM2_LS[zernike_I_choose[4],:]])

WF2_LS=Zalign.Simulated_Wavefront_Zalignment_on_vector(field_vector,LS+LS1,nbr_zernikes)
WF2_LS=Zalign.decoup_element(WF2_LS,decoup_vector)
#WF2_LS=np.array([WF2_LS[zernike_I_choose[0]],WF2_LS[zernike_I_choose[1]],WF2_LS[zernike_I_choose[2]],WF2_LS[zernike_I_choose[4]]])


LS2=Zalign.LS_reconstruction_on_vectors(cond_val,IM2_LS,measure_vect,WF2_LS)

###############################################################################
#Third iteration of the loop
#MMSE
IM3_MMSE=Zalign.IM_on_vectors(field_vector,actuator_value,MMSE2+MMSE1+MMSE,nbr_zernikes)
IM3_MMSE=Zalign.decoup_line(IM3_MMSE,decoup_vector)
#IM3_MMSE=np.array([IM3_MMSE[zernike_I_choose[0],:],IM3_MMSE[zernike_I_choose[1],:],IM3_MMSE[zernike_I_choose[2],:],IM3_MMSE[zernike_I_choose[4],:]])

WF3_MMSE=Zalign.Simulated_Wavefront_Zalignment_on_vector(field_vector,MMSE+MMSE1+MMSE2,nbr_zernikes)
WF3_MMSE=Zalign.decoup_element(WF3_MMSE,decoup_vector)
#WF3_MMSE=np.array([WF3_MMSE[zernike_I_choose[0]],WF3_MMSE[zernike_I_choose[1]],WF3_MMSE[zernike_I_choose[2]],WF3_MMSE[zernike_I_choose[4]]])


MMSE3=Zalign.MMSE_reconstruction_on_vectors(nb_FoV,noise_level,pert/8.,IM3_MMSE,measure_vect,WF3_MMSE)

#LS
IM3_LS=Zalign.IM_on_vectors(field_vector,actuator_value,LS2+LS1+LS,nbr_zernikes)
IM3_LS=Zalign.decoup_line(IM3_LS,decoup_vector)
#IM3_LS=np.array([IM3_LS[zernike_I_choose[0],:],IM3_LS[zernike_I_choose[1],:],IM3_LS[zernike_I_choose[2],:],IM3_LS[zernike_I_choose[4],:]])

WF3_LS=Zalign.Simulated_Wavefront_Zalignment_on_vector(field_vector,LS+LS1+LS2,nbr_zernikes)
WF3_LS=Zalign.decoup_element(WF3_LS,decoup_vector)
#WF3_LS=np.array([WF3_LS[zernike_I_choose[0]],WF3_LS[zernike_I_choose[1]],WF3_LS[zernike_I_choose[2]],WF3_LS[zernike_I_choose[4]]])


LS3=Zalign.LS_reconstruction_on_vectors(cond_val,IM3_LS,measure_vect,WF3_LS)