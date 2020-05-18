# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 15:05:47 2019

@author: Saman Ghaffarian
"""
import numpy as np
from houshold_agent import HouseholdAgent
import pandas
import random
import xlrd
import time

    
def sub_sort1(self, model):
    sub_sort1 = []
    sub_sort2 = []
    sub_sort3 = []
    sub_sort4 = []
        #print(len(model.grid.agents))
        
    self.sub_sort = []
    for y1 in range(len(model.grid.agents)):
        sub_sort1.append(int(model.grid.agents[y1].pointid))
        #sub_sort2.append(int(model.grid.agents[y1].grid_code))
        sub_sort2.append(int(model.grid.agents[y1].Name))
        sub_sort3.append(int(model.grid.agents[y1].idx_id))
        sub_sort4.append(int(model.grid.agents[y1].RASTERVALU))      
        
    sub_sort = sub_sort1
    sub_sort.append (sub_sort2)
    sub_sort.append (sub_sort3)
    sub_sort.append (sub_sort4)
    
    return self.sub_sort

_start_time = time.time()

def tic():
    global _start_time 
    _start_time = time.time()

def tac():
    t_sec = round(time.time() - _start_time)
    (t_min, t_sec) = divmod(t_sec,60)
    (t_hour,t_min) = divmod(t_min,60) 
    print('Time passed: {}hour:{}min:{}sec'.format(t_hour,t_min,t_sec))
    
class AllHouseHoldsAgent(HouseholdAgent):
    def __init__(self, unique_id, model, shape, choice_model=None, satisfaction_model=None):
        super().__init__(unique_id, model, shape)

        
        self.choice_model = choice_model
        self.satisfaction_model = satisfaction_model
        #print(model.grid.agents['LocationAgent'])
        #self.landuse = model.grid.agents['LcationAgent']['grid_code']
        
        kkk = unique_id.split()
        lll = int(kkk[1])
      
        if lll==0:
            self.sub_sort = sub_sort1(self, model)
        
        
        #self.landuse = model.grid.agents[lll].grid_code
        self.landuse = model.grid.agents[lll].Name
        self.newLU = model.grid.agents[lll].RASTERVALU
        if self.newLU is 2 or 3:
            self.damaged = 'yes'
        else:
            self.damaged = 'no'
        
        self.distance = model.grid.agents[lll].distance

        self.job = 0
        self.workplace= 0
        self.income = 0
        self.education = 0
        self.homo = 0
        self.shomo = 0
        #tic()
        self.initialize()
        #tac()

    def initialize(self):
        
        job = ['yes', 'no']
        self.job= np.random.choice(job, 1, p=[0.92, 0.08])[0]
        
        workplace= ['farm', 'fishing', 'construction', 'service']
        p_FB_work= [0, 0, 0, 1]
        workplace_slum = ['farm', 'fishing', 'construction']
        p_slum_work = [0.45, 0.45, 0.1]
        
        #print(self.landuse)
        
        if self.landuse == 2:
            if self.job == "yes":
                self.workplace = np.random.choice(workplace_slum, 1, p = p_slum_work)[0]
        elif self.landuse == 3:
            if self.job== "yes":
                self.workplace = np.random.choice(workplace, 1, p = p_FB_work)[0]
        
        
        if self.workplace != 'service':
            self.distance = 0.1

		
        if self.job == "yes":
            if self.workplace== "service":
                self.income = "high"
            elif self.workplace== "farm" or "fishing" or "construction":
                self.income = "low"

        else:
            self.income = 0
            
        
        if self.job == "yes":
            job1 = 1
        else:
            job1 = 0
            
        if self.income == "low":
            income = 0.5
        elif self.income == "high":
            income = 1
        else:
            income = self.income
        
        if self.landuse == 2:
            education =  0.5
        elif self.landuse == 3:
            education =  1

               
        D_normalized = float(self.distance)
        #print (self.workplace, self.landuse, self.income, income, education, D_normalized)
        self.satisfaction = job1*(income/education)*(1-D_normalized)    
        self.homo = 0
        self.shomo = 0
        self.attr = [self.job, self.workplace, self.income, self.distance]
        
        
    def step(self):    

        D_normalized = float(self.distance)

        if self.landuse == 2:
            education =  0.5
        elif self.landuse == 3:
            education =  1
            
        #education =  1
        
        if self.income == "low":
            income = 0.5
        elif self.income == "high":
            income = 1
        else:
            income = self.income
                
        #print(income)
        if self.job == "yes":
            job1 = 1
        else:
            job1 = 0
            
        job1 = float(job1)
        income = float(income)
        education = float(education)
        DImp = 1
        
        # Reading an excel file using Python      
        # Give the location of the file 
        loc = ("C:\\ABM\\Data\\Recovery_Steps\\RC_Steps2.xlsx") 
          
        # To open Workbook 
        wb = xlrd.open_workbook(loc) 
        sheet = wb.sheet_by_index(0) 
          
                       
        if self.model.schedule.time == 1: # Event time == step2
            if self.damaged == "yes":
                DImp = 0
            elif self.damaged == "no":
                DImp = 1
               
        if self.model.schedule.time >= 2: # Early recovery == step3      
            #print(self.model.schedule.time)  
            #print(self.landuse)               
            if self.damaged == "yes":
                #print(self.landuse)
                #print(self.damaged)
                if self.landuse == 2:                       
                    still_damaged = ['yes', 'no']
                    p_still_damaged = [1-(sheet.cell_value(4,(self.model.schedule.time+1))), sheet.cell_value(4,(self.model.schedule.time+1))]
                    #print(p_still_damaged, self.landuse, self.damaged)
                    self.damaged = np.random.choice(still_damaged, 1, p = p_still_damaged)[0]
                    #print(self.damaged)
                    #print((sheet.cell_value(1,(self.model.schedule.time+1))))
                elif self.landuse == 3:
                    still_damaged = ['yes', 'no']
                    p_still_damaged = [1-(sheet.cell_value(5,(self.model.schedule.time+1))), sheet.cell_value(5,(self.model.schedule.time+1))]
                    #print(p_still_damaged, self.landuse)
                    self.damaged = np.random.choice(still_damaged, 1, p = p_still_damaged)[0]
                    #print(self.damaged)
            if self.damaged == "yes":
                    DImp = 0
            elif self.damaged == "no":
                DImp = 1
        p_still_damaged = []    

       
        #satisfaction score calculation
        self.satisfaction = DImp*job1*(income/education)*(1-D_normalized)
        if self.satisfaction >1:
            print(self.satisfaction, job1, self.income, income, education)
            
        self.update_coefficients(sheet)        
        p_satisfaction, p_satisfaction2 = self.mean_satisfaction()
        #threshold = np.random.rand() # selects a random threshold
        
        normalized_satisfaction = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        threshold = np.random.choice(normalized_satisfaction, 1, p = p_satisfaction)[0]
        #print(threshold)
        
        if threshold > self.satisfaction:
            choice_type= ['only_job', 'only_location', 'job+location']
            self.choice_type= np.random.choice(choice_type, 1, p=[0.4, 0.4, 0.2])[0]
            if self.choice_type == "only_job":
                
                listtt= self.only_jobF(sheet)

                SortIndex = np.argsort(listtt)[::-1][:10] # sort the best choices
                RandNum = random.randint(0,1)
                SelectedIndex = SortIndex[RandNum] # select one of the 7 best available choices

                if listtt[SelectedIndex] > self.satisfaction : #if the selected job provides higher satisfaction score than current one
                    self.job = self.ListforBest[SelectedIndex][0]
                    self.workplace = self.ListforBest[SelectedIndex][1]
                    self.income = self.ListforBest[SelectedIndex][2]
                    self.distance = self.ListforBest[SelectedIndex][3]
                    self.damaged = self.ListforBest[SelectedIndex][4]
                
            elif self.choice_type == "only_location":
                chosen_locations = self.choice_model.choose_location_new(self)
                SelectedIndex, list_distance, list_satis = self.only_loc(sheet)
                if list_satis[SelectedIndex] > self.satisfaction:
                    self.shape = chosen_locations[SelectedIndex].shape
 
            elif self.choice_type == "job+location":
                chosen_locations = self.choice_model.choose_location_new(self)
                listtt, SelectedIndex2, list_distance = self.job_and_loc(sheet)
                
                SortIndex = np.argsort(listtt)[::-1][:10] # sort the best choices
                #SortIndex = np.argsort(listtt)
                RandNum = random.randint(0,1)
                SelectedIndex = SortIndex[RandNum] # select one of the 10 best available choices
                #print (SortIndex)
                #print (SelectedIndex)
                if listtt[SelectedIndex] > self.satisfaction :
                    self.job = self.ListforBest[SelectedIndex][0]
                    self.workplace = self.ListforBest[SelectedIndex][1]
                    self.income = self.ListforBest[SelectedIndex][2]
                    self.distance = self.ListforBest[SelectedIndex][3]
                    self.damaged = self.ListforBest[SelectedIndex][4]
                    self.shape = chosen_locations[SelectedIndex2].shape
                    
            else:
                self.choice_type = 0 # No change
              
        self.update_distance()
        p_still_damaged = [] 
        self.ListforBest=0

        
    def job_and_loc(self,sheet):
        kk = []
        self.ListforBest = []
        for itm in range (0,2):
            self.update_coefficients(sheet)
            if self.job == "yes":
                if self.workplace == "service":
                    self.income = "high"
                elif self.workplace== "farm" or "fishing" or "construction":
                    self.income = "low"
            else:
                self.income = 0
                                    
            if self.income == "low":
                income = 0.5
            elif self.income == "high":
                income = 1
            else:
                income = self.income
                    
                #print(income)
            if self.job == "yes":
                job1 = 1
            else:
                job1 = 0
             
            
            if self.landuse == 2:
                education =  0.5
            elif self.landuse == 3:
                education =  1
            DImp = 1            
              
            
            if self.model.schedule.time == 1: # Event time == step2
                if self.damaged == "yes":
                    DImp = 0
                elif self.damaged == "no":
                    DImp = 1
           
            if self.model.schedule.time >= 2: # Early recovery == step3      
               
                if self.damaged == "yes":
                    if self.landuse == 2:                       
                        still_damaged = ['yes', 'no']
                        p_still_damaged = [1-(sheet.cell_value(4,(self.model.schedule.time+1))), sheet.cell_value(4,(self.model.schedule.time+1))]
                        self.damaged = np.random.choice(still_damaged, 1, p = p_still_damaged)[0]

                    elif self.landuse == 3:
                        still_damaged = ['yes', 'no']
                        p_still_damaged = [1-(sheet.cell_value(5,(self.model.schedule.time+1))), sheet.cell_value(5,(self.model.schedule.time+1))]
                        self.damaged = np.random.choice(still_damaged, 1, p = p_still_damaged)[0]
                if self.damaged == "yes":
                        DImp = 0
                elif self.damaged == "no":
                    DImp = 1
            
            SelectedIndex2, list_distance, list_satis = self.only_loc(sheet)
            self.distance = list_distance[SelectedIndex2]
            D_normalized = float(self.distance)    
            job1 = float(job1)
            income = float(income)
            s_new = DImp*job1*(income/education)*(1-D_normalized)            
            kk.append(s_new)
            self.ListforBest.append ( [self.job, self.workplace, self.income, self.distance, self.damaged])


        return kk, SelectedIndex2, list_distance
         
            
    
    def only_loc(self, sheet):

        list_distance = []
        kk = []
        for itm in range (0,2):
            distance = [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
            p_FB_distance = [0.274, 0.408, 0.198, 0.062, 0.031, 0.011, 0.006, 0.005, 0.002, 0.002, 0.001]
            if self.workplace == 'service':
                list_distance.append(np.random.choice(distance, 1, p = p_FB_distance)[0])
            else:
                list_distance.append(0.1)
            
            if self.job == "yes":
                if self.workplace == "service":
                    self.income = "high"
                elif self.workplace== "farm" or "fishing" or "construction":
                    self.income = "low"

            else:
                self.income = 0
                                    
            if self.income == "low":
                income = 0.5
            elif self.income == "high":
                income = 1
            else:
                income = self.income
                    
                #print(income)
            if self.job == "yes":
                job1 = 1
            else:
                job1 = 0
             
            
            if self.landuse == 2:
                education =  0.5
            elif self.landuse == 3:
                education =  1
            DImp = 1
            

            if self.model.schedule.time == 1: # Event time == step2
                if self.damaged == "yes":
                    DImp = 0
                elif self.damaged == "no":
                    DImp = 1
           
           
            if self.model.schedule.time >= 2: # Early recovery == step3                
                if self.damaged == "yes":
                    if self.landuse == 2:                       
                        still_damaged = ['yes', 'no']
                        p_still_damaged = [1-(sheet.cell_value(4,(self.model.schedule.time+1))), sheet.cell_value(4,(self.model.schedule.time+1))]
                        self.damaged = np.random.choice(still_damaged, 1, p = p_still_damaged)[0]

                    elif self.landuse == 3:
                        still_damaged = ['yes', 'no']
                        p_still_damaged = [1-(sheet.cell_value(5,(self.model.schedule.time+1))), sheet.cell_value(5,(self.model.schedule.time+1))]
                        self.damaged = np.random.choice(still_damaged, 1, p = p_still_damaged)[0]
                if self.damaged == "yes":
                        DImp = 0
                elif self.damaged == "no":
                    DImp = 1

            D_normalized = float(list_distance[itm])    
            job1 = float(job1)
            income = float(income)
            s_new = DImp*job1*(income/education)*(1-D_normalized)
            kk.append(s_new)
           
        SortIndex = np.argsort(kk)[::-1][:10] # sort the best choices
        RandNum = random.randint(0,1)
        SelectedIndex = SortIndex[RandNum] # select one of the 7 best available choices
        if kk[SelectedIndex] > self.satisfaction:
            self.distance = list_distance[SelectedIndex]

        return SelectedIndex, list_distance, kk
                
    def only_jobF(self,sheet):
        kk = []
        self.ListforBest = []
        for itm in range (0,2):
            self.update_coefficients(sheet)
            if self.job == "yes":
                if self.workplace == "service":
                    self.income = "high"
                elif self.workplace== "farm" or "fishing" or "construction":
                    self.income = "low"
            else:
                self.income = 0
                                    
            if self.income == "low":
                income = 0.5
            elif self.income == "high":
                income = 1
            else:
                income = self.income
                    
                #print(income)
            if self.job == "yes":
                job1 = 1
            else:
                job1 = 0
             
            
            if self.landuse == 2:
                education =  0.5
            elif self.landuse == 3:
                education =  1
            DImp = 1
        
            if self.model.schedule.time == 1: # Event time == step2
                if self.damaged == "yes":
                    DImp = 0
                elif self.damaged == "no":
                    DImp = 1          
           
            if self.model.schedule.time >= 2: # Early recovery == step3      
              
                if self.damaged == "yes":
                    #print(self.landuse)
                    if self.landuse == 2:                       
                        still_damaged = ['yes', 'no']
                        p_still_damaged = [1-(sheet.cell_value(4,(self.model.schedule.time+1))), sheet.cell_value(4,(self.model.schedule.time+1))]
                        self.damaged = np.random.choice(still_damaged, 1, p = p_still_damaged)[0]
                    elif self.landuse == 3:
                        still_damaged = ['yes', 'no']
                        p_still_damaged = [1-(sheet.cell_value(5,(self.model.schedule.time+1))), sheet.cell_value(5,(self.model.schedule.time+1))]
                        self.damaged = np.random.choice(still_damaged, 1, p = p_still_damaged)[0]
                if self.damaged == "yes":
                        DImp = 0
                elif self.damaged == "no":
                    DImp = 1
     
            self.update_distance()
            D_normalized = float(self.distance)    
            job1 = float(job1)
            income = float(income)
            s_new = DImp*job1*(income/education)*(1-D_normalized)            
            kk.append(s_new)
            self.ListforBest.append ( [self.job, self.workplace, self.income, self.distance, self.damaged])

        return kk
                
                
    def mean_satisfaction(self):
        agent_satisfaction = self.model.datacollector.get_agent_vars_dataframe()
        agent_satisfaction.head()
        stp_satsf = self.model.schedule.time
        all_satisfaction = agent_satisfaction.xs(stp_satsf, level="Step")["Satisfaction"]  
        hist = np.histogram(all_satisfaction, bins=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
        histt = hist[0]
        p_hist=[]
        p_hist2 =[]
        for h in range(len(histt)):
            p_hist.append(histt[h]/sum(histt))
            p_hist2.append((1-histt[h])/sum(histt))

        return p_hist, p_hist2
    
    
    
    def update_coefficients(self,sheet):
                
        HHs = [100, 40, 50]
        PB_Farm_Slum = [0.6, 0.1, 0.15] ; PB_Fishing_Slum = [0.4, 0.6, 0.4]; PB_Construction_Slum = [0, 0.3, 0.45]; PB_Services_Slum = [0, 0, 0]
        PB_Farm_FB = [0.1, 0.1, 0.1]; PB_Fishing_FB = [0.1, 0.1, 0.1]; PB_Construction_FB = [0.1, 0.1, 0.1]; PB_Services_FB = [0.7, 0.7, 0.7]
        df_HHs_Jobs = pandas.DataFrame(data={"HHs": HHs, "PB_Farm_Slum": PB_Farm_Slum, "PB_Fishing_Slum": PB_Fishing_Slum, "PB_Construction_Slum": PB_Construction_Slum, "PB_Services_Slum": PB_Services_Slum,
                                             "PB_Farm_FB": PB_Farm_FB, "PB_Fishing_FB": PB_Fishing_FB, "PB_Construction_FB": PB_Construction_FB, "PB_Services_FB": PB_Services_FB})
        #print(df_HHs_Jobs)
        sorted_homo_indices = []         
        if self.model.schedule.time >= 1: # Early recovery == step3
          homo_choice = np.random.randint(2)

          
          agent_all = self.model.datacollector.get_agent_vars_dataframe()
          agent_all.head()
          stp_satsf = self.model.schedule.time
          all_homo = agent_all.xs(stp_satsf, level="Step")["Homo"] 
          all_workplace = agent_all.xs(stp_satsf, level="Step")["WorkPlace"]
          sorted_homo_indices = all_homo.argsort()[-5:][::-1]
          workplaces_homo = []

          for wh in range(len(sorted_homo_indices)):
              workplaces_homo.append(all_workplace[sorted_homo_indices[wh]])
          p_homo = [workplaces_homo.count('farm')*0.2,workplaces_homo.count('fishing')*0.2,workplaces_homo.count('construction')*0.2,workplaces_homo.count('service')*0.2]
          if self.landuse == 2:
              p_homo = [(workplaces_homo.count('farm')+workplaces_homo.count('service'))*0.2,workplaces_homo.count('fishing')*0.2,workplaces_homo.count('construction')*0.2,0]

          Farm_FB = (1-(sheet.cell_value(2,(self.model.schedule.time+1))))/3
          Fishing_FB = (1-(sheet.cell_value(2,(self.model.schedule.time+1))))/3
          Construction_FB = 1-Farm_FB-Fishing_FB-sheet.cell_value(2,(self.model.schedule.time+1))
          p_FB_work = [Farm_FB, Fishing_FB, Construction_FB,sheet.cell_value(2,(self.model.schedule.time+1))]
 
          workplace= ['farm', 'fishing', 'construction', 'service']
          stp = 2
          p_slum_work= [df_HHs_Jobs.PB_Farm_Slum[stp],df_HHs_Jobs.PB_Fishing_Slum[stp],df_HHs_Jobs.PB_Construction_Slum[stp],df_HHs_Jobs.PB_Services_Slum[stp]]
          
          if homo_choice == 1:
              if self.landuse == 2:
                  if self.model.schedule.time >= 3:
                      p_slum_work = []
                      p_slum_work = [0.4, 0.4, 0.2, 0]   
                  p_slum_all = [(p_slum_work[0]+p_homo[0])/2,(p_slum_work[1]+p_homo[1])/2,(p_slum_work[2]+p_homo[2])/2,(p_slum_work[3]+p_homo[3])/2]

                  if self.job == "yes":
                     self.workplace = np.random.choice(workplace, 1, p = p_slum_all)[0]
                     
              elif self.landuse == 3:
                  p_FB_all = [(p_FB_work[0]+p_homo[0])/2,(p_FB_work[1]+p_homo[1])/2,(p_FB_work[2]+p_homo[2])/2,(p_FB_work[3]+p_homo[3])/2]
                  if self.job== "yes":
                     self.workplace = np.random.choice(workplace, 1, p = p_FB_all)[0]
    
          if homo_choice == 0:
              if self.landuse == 2:
                  if self.job == "yes":
                     self.workplace = np.random.choice(workplace, 1, p = p_slum_work)[0]
                     
              elif self.landuse == 3:
                  if self.job== "yes":
                     self.workplace = np.random.choice(workplace, 1, p = p_FB_work)[0]
    
                  if self.model.schedule.time >= 3: # Post-disaster recovery/normal condition >= step4
                    workplace= ['farm', 'fishing', 'construction', 'service']
                    #stp = 2
                    p_slum_work = [0.4, 0.4, 0.2, 0]
                  
                    if self.landuse == 2:
                        if self.job == "yes":
                           self.workplace = np.random.choice(workplace, 1, p = p_slum_work)[0]
        pass
    
    def update_distance(self):
        distance = [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        p_FB_distance = [0.274, 0.408, 0.198, 0.062, 0.031, 0.011, 0.006, 0.005, 0.002, 0.002, 0.001]
        p_Slum_distance = [0.3, 0.4, 0.2, 0.1, 0, 0, 0, 0, 0, 0, 0]
        if self.workplace == 'service':
            self.distance = np.random.choice(distance, 1, p = p_FB_distance)[0]
        else:
            self.distance = np.random.choice(distance, 1, p = p_Slum_distance)[0]
        pass
    

    def __geo_interface__(self):
        props = super().__geo_interface__()
        coord = props
        kkk = []
        kkk.append(coord['geometry']['coordinates'][0])
        kkk.append(coord['geometry']['coordinates'][1])
        coord['geometry']['coordinates'] = kkk
        props = coord
        # Remove non serializable attributes
        del props['properties']['choice_model']
        del props['properties']['satisfaction_model']
        del props['properties']['attr']
        #del props['properties']['choice_type']
        #del props['properties']['ListforBest']
        del props['properties']['job']
        del props['properties']['newLU']
        del props['properties']['pos']
        del props['properties']['unique_id']
        del props['properties']['workplace']
        #del props['properties']['coefficients']

        return props