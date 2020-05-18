import numpy as np

class RandomSlumModel:
    def __init__(self):
        pass
    
    def choose_location(self, agent):
        return np.random.choice(agent.model.locations)
 

    def choose_location_new(self, agent):
        loc = np.random.choice(agent.model.locations, 12)
        #print(loc) 
        
        return loc    
   # def Land_Use(self, agent):
    #    return np.random.choice(agent.model.grid_code)
    