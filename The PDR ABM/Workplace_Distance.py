# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 14:44:24 2019

@author: Saman Ghaffarian

Calculate the distance to workplaces for FH.

"""


import math
from geojson_utils import point_distance
import numpy as np

def Prepare_data(points):
    p = points['features']

    FormalB =[]
    Slum = []
    Industry1 = []

    for x1 in range(0,len(p)):
        p[x1].update({'landuse': p[x1]['properties']['Name']})

    for x in range(0,len(p)):
        if p[x]['properties']['Name']==3:
            FormalB.append(p[x])
        if p[x]['properties']['Name']==2:
            Slum.append(p[x])
        if p[x]['properties']['Name']==1:
            Industry1.append(p[x]) 
            
    return (FormalB, Industry1, Slum)

def Workplace_Dist(FB, BS, BC):
   
    FormalB = FB    
    Industry = BS
    row = []        
    dist = []
    listt = []

    for y1 in range(0,len(FormalB)):
        for y2 in range(0,len(Industry)):
            dist.append(math.floor(point_distance(FormalB[y1]['geometry'], Industry[y2]['geometry'])))
        
        FormalB[y1]['properties']['distance'] = sorted(dist)[0]
        FormalB[y1]['properties']['workplace'] = np.argsort(dist)[0]
        listt.append(np.argsort(dist)[0])
    
        if listt.count(np.argsort(dist)[0])>=BC:
            Industry[np.argsort(dist)[0]]['geometry']['coordinates'][0]= 0
            Industry[np.argsort(dist)[0]]['geometry']['coordinates'][1]= 0
    
        dist=[]
        

# Normalize the distance values 
    for k in range(0,len(listt)):
        if listt[k]<=0:
            FormalB[k]['properties']['distance']=0
        else:
            row.append(FormalB[k]['properties']['distance'])
        
    maxx = max(row)

    for k in range(0,len(listt)):
        if listt[k]<=0:
            FormalB[k]['properties']['distance']=0
        else:
            FormalB[k]['properties']['distance']=(FormalB[k]['properties']['distance']/maxx)
        
    return FormalB


