#! /usr/bin/env python
import os, sys, csv
import string as s
import math 
import time
#import matplotlib
import numpy as np 


def ReadFiles(path, filename):
    
    fin = open(path, 'r')
    file_contents = fin.readlines()
    #print 'file_contents **********'
    #print file_contents
    
    file_data = {'mod_file_name':filename}    # Dictionary of data from file

    for d in file_contents :
        d1 = s.strip(s.split(d, '#')[0])    # ignore comments
        if d1 :
            d1a = s.split(d1, '>') # look for parameters
            if (s.strip(d1a[0]) == '') & (len(d1a) > 1) :      # parameter line must begin with >.
                d2 = s.split(d1a[1], '=')
                if len(d2) > 0 :
                    key = s.strip(d2[0]).lower()
                    file_data[key] = s.strip(d2[1])

            elif ord(d1[0]):      # The line is data if it begins with 0-9, -, +, or ..
                dpoints = s.split(d1,',')
                dims = len(dpoints)

                for i in range(dims):
                    if(dpoints[i]!=''):
                        data = float(dpoints[i])

                    key = 'dim_'+str(i+1)
                 
                    if(file_data.has_key(key)):
                        #print 'has key'
                        file_data[key].append(data)
                    else:
                        #print 'no has key'
                        file_data[key] = [data]

    
    for n in range(dims):  #this only makes the last set an array
        key = 'dim_'+str(n+1)
        file_data[key] = np.array(file_data[key])

    fin.close()

    return file_data
    
