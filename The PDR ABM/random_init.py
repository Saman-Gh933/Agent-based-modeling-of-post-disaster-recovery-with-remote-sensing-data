from houshold_agent import HouseholdAgent
from polygon_utils import random_point_within

import numpy as np

class RandomInitialization:
    def __init__(self, **kwargs):
        if 'AgentClass' not in kwargs:
            raise Exception("RandomInitialization requires an AgentClass keyword argument")
        self.AgentClass = kwargs['AgentClass']
        self.kwargs = kwargs
        del self.kwargs['AgentClass']
        self.landuse1 = []
    
    def next(self, name, model):
        chosen_location = np.random.choice(model.locations)
        self.landuse1 = chosen_location.Name
        return self.AgentClass(name, model, random_point_within(chosen_location.shape), **self.kwargs), self.landuse1

