import numpy as np
import random


class RandomHHModel:
    def __init__(self):
        pass
    
    def choose_location(self, agent):
        
        while True:
            R_N = random.randrange(len(agent.model.locations))
            LU = agent.model.grid_code[R_N]
            if LU == self.landuse:
                break
        loc = agent.model.locations[R_N]
        return loc
 

    def choose_location_new(self, agent):

        while True:
            randomList = random.sample(range(0, len(agent.model.locations)), 10)          
            LU = agent.model.grid_code[randomList]
            if LU == self.landuse:
                break          
        loc = agent.model.locations[randomList]     
        return loc    

    