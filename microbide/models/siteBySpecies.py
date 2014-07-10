from __future__ import division
import sys, csv
import numpy as np
import random
from random import randrange
import decimal
import cloud

sys.path.append("/Users/lisalocey/Desktop/evolution-canyon/microbide/models/coreFunctions")
import coreFunctions as cf


""" This script will run the microbide model and generate site by species
    matrices.
"""

num_patches = 20 # number of patches in each local community

lgp = 0.99 # log-series parameter, typically approaches 1 for ecological
           # communities. represents underlying structure of regional pool

state_list = ['heterogeneous']#,'homogeneous'] # homogeneity or heterogeneity 
            # among local communities local communities vary along a single 
            # environmental axis, e.g.,mean daily temp, precipitation, etc.

im_list = [1]  # number of individuals immigrating
                           # from regional pool per time step


optimas = ['neutral', 'random', 'inverse-zipf']

northVals = [0.1, 0.3, 0.5]
southVals = [0.1, 0.3, 0.5] 

time = 500

for optima in optimas:
    
    for northVal in northVals: # environmental values
        
        for southVal in southVals: # environmental values
            
            for j, state in enumerate(state_list):
                
                for k, im in enumerate(im_list):
                    
                    northCOM, southCOM = cf.microbide(im, num_patches, lgp, northVal, southVal, optima, time)
                    #job_id = cloud.call(cf.microbide, im, num_patches, lgp, northVal, southVal, optima, time)
                    #northCOM, southCOM = cloud.result(job_id)
                    
                    
                    print len(northCOM),'patches in north and',
                    print len(southCOM),'patches in south'
                    
                    SbyS = cf.get_SitebySpecies([northCOM, southCOM])
                    #job_id = cloud.call(cf.get_SitebySpecies, [northCOM, southCOM])
                    #SbyS = cloud.result(job_id)
                    
                    
                    S = len(SbyS[0]) - 3
                    
                    r1 = len(SbyS[0])
                    for row in SbyS:
                        r2 = len(row)
                        if r1 != r2:
                            print 'unequal sized rows in Site by Species matrix'
                            sys.exit()
                        r1 = r2
                    
                    path = '/Users/lisalocey/Desktop/evolution-canyon/microbide/models'
                    path = path + '/SiteBySpecies/'
                    
                    fileName = 'SbyS_NorthVal=' + str(northVal) + '_SouthVal='
                    fileName = fileName + str(southVal) + '_im=' + str(im)
                    fileName = fileName + '_' + optima + '_optima'
                    
                    OUT = open(path + fileName + '.share','w')
                    writer = csv.writer(OUT, delimiter='\t')
                    
                    linedata = ['label', 'Group', 'numOtus']
                    for i in range(S):
                        linedata.append('Otu'+str(i))
                    
                    writer.writerow(linedata)
                
                    for row in SbyS:
                        if len(row) != r1:
                            print 'row length has been corrupted'
                            sys.exit()
                    
                        writer.writerow(row)
                        #print row
                        
                    OUT.close()