# -*- coding: utf-8 -*-
"""
Created on Fri May 06 16:33:35 2016

@author: jost
"""

import subprocess

LASERexePath = "C:\\Users\\jost\\Desktop\\SourceLaser\\debug\\"

channel=3
current=43.88

LASER = subprocess.Popen(["C:\\Users\\jost\\Desktop\\SourceLaser\\debug\\SourceLaser.exe", str(channel), str(current)], 
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                        cwd=LASERexePath, bufsize=1)

#nloops = 4
#current = [0, 49, 0, 50]
#for idm in xrange(nloops):
#    #print >>DM.stdin, "config"
#    LASER.stdin.write(str(current[idm])+"\n")
#    LASER.stdin.flush()


raw_input("Press enter")
LASER.stdin.write("quit\n")
LASER.stdin.close()

for line in LASER.stdout: #print DM.stdout.readline()
    print line
    
 