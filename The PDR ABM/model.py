from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa_geo import GeoSpace, GeoAgent
from shapely.geometry import Point
import random
import networkx as nx
from location_agent import LocationAgent
from mesa.space import NetworkGrid
import shapely.geometry

def agent_satisfaction(agent):
    if isinstance(agent, LocationAgent):
        return None
    else:
        return agent.satisfaction

def agent_loc(agent):
    if isinstance(agent, LocationAgent):
        return None
    else:
        return agent.shape
    
def agent_LU(agent):
    if isinstance(agent, LocationAgent):
        return None
    else:
        return agent.landuse
    
def agent_shomo(agent):
    if isinstance(agent, LocationAgent):
        return None
    else:
        return agent.shomo
    
def agent_homo(agent):
    if isinstance(agent, LocationAgent):
        return None
    else:
        return agent.homo
    
def agent_workplace(agent):
    if isinstance(agent, LocationAgent):
        return None
    else:
        return agent.workplace

def jaccard_similarity(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    union = 2
    return float(intersection / union)

class RecoveryModel(Model):

    def __init__(self, locations, N1, scheduleClass, initialization=None, seed=None):
        if initialization == None:
            raise Exception("Initialization cannot be none")
            
        N = len(locations['features']) * N1 #N1 =density of housholds in one building
        #print(N)
        self.landuse = locations['features'][0]['landuse']
        #print(self.landuse[0])
        self.running = True
        self.num_agents = N
        self.schedule = scheduleClass(self)
        self.G = nx.complete_graph(self.num_agents)
        self.nw = NetworkGrid(self.G)
        self.grid = GeoSpace(crs='epsg:4326')   
        agent_kwargs = dict(model=self, unique_id='id')        
        self.grid.create_agents_from_GeoJSON(locations, agent=LocationAgent, **agent_kwargs)
        self.locations = list(self.grid.agents)
        self.initialize(initialization)
        self.datacollector = DataCollector(agent_reporters={"NewShape" : agent_loc,
                                                            "Satisfaction": agent_satisfaction,
                                                            "LandUse": agent_LU,
                                                            "Homo": agent_homo,
                                                            "WorkPlace": agent_workplace})
        self.grid.update_bbox()
        self.grid.create_rtree()
        
    def initialize(self, initialization):
        list_of_random_nodes = random.sample(self.G.nodes(), self.num_agents)

        for i in range(self.num_agents):
            agent, self.landuse1 = initialization.next('Household ' + str(i), self)
            self.nw.place_agent(agent, list_of_random_nodes[i])
            self.schedule.add(agent)
            self.grid.add_agent(agent) 

    def calculate_homophily(self):
        for i in range(self.G.number_of_nodes()):
            HH_homphily = 0
            total_homophily = 0
            c = 1
            for agent in self.G.node[i]['agent']:
                attr_self = [agent.workplace, agent.income, agent.education]
                agent_location = agent.shape
                
            for HH in self.locations:
                if HH.shape.contains(agent_location):
                    HH_polygon = HH.shape 
                
            neighbor_nodes = self.nw.get_neighbors(i, include_center=False)
            for node in neighbor_nodes:
                for nbr in self.G.node[node]['agent']:
                    attr_neighbor = [nbr.workplace, nbr.income, nbr.education]
                    self.G[i][node]['weight'] = jaccard_similarity(attr_self, attr_neighbor)
                    total_homophily = total_homophily + jaccard_similarity(attr_self, attr_neighbor)
                    neighbor_point = nbr.shape
                    if HH_polygon.contains(neighbor_point):
                        c = c + 1
                        HH_homphily = HH_homphily + jaccard_similarity(attr_self, attr_neighbor)
                    else:
                        pass
                        
            agent.homo = total_homophily
            agent.shomo = HH_homphily/c
            
              
        
    def step(self):
        #print (self.schedule.time)
        self.datacollector.collect(self)
        self.schedule.step()
        self.grid.create_rtree()
        self.calculate_homophily()