# -*- coding: utf-8 -*-
"""
Created on Sun May 01 10:27:24 2016

@author: jost
"""

import subprocess

disableHardware = "false"
DMexePath = "C:\\Users\\jost\\Desktop\\Control DM\\Code\\release"
DM = subprocess.Popen(["C:\\Users\\jost\\Desktop\\Control DM\\Code\\release\\DM_Control.exe", disableHardware], 
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                        cwd=DMexePath, bufsize=1)

#DM.stdin.write("flat\n")
#DM.stdin.flush()

try:
#
    print allo    
    
    raw_input("Press enter")
    nloops = 2
    for idm in xrange(nloops):
        #print >>DM.stdin, "config"
        DM.stdin.write("config\n")
        DM.stdin.flush()
        raw_input("Press enter")
    
    
    DM.stdin.write("flat\n")
    DM.stdin.flush()
    
    raw_input("Press enter")
    

except: print "ENCOUNTERED PROBLEM, SHUTTING DOWN."
    
raw_input("Press enter one last time")
DM.stdin.write("quit\n")
DM.stdin.close()
for line in DM.stdout: #print DM.stdout.readline()
    print line
print "CLOSED"


