# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 13:32:17 2016

@author: egron
"""

# --------- Python program: XPS controller demonstration -------- 
# 
import XPS_Q8_drivers 
import sys 
import time
# Display error function: simplify error print out and closes socket 
def displayErrorAndClose (socketId, errorCode, APIName): 
    if (errorCode != -2) and (errorCode != -108): 
         [errorCode2, errorString] = myxps.ErrorStringGet(socketId, errorCode) 
         if (errorCode2 != 0): 
            print APIName + ': ERROR ' + str(errorCode) 
         else: 
            print APIName + ': ' + errorString 
    else: 
       if (errorCode ==-2): 
           print APIName + ': TCP timeout' 
       if (errorCode ==-108): 
           print APIName + ': The TCP/IP connection was closed by an administrator' 
    myxps.TCP_CloseSocket(socketId) 
    return 

# Instantiate the class 
myxps = XPS_Q8_drivers.XPS() 
# Connect to the XPS 
socketId = myxps.TCP_ConnectToServer('192.168.192.115', 5001, 20) 

def Motors_Initialize():
    #Initialize the motors
    for ind in range(8):
        group = 'Group'+str(ind+1)  
        positioner = group + '.Pos'
        [errorCode, returnString] = myxps.GroupInitialize(socketId, group)
    return
    
def Motors_to_zero():
    #Motors to 0 
    for ind in range(8):
        group = 'Group'+str(ind+1)  
        positioner = group + '.Pos'
        [errorCode, returnString] = myxps.GroupMoveAbsolute(socketId, positioner, [0])  
    return

def Motors_Home():
    # Home the motors
    for ind in range(8):
        group = 'Group'+str(ind+1)  
        positioner = group + '.Pos'
        [errorCode, returnString] = myxps.GroupHomeSearch(socketId, group)
    return
    
def Motors_Nominal(nominal_motor_position):
    # Get to the nominal position
    for ind in range(8):
        group = 'Group'+str(ind+1)  
        positioner = group + '.Pos' 
        [errorCode, returnString] = myxps.GroupMoveAbsolute(socketId, positioner, [nominal_motor_position[ind]])    
    return

def Motor_absolute_move(group_motor,absolute_position):
    group = 'Group'+str(group_motor)  
    positioner = group + '.Pos' 
    [errorCode, returnString] = myxps.GroupInitialize(socketId, group)
    time.sleep(1)
    [errorCode, returnString] = myxps.GroupMoveAbsolute(socketId, positioner, [0])  
    time.sleep(1)    
    [errorCode, returnString] = myxps.GroupHomeSearch(socketId, group)
    time.sleep(1)
    [errorCode, returnString] = myxps.GroupMoveAbsolute(socketId, positioner, [absolute_position])    
    return        
    

    
    

