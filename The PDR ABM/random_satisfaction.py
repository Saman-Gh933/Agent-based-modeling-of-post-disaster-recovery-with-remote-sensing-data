import numpy as np

class RandomSatisfaction():
    def __init__(self):
        pass
    
    def satisfaction(self, agent, omegas):
        o = np.reshape(omegas, (1, 1))
        return np.asscalar(np.dot(o, self.satisfiers(agent)))
    
    def satisfiers(self, agent):

        return np.random.rand(1, 1)

class UtilitySatisfaction():
    def __init__(self):
        pass
    
    def satisfaction(self, agent, omegas):
        return agent.shomo
        