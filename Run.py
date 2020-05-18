# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 14:05:37 2019

@author: Saman Ghaffarian

This package is develope for the post-disaster recovery modeling based on agent-based modeling. 
The code is used in the paper entitled: Agent-based modeling of post-disaster recovery with remote sensing data
Required libraries to run the code are as follows:
    Mesa package for ABM
    pandas
    numpy
    pickle
    pyproj
    time
    math
    geojson_utils
    random
    xlrd
    shapely
    networkx
    polygon_utils
    

"""

import json
from Workplace_Distance import Prepare_data, Workplace_Dist
from AllHouseholds_agent_homo import AllHouseHoldsAgent
from random_init import RandomInitialization
from random_HH import RandomHHModel
from random_satisfaction import RandomSatisfaction, SocialSatisfaction
from mesa.time import RandomActivation
from model import RecoveryModel 
import time
import pickle
import pandas as pd
from pyproj import Proj, transform

_start_time = time.time()

def tic():
    global _start_time 
    _start_time = time.time()

def tac():
    t_sec = round(time.time() - _start_time)
    (t_min, t_sec) = divmod(t_sec,60)
    (t_hour,t_min) = divmod(t_min,60) 
    print('Time passed: {}hour:{}min:{}sec'.format(t_hour,t_min,t_sec))

with open('C:/ABM/Data/Tacloban/Tacloban_points_resample+event_reloc.json') as f:
     all_agents = json.load(f)
test_agents = all_agents 
print(len(all_agents))

myProj = Proj("+proj=utm +zone=51N, +north +ellps=WGS84 +datum=WGS84 +units=m +no_defs")
for ii in range(len(all_agents['features'])):
    all_agents['features'][ii]['geometry']['coordinates'][1], all_agents['features'][ii]['geometry']['coordinates'][0] = myProj(all_agents['features'][ii]['geometry']['coordinates'][0], 
                      all_agents['features'][ii]['geometry']['coordinates'][1], inverse=True)
    
for q in range (0, len(all_agents['features'])):
    if all_agents['features'][q]['properties']['RASTERVALU'] is None:
        all_agents['features'][q]['properties']['RASTERVALU'] = 20
    test111.append(all_agents['features'][q]['properties']['RASTERVALU'])

initialization = RandomInitialization(AgentClass=AllHouseHoldsAgent,
                                      choice_model=RandomHHModel(),
                                      satisfaction_model=SocialSatisfaction())

print (initialization)

[FB, BS, Slum] = Prepare_data(all_agents)

BC = 3 #Business capacity for each workplace of high income jobs
FormalB = Workplace_Dist(FB, BS, BC)
dst = []
for q in range (0, len(FormalB)):
    dst.append(FormalB[q]['properties']['distance'])

for k in range(0,len(Slum)):
    Slum[k]['properties']['distance']=0


HouseHolds = FormalB + Slum
HouseHolds = {"crs": all_agents["crs"],
            "features": HouseHolds , 
            "type": all_agents["type"]}

for x1 in range(len(HouseHolds['features'])):
    HouseHolds['features'][x1]['id']= str(HouseHolds['features'][x1]['id'])

from tqdm import tqdm

for run_iter in tqdm(range(10)):
    
    model = RecoveryModel(HouseHolds, 3, RandomActivation, initialization=initialization)
    agent_satisfaction_all = []
    
    for i in range(20):
            tic()
            model.step()
            tac()
            if i == 1:
                cord =[]
                for j in range(model.G.number_of_nodes()):
                    for agent in model.G.node[j]['agent']:
                        #homo.append(agent.shomo)
                        cord.append(agent.__geo_interface__())
                        cord[j]['geometry']['coordinates'][0],cord[j]['geometry']['coordinates'][1]=myProj(cord[j]['geometry']['coordinates'][1],cord[j]['geometry']['coordinates'][0])
    
                geo_vision = {"crs": all_agents["crs"],
                              "features": cord , 
                              "type": all_agents["type"]}
    agent_satisfaction_all.append(model.datacollector.get_agent_vars_dataframe())
    with open('D:\\ABM\\Results\\Results_Run_'+ str(run_iter) + '.pkl', 'wb') as f:
        pickle.dump(agent_satisfaction_all, f)
    agent_satisfaction_all.to_pickle('D:\\ABM\\Results\\Results_Run_'+ str(run_iter) + '.pkl')  # where to save it, usually as a .pkl
    del model

# Starting here the further lines are only for plotting the results (e.g. plot agent satisfaction)
df = []
for open_iter in range(3):
    df.append(pd.read_pickle('D:\\ABM\\Results\\Results_Run_'+ str(open_iter) + '.pkl'))

start_satisfaction = df[1][0]
#kll = pd.DataFrame(start_satisfaction.xs(0 , level="Step")["Satisfaction"])
kll = pd.DataFrame(start_satisfaction["Satisfaction"])
mean_satisfaction = pd.DataFrame(start_satisfaction["LandUse"])
mean_satisfaction.insert(0,'NewShape', start_satisfaction["NewShape"], True)

for m_run in range (1,3):
    #kll = df[m_run][0].xs(1 , level="Step")["Satisfaction"] (2, "Age", [21, 23, 24, 21], True)
    kll.insert(1,'Satisfaction'+ str(m_run), df[m_run][0]["Satisfaction"], True)
    #mean_satisfactioin = 

mean_satisfaction['Satisfaction'] = kll.mean(axis=1)
  
from json import dump

agent_satisfaction =mean_satisfaction
dict_mean =agent_satisfaction.to_dict()
cord = mean_satisfaction
coord = cord['NewShape']
cordif = coord.values.tolist()
No_agents= coord[0].values.tolist()
coord1 = []
coord2 =[]

geo_vision_f = geo_vision 
for run_iter in range(5):

    coord1.append(coord[run_iter].values.tolist())

    for agent_iter in range (len(No_agents)):
        #run_iter = 0
        #print(run_iter,agent_iter)
        coord21, coord22 =myProj(float(coord1[run_iter][agent_iter].y),float(coord1[run_iter][agent_iter].x))
        geo_vision_f['features'][agent_iter]['geometry']['coordinates'][0],geo_vision_f['features'][agent_iter]['geometry']['coordinates'][1]=coord21, coord22
        
        geo_vision_f['features'][agent_iter]['properties']['satisfaction']=mean_satisfaction['Satisfaction'][run_iter][agent_iter]

        del coord21, coord22    

        
    with open('D:\\ABM\\Json\\step_'+ str(run_iter)+'.json', 'w') as f:
        dump(geo_vision_f, f)
    geo_test = geo_vision_f

   
    
import matplotlib.pyplot as plt

coord = agent.__geo_interface__()
print(all_agents["crs"])
print(all_agents["type"])

geo_vision = {"crs": all_agents["crs"],
            "features": coord_f , 
            "type": all_agents["type"]}
#kkk = []
#kkk.append(coord['geometry']['coordinates'][0])
#kkk.append(coord['geometry']['coordinates'][1])
#coord['geometry']['coordinates'] = kkk
agent_satisfaction = df[0][0]
#agent_satisfaction = model.datacollector.get_agent_vars_dataframe()
agent_satisfaction.head()

#def count_change(agent_satisfaction):
NofHH = len(agent_satisfaction.xs(0 , level="Step")["NewShape"])
count2 = {}
count3 = {}
for NHH in range(NofHH):
    HH_N = NHH
    s1 = ['Household ', str(HH_N)] 
    HH_name = ''.join(s1)
    all_loc = agent_satisfaction.xs(HH_name , level="AgentID")["NewShape"]
    LandU = agent_satisfaction.xs(HH_name , level="AgentID")["LandUse"]
    #chg = 0
    cnt = 0
    for chg in range(len(all_loc)-1):
        k_dist = all_loc[chg].distance(all_loc[chg+1])
        if k_dist > 0:
            cnt = cnt+1
        
            #it = it+1
        k_dist = []
    if LandU[0] == 3:
        count3.update({HH_name: cnt})
    else:
        count2.update({HH_name: cnt})

import seaborn as sns; sns.set(color_codes=True)
from pylab import subplot

HH_count3 = count3
d3= HH_count3.values()
plt.figure()
subplot(2,1,1)
plt.hist(d3,bins = 30,
         color = 'blue', edgecolor = 'black')
plt.title('Formal Settelments')

HH_count2 = count2
d2= HH_count2.values()
subplot(2,1,2)
plt.hist(d2,bins = 30,
         color = 'blue', edgecolor = 'black')
plt.title('Informal Settelments')



LandU = agent_satisfaction.xs(HH_name , level="AgentID")["LandUse"]
end_satisfaction0LU = agent_satisfaction.xs(0, level="Step")["LandUse"]
end_satisfaction0SS = agent_satisfaction.xs(0, level="Step")["Satisfaction"]
end_satisfaction02 = []
end_satisfaction03 = []

for ik in range(len(end_satisfaction0SS)):
    if end_satisfaction0LU[ik]==3:
        end_satisfaction03.append(end_satisfaction0SS[ik])
    else:
        end_satisfaction02.append(end_satisfaction0SS[ik])

end_satisfaction_FB = []
end_satisfaction_Slum = []
end_satisfaction_FB_all = []
end_satisfaction_Slum_all = [] 
      
for itr in range (0,5):

    end_satisfactionLU = agent_satisfaction.xs(itr, level="Step")["LandUse"]
    end_satisfactionSS = agent_satisfaction.xs(itr, level="Step")["Satisfaction"]

    for itk in range(len(end_satisfaction0SS)):
        if end_satisfactionLU[itk]==3:
            end_satisfaction_FB.append(end_satisfactionSS[itk])
        else:
            end_satisfaction_Slum.append(end_satisfactionSS[itk])
     
    fig = plt.figure()    
    plt.hist(end_satisfaction_FB,bins = 40, range=[0, 1],
                 color = 'blue', edgecolor = 'black')   
    plt.title('Satisfaction Score Histogram for Formal Building HHs: Step = ' + str(itr))
    plt.xlabel('Satisfaction Score')
    plt.ylabel('No. HHs')
    #fig.savefig('\\ABM\\Results1\\FB_Hist_Step_'+ str(itr) + '.png', bbox_inches='tight')

    fig2 = plt.figure()     
    ax = sns.kdeplot(end_satisfaction_FB, bw=.15)
    plt.title('kde diagram of Satisfaction Score for Formal Building HHs: Step = ' + str(itr))
    plt.xlabel('Satisfaction Score')
    plt.ylabel('Density')
    #fig2.savefig('\\ABM\\Results1\\FB_Kde_Step_'+ str(itr) + '.png', bbox_inches='tight')    
    end_satisfaction_FB_all.append(end_satisfaction_FB)
    end_satisfaction_FB= [] 

     
    fig_Slum = plt.figure()    
    plt.hist(end_satisfaction_Slum,bins = 40, range=[0, 1],
                 color = 'blue', edgecolor = 'black')   
    plt.title('Satisfaction Score Histogram for Slum HHs: Step = ' + str(itr))
    plt.xlabel('Satisfaction Score')
    plt.ylabel('No. HHs')
    #fig.savefig('\\ABM\\Results1\\Slum_Hist_Step_'+ str(itr) + '.png', bbox_inches='tight')

    fig2_Slum = plt.figure()     
    ax = sns.kdeplot(end_satisfaction_Slum, bw=.15)
    plt.title('kde diagram of Satisfaction Score for Slum HHs: Step = ' + str(itr))
    plt.xlabel('Satisfaction Score')
    plt.ylabel('Density')
    #fig2_Slum.savefig('\\ABM\\Results1\\Slum_Kde_Step_'+ str(itr) + '.png', bbox_inches='tight')    
    end_satisfaction_Slum_all.append(end_satisfaction_Slum)
    end_satisfaction_Slum= [] 
 
 
   
import pandas as pd

# work off a copy of the dataset to preserve the original
ohlc_df = pd.DataFrame(end_satisfaction_Slum_all)

# aggregation frequency
time_grouper = 0.1 # try 'Y', '5Y', 'M', etc
ohlc_df_t = ohlc_df.transpose()
#ohlc_df = ohlc_df_t.set_index(0)
#boxplot = ohlc_df.boxplot()
plt.figure()
plt.boxplot(ohlc_df) 
plt.plot(ohlc_df)

mean = ohlc_df_t.mean()

fig2_Slum = plt.figure()     

ax = plt.plot(mean)
plt.title('kde diagram of Satisfaction Score for Slum HHs: Step = ')
plt.xlabel('Satisfaction Score')
plt.ylabel('Density')  


import matplotlib as mpl
import matplotlib.pyplot as pltt


# Create a figure instance
fig = plt.figure(1, figsize=(9, 6))

# Create an axes instance
ax = fig.add_subplot(111)

# Create the boxplot
#df.boxplot(showfliers=False, ax=ax)
bp = ax.boxplot(ohlc_df)
pltt.xticks(range(1,9), ohlc_df.columns[1:9],rotation=40,ha='right')


pltt.violinplot(ohlc_df,
                   showmeans=True,
                   showmedians=False)





