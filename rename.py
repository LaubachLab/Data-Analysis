# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 10:39:49 2015

Rename MedPC files 

@author: kyra
"""

import os


os.chdir("enter directory here")

for filename in os.listdir("."):
    if filename[0]=="!":
        first = filename[1:12]
        last = filename[27:]
        if first+last not in os.listdir("."):
            os.rename(filename, first+last)
    


