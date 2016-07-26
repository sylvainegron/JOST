# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 11:59:08 2016

@author: egron
"""
import time
import numpy as np
import requests
import datetime
from astropy.io import fits
import urllib2


def Camera_Exposure(date_time,ConfigFile,Field_Number,Type=""):

    if Type=="Focus":    
 
        ################################################################################################################################
        ##FIRST PART: SET UP
        IP_address='http://192.168.192.116/'
        #frame size=3 for quarter, 2 for half, and 1 for full. 
        Frame_size='setup.html?'+'FrameSize='+str(int(1))
        Set_up=IP_address+Frame_size
        #Website: http://192.168.192.116/setup.html?FrameSize=3
        r1=requests.get(Set_up)
        ###############################################################################################################################
        ##SECOND PART: SETTINGS
        Set='api/ImagerSetSettings.cgi?'
        
        #X Central pixel StartX ConfigFile_Labview[9] for the first field at the focus
        #X Central pixel StartX ConfigFile_Labview[10] for the first field at the focus
        Central_Pixel_position='StartX='+str(int(ConfigFile[10+8*(Field_Number-1)]))+'&StartY='+str(int(ConfigFile[11+8*(Field_Number-1)]))
        
        #Size image: ConfigFile_Labview[2] for both sides
        Num='&NumX='+str(int(ConfigFile[1]))+'&NumY='+str(int(ConfigFile[1]))
        
        Settings=IP_address+Set+Central_Pixel_position+Num
        #Website: http://192.168.192.116/api/ImagerSetSettings.cgi?StartX=1998&StartY=1998&NumX=100&NumY=100       
        r2=requests.get(Settings)
        time.sleep(4)
        
        #############################################################################################################
        #Exposition to avoid the problem with the first frame
        #THIRD PART: Start Exposure    
        #The exposure time is ConfigFile_Labview[6]        
        Duration='api/ImagerStartExposure.cgi?Duration='+str(int(ConfigFile[5]))
        
        #The frame type is fixed to 1. CF issues with images when we change that number
        Frame_Type='&FrameType='+str(int(1))       
        
        today=datetime.datetime.now()
        DateTime='&DateTime='+today.isoformat()
        
        Start_Exposure=IP_address+Duration+Frame_Type+DateTime
        #Website: http://192.168.192.116/api/ImagerStartExposure.cgi?Duration=0.01&FrameType=1&DateTime=2015-1218-T15:50:49   
        r3=requests.get(Start_Exposure)
        time.sleep(2)
        ############################################################################################################################
        #FOURTH PART: FIT
        api='api/Imager.FIT'
        Imager=IP_address+api
        #Website: http://192.168.192.116/api/Imager.FIT
    
    
        Working_Directory ='Z:\Testbeds\JOST\Alignment\data\\'+date_time
        Image_name='\\'+Type+'_X'+str(int(ConfigFile[6+8*(Field_Number-1)]))+'_Y'+str(int(ConfigFile[7+8*(Field_Number-1)]))+'_'+str(int(0+1))+'.FIT'
        Image=Working_Directory+Image_name
        #Website: Z:\Testbeds\JOST\Alignment\data\q_005.FIT
        
        url=Imager 
        u=urllib2.urlopen(url) 
        output=open(Image,'wb')
        output.write(u.read())
        output.close()  
               
       
       #################################################################################################################################
        for i in range(int(ConfigFile[0])):           
            
            #THIRD PART: Start Exposure    
            #The exposure time is ConfigFile_Labview[6]
            Duration='api/ImagerStartExposure.cgi?Duration='+str(int(ConfigFile[5]))
            
            #The frame type is fixed to 1. CF issues with images when we change that number
            Frame_Type='&FrameType='+str(int(1))       
            
            today=datetime.datetime.now()
            DateTime='&DateTime='+today.isoformat()
            
            Start_Exposure=IP_address+Duration+Frame_Type+DateTime
            #Website: http://192.168.192.116/api/ImagerStartExposure.cgi?Duration=0.01&FrameType=1&DateTime=2015-1218-T15:50:49   
            r3=requests.get(Start_Exposure)
            time.sleep(2)
            ############################################################################################################################
            #FOURTH PART: FIT
            api='api/Imager.FIT'
            Imager=IP_address+api
            #Website: http://192.168.192.116/api/Imager.FIT
        
        
            Working_Directory ='Z:\Testbeds\JOST\Alignment\data\\'+date_time
            Image_name='\\'+Type+'_X'+str(int(ConfigFile[6+8*(Field_Number-1)]))+'_Y'+str(int(ConfigFile[7+8*(Field_Number-1)]))+'_'+str(int(i+1))+'.FIT'
            Image=Working_Directory+Image_name
            #Website: Z:\Testbeds\JOST\Alignment\data\q_005.FIT
            
            url=Imager 
            u=urllib2.urlopen(url) 
            output=open(Image,'wb')
            output.write(u.read())
            output.close()  
            


    elif Type=="Defocus":    
 
        ################################################################################################################################
        ##FIRST PART: SET UP
        IP_address='http://192.168.192.116/'
        #frame size=3 for quarter, 2 for half, and 1 for full. 
        Frame_size='setup.html?'+'FrameSize='+str(int(1))
        Set_up=IP_address+Frame_size
        #Website: http://192.168.192.116/setup.html?FrameSize=3
        r1=requests.get(Set_up)
        ###############################################################################################################################
        ##SECOND PART: SETTINGS
        Set='api/ImagerSetSettings.cgi?'
        
        #X Central pixel StartX ConfigFile_Labview[9] for the first field at the focus
        #X Central pixel StartX ConfigFile_Labview[10] for the first field at the focus
        Central_Pixel_position='StartX='+str(int(ConfigFile[12+8*(Field_Number-1)]))+'&StartY='+str(int(ConfigFile[13+8*(Field_Number-1)]))
        
        #Size image: ConfigFile_Labview[2] for both sides
        Num='&NumX='+str(int(ConfigFile[1]))+'&NumY='+str(int(ConfigFile[1]))
        
        Settings=IP_address+Set+Central_Pixel_position+Num
        #Website: http://192.168.192.116/api/ImagerSetSettings.cgi?StartX=1998&StartY=1998&NumX=100&NumY=100       
        r2=requests.get(Settings)
        
        time.sleep(4)
        
        #############################################################################################################
        #Exposition to avoid the problem with the first frame
        #THIRD PART: Start Exposure    
        #The exposure time is ConfigFile_Labview[6]
        Duration='api/ImagerStartExposure.cgi?Duration='+str(int(ConfigFile[5]))
        
        #The frame type is fixed to 1. CF issues with images when we change that number
        Frame_Type='&FrameType='+str(int(1))       
        
        today=datetime.datetime.now()
        DateTime='&DateTime='+today.isoformat()
        
        Start_Exposure=IP_address+Duration+Frame_Type+DateTime
        #Website: http://192.168.192.116/api/ImagerStartExposure.cgi?Duration=0.01&FrameType=1&DateTime=2015-1218-T15:50:49   
        r3=requests.get(Start_Exposure)
        time.sleep(2)
        ############################################################################################################################
        #FOURTH PART: FIT
        api='api/Imager.FIT'
        Imager=IP_address+api
        #Website: http://192.168.192.116/api/Imager.FIT
    
        Working_Directory ='Z:\Testbeds\JOST\Alignment\data\\'+date_time
        Image_name='\\'+Type+'_X'+str(int(ConfigFile[6+8*(Field_Number-1)]))+'_Y'+str(int(ConfigFile[7+8*(Field_Number-1)]))+'_'+str(int(0+1))+'.FIT'
        Image=Working_Directory+Image_name
        #Website: Z:\Testbeds\JOST\Alignment\data\q_005.FIT
        
        url=Imager 
        u=urllib2.urlopen(url) 
        output=open(Image,'wb')
        output.write(u.read())
        output.close() 
              
        #################################################################################################################################
        for i in range(int(ConfigFile[0])):           
            #THIRD PART: Start Exposure    
            #The exposure time is ConfigFile_Labview[6]
            Duration='api/ImagerStartExposure.cgi?Duration='+str(int(ConfigFile[5]))
            
            #The frame type is fixed to 1. CF issues with images when we change that number
            Frame_Type='&FrameType='+str(int(1))       
            
            today=datetime.datetime.now()
            DateTime='&DateTime='+today.isoformat()
            
            Start_Exposure=IP_address+Duration+Frame_Type+DateTime
            #Website: http://192.168.192.116/api/ImagerStartExposure.cgi?Duration=0.01&FrameType=1&DateTime=2015-1218-T15:50:49   
            r3=requests.get(Start_Exposure)
            time.sleep(2)
            ############################################################################################################################
            #FOURTH PART: FIT
            api='api/Imager.FIT'
            Imager=IP_address+api
            #Website: http://192.168.192.116/api/Imager.FIT
        
            Working_Directory ='Z:\Testbeds\JOST\Alignment\data\\'+date_time
            Image_name='\\'+Type+'_X'+str(int(ConfigFile[6+8*(Field_Number-1)]))+'_Y'+str(int(ConfigFile[7+8*(Field_Number-1)]))+'_'+str(int(i+1))+'.FIT'
            Image=Working_Directory+Image_name
            #Website: Z:\Testbeds\JOST\Alignment\data\q_005.FIT
            
            url=Imager 
            u=urllib2.urlopen(url) 
            output=open(Image,'wb')
            output.write(u.read())
            output.close() 
            
            
    elif Type=="bg_Focus":
 
        ################################################################################################################################
        ##FIRST PART: SET UP
        IP_address='http://192.168.192.116/'
        #frame size=3 for quarter, 2 for half, and 1 for full. 
        Frame_size='setup.html?'+'FrameSize='+str(int(1))
        Set_up=IP_address+Frame_size
        #Website: http://192.168.192.116/setup.html?FrameSize=3
        r1=requests.get(Set_up)
        ###############################################################################################################################
        ##SECOND PART: SETTINGS
        Set='api/ImagerSetSettings.cgi?'
        
        #X Central pixel StartX ConfigFile_Labview[9] for the first field at the focus
        #X Central pixel StartX ConfigFile_Labview[10] for the first field at the focus
        Central_Pixel_position='StartX='+str(int(ConfigFile[10+8*(Field_Number-1)]))+'&StartY='+str(int(ConfigFile[11+8*(Field_Number-1)]))
        
        #Size image: ConfigFile_Labview[2] for both sides
        Num='&NumX='+str(int(ConfigFile[1]))+'&NumY='+str(int(ConfigFile[1]))
        
        Settings=IP_address+Set+Central_Pixel_position+Num
        #Website: http://192.168.192.116/api/ImagerSetSettings.cgi?StartX=1998&StartY=1998&NumX=100&NumY=100       
        r2=requests.get(Settings)
        time.sleep(4)

        #############################################################################################################
        #Exposition to avoid the problem with the first frame
        #THIRD PART: Start Exposure    
        #The exposure time is ConfigFile_Labview[6]
        Duration='api/ImagerStartExposure.cgi?Duration='+str(int(ConfigFile[5]))
        
        #The frame type is fixed to 1. CF issues with images when we change that number
        Frame_Type='&FrameType='+str(int(1))       
        
        today=datetime.datetime.now()
        DateTime='&DateTime='+today.isoformat()
        
        Start_Exposure=IP_address+Duration+Frame_Type+DateTime
        #Website: http://192.168.192.116/api/ImagerStartExposure.cgi?Duration=0.01&FrameType=1&DateTime=2015-1218-T15:50:49   
        r3=requests.get(Start_Exposure)
        time.sleep(2)
        ############################################################################################################################
        #FOURTH PART: FIT
        api='api/Imager.FIT'
        Imager=IP_address+api
        #Website: http://192.168.192.116/api/Imager.FIT
    
    
        Working_Directory ='Z:\Testbeds\JOST\Alignment\data\\'+date_time
        Image_name=Image_name='\\'+Type+'_X'+str(int(ConfigFile[6+8*(Field_Number-1)]))+'_Y'+str(int(ConfigFile[7+8*(Field_Number-1)]))+'_'+str(int(0+1))+'.FIT'
        Image=Working_Directory+Image_name
        #Website: Z:\Testbeds\JOST\Alignment\data\q_005.FIT
        
        url=Imager 
        u=urllib2.urlopen(url) 
        output=open(Image,'wb')
        output.write(u.read())
        output.close() 
              
        #################################################################################################################################
        for i in range(int(ConfigFile[0])):        
            #THIRD PART: Start Exposure    
            #The exposure time is ConfigFile_Labview[6]
            Duration='api/ImagerStartExposure.cgi?Duration='+str(int(ConfigFile[5]))
            
            #The frame type is fixed to 1. CF issues with images when we change that number
            Frame_Type='&FrameType='+str(int(1))       
            
            today=datetime.datetime.now()
            DateTime='&DateTime='+today.isoformat()
            
            Start_Exposure=IP_address+Duration+Frame_Type+DateTime
            #Website: http://192.168.192.116/api/ImagerStartExposure.cgi?Duration=0.01&FrameType=1&DateTime=2015-1218-T15:50:49   
            r3=requests.get(Start_Exposure)
            time.sleep(2)
            ############################################################################################################################
            #FOURTH PART: FIT
            api='api/Imager.FIT'
            Imager=IP_address+api
            #Website: http://192.168.192.116/api/Imager.FIT
        
        
            Working_Directory ='Z:\Testbeds\JOST\Alignment\data\\'+date_time
            Image_name=Image_name='\\'+Type+'_X'+str(int(ConfigFile[6+8*(Field_Number-1)]))+'_Y'+str(int(ConfigFile[7+8*(Field_Number-1)]))+'_'+str(int(i+1))+'.FIT'
            Image=Working_Directory+Image_name
            #Website: Z:\Testbeds\JOST\Alignment\data\q_005.FIT
            
            url=Imager 
            u=urllib2.urlopen(url) 
            output=open(Image,'wb')
            output.write(u.read())
            output.close() 
            
            

    elif Type=="bg_Defocus":
 
        ################################################################################################################################
        ##FIRST PART: SET UP
        IP_address='http://192.168.192.116/'
        #frame size=3 for quarter, 2 for half, and 1 for full. 
        Frame_size='setup.html?'+'FrameSize='+str(int(1))
        Set_up=IP_address+Frame_size
        #Website: http://192.168.192.116/setup.html?FrameSize=3
        r1=requests.get(Set_up)
        ###############################################################################################################################
        ##SECOND PART: SETTINGS
        Set='api/ImagerSetSettings.cgi?'
        
        #X Central pixel StartX ConfigFile_Labview[9] for the first field at the focus
        #X Central pixel StartX ConfigFile_Labview[10] for the first field at the focus
        Central_Pixel_position='StartX='+str(int(ConfigFile[12+8*(Field_Number-1)]))+'&StartY='+str(int(ConfigFile[13+8*(Field_Number-1)]))
        
        #Size image: ConfigFile_Labview[2] for both sides
        Num='&NumX='+str(int(ConfigFile[1]))+'&NumY='+str(int(ConfigFile[1]))
        
        Settings=IP_address+Set+Central_Pixel_position+Num
        #Website: http://192.168.192.116/api/ImagerSetSettings.cgi?StartX=1998&StartY=1998&NumX=100&NumY=100       
        r2=requests.get(Settings)
        time.sleep(4)

        #############################################################################################################
        #Exposition to avoid the problem with the first frame        
        #THIRD PART: Start Exposure    
        #The exposure time is ConfigFile_Labview[6]
        Duration='api/ImagerStartExposure.cgi?Duration='+str(int(ConfigFile[5]))
        
        #The frame type is fixed to 1. CF issues with images when we change that number
        Frame_Type='&FrameType='+str(int(1))       
        
        today=datetime.datetime.now()
        DateTime='&DateTime='+today.isoformat()
        
        Start_Exposure=IP_address+Duration+Frame_Type+DateTime
        #Website: http://192.168.192.116/api/ImagerStartExposure.cgi?Duration=0.01&FrameType=1&DateTime=2015-1218-T15:50:49   
        r3=requests.get(Start_Exposure)
        time.sleep(2)
        ############################################################################################################################
        #FOURTH PART: FIT
        api='api/Imager.FIT'
        Imager=IP_address+api
        #Website: http://192.168.192.116/api/Imager.FIT
    
    
    
        Working_Directory ='Z:\Testbeds\JOST\Alignment\data\\'+date_time
        Image_name=Image_name='\\'+Type+'_X'+str(int(ConfigFile[6+8*(Field_Number-1)]))+'_Y'+str(int(ConfigFile[7+8*(Field_Number-1)]))+'_'+str(int(0+1))+'.FIT'
        Image=Working_Directory+Image_name
        #Website: Z:\Testbeds\JOST\Alignment\data\q_005.FIT
        
        url=Imager 
        u=urllib2.urlopen(url) 
        output=open(Image,'wb')
        output.write(u.read())
        output.close()            
              
        #################################################################################################################################
        for i in range(int(ConfigFile[0])):        
            #THIRD PART: Start Exposure    
            #The exposure time is ConfigFile_Labview[6]
            Duration='api/ImagerStartExposure.cgi?Duration='+str(int(ConfigFile[5]))
            
            #The frame type is fixed to 1. CF issues with images when we change that number
            Frame_Type='&FrameType='+str(int(1))       
            
            today=datetime.datetime.now()
            DateTime='&DateTime='+today.isoformat()
            
            Start_Exposure=IP_address+Duration+Frame_Type+DateTime
            #Website: http://192.168.192.116/api/ImagerStartExposure.cgi?Duration=0.01&FrameType=1&DateTime=2015-1218-T15:50:49   
            r3=requests.get(Start_Exposure)
            time.sleep(2)
            ############################################################################################################################
            #FOURTH PART: FIT
            api='api/Imager.FIT'
            Imager=IP_address+api
            #Website: http://192.168.192.116/api/Imager.FIT
        
        
        
            Working_Directory ='Z:\Testbeds\JOST\Alignment\data\\'+date_time
            Image_name=Image_name='\\'+Type+'_X'+str(int(ConfigFile[6+8*(Field_Number-1)]))+'_Y'+str(int(ConfigFile[7+8*(Field_Number-1)]))+'_'+str(int(i+1))+'.FIT'
            Image=Working_Directory+Image_name
            #Website: Z:\Testbeds\JOST\Alignment\data\q_005.FIT
            
            url=Imager 
            u=urllib2.urlopen(url) 
            output=open(Image,'wb')
            output.write(u.read())
            output.close()            
            
            
def Take_Image(Size_Image,Number_of_images,CenterImageX,CenterImageY,Image_name):
    #example  
    # Cam.Take_Image(100,5,1998,2998,'Z:\Testbeds\JOST\Alignment\\data\\test')
    
        
    ################################################################################################################################
    time.sleep(4)        
    ##FIRST PART: SET UP
    IP_address='http://192.168.192.116/'
    #frame size=3 for quarter, 2 for half, and 1 for full. 
    Frame_size='setup.html?'+'FrameSize='+str(int(1))
    Set_up=IP_address+Frame_size
    r1=requests.get(Set_up)
    ###############################################################################################################################
    time.sleep(4)        
    ##SECOND PART: SETTINGS
    Set='api/ImagerSetSettings.cgi?'
    
    #X Central pixel StartX ConfigFile_Labview[9] for the first field at the focus
    #X Central pixel StartX ConfigFile_Labview[10] for the first field at the focus
    Central_Pixel_position='StartX='+str(CenterImageX)+'&StartY='+str(CenterImageY)
    
    #Size image: ConfigFile_Labview[2] for both sides
    Num='&NumX='+str(Size_Image)+'&NumY='+str(Size_Image)
    
    Settings=IP_address+Set+Central_Pixel_position+Num      
    r2=requests.get(Settings)
    
    #################################################################################################################################        
    time.sleep(4)       
    #THIRD PART: Start Exposure    
    #The exposure time is ConfigFile_Labview[6]
    Duration='api/ImagerStartExposure.cgi?Duration='+str(0.01)
    
    #The frame type is fixed to 1. CF issues with images when we change that number
    Frame_Type='&FrameType='+str(int(1))       
    
    today=datetime.datetime.now()
    DateTime='&DateTime='+today.isoformat()
    
    Start_Exposure=IP_address+Duration+Frame_Type+DateTime
    r3=requests.get(Start_Exposure)
    
    ############################################################################################################################
    time.sleep(2)        
    #FOURTH PART: FIT
    api='api/Imager.FIT'
    Imager=IP_address+api


    Second_part='_'+str(int(1))+'.FIT'
    Image=Image_name+Second_part
    
    url=Imager 
    u=urllib2.urlopen(url) 
    output=open(Image,'wb')
    output.write(u.read())
    output.close()          
    
    for i in range(Number_of_images):
        #################################################################################################################################        
               
        #THIRD PART: Start Exposure    
        #The exposure time is ConfigFile_Labview[6]
        Duration='api/ImagerStartExposure.cgi?Duration='+str(0.01)
        
        #The frame type is fixed to 1. CF issues with images when we change that number
        Frame_Type='&FrameType='+str(int(1))       
        
        today=datetime.datetime.now()
        DateTime='&DateTime='+today.isoformat()
        
        Start_Exposure=IP_address+Duration+Frame_Type+DateTime
        r3=requests.get(Start_Exposure)
        
        ############################################################################################################################
        time.sleep(2)        
        #FOURTH PART: FIT
        api='api/Imager.FIT'
        Imager=IP_address+api
    
    
        Second_part='_'+str(int(i+1))+'.FIT'
        Image=Image_name+Second_part
        
        url=Imager 
        u=urllib2.urlopen(url) 
        output=open(Image,'wb')
        output.write(u.read())
        output.close()  
       
        
def Take_Image_no_time_sleep(Size_Image,Number_of_images,CenterImageX,CenterImageY,Image_name):
    #example  
    # Cam.Take_Image(100,5,2048,2048,'Z:\Testbeds\JOST\Alignment\\data\\test')
    
    ################################################################################################################################
    ##FIRST PART: SET UP
    IP_address='http://192.168.192.116/'
    #frame size=3 for quarter, 2 for half, and 1 for full. 
    Frame_size='setup.html?'+'FrameSize='+str(int(1))
    Set_up=IP_address+Frame_size
    r1=requests.get(Set_up)
    ###############################################################################################################################
    ##SECOND PART: SETTINGS
    Set='api/ImagerSetSettings.cgi?'
    
    #X Central pixel StartX ConfigFile_Labview[9] for the first field at the focus
    #X Central pixel StartX ConfigFile_Labview[10] for the first field at the focus
    Central_Pixel_position='StartX='+str(CenterImageX-Size_Image/2)+'&StartY='+str(CenterImageY-Size_Image/2)
    
    #Size image: ConfigFile_Labview[2] for both sides
    Num='&NumX='+str(Size_Image)+'&NumY='+str(Size_Image)
    
    Settings=IP_address+Set+Central_Pixel_position+Num      
    r2=requests.get(Settings)
    
    #################################################################################################################################
    #THIRD PART: Start Exposure    
    #The exposure time is ConfigFile_Labview[6]
    Duration='api/ImagerStartExposure.cgi?Duration='+str(0.01)
    
    #The frame type is fixed to 1. CF issues with images when we change that number
    Frame_Type='&FrameType='+str(int(1))       
    
    today=datetime.datetime.now()
    DateTime='&DateTime='+today.isoformat()
    
    Start_Exposure=IP_address+Duration+Frame_Type+DateTime
    r3=requests.get(Start_Exposure)
    
    ############################################################################################################################
    #FOURTH PART: FIT
    api='api/Imager.FIT'
    Imager=IP_address+api
    
    for i in range(Number_of_images):
        Second_part='_'+str(int(i+1))+'.FIT'
        Image=Image_name+Second_part
        
        url=Imager 
        u=urllib2.urlopen(url) 
        output=open(Image,'wb')
        output.write(u.read())
        output.close()  
    