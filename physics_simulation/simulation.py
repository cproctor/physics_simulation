from particle import Particle
from voronoi import computeVoronoiDiagram
from itertools import combinations
from collections import defaultdict
from settings import *

class Simulation:
    eta = 0.01
    
    def __init__(self, s=None):
        self.s = s or DefaultSettings      
        self.particles = self.s.PARTICLES
        self.center = Particle(self.s.WIDTH/2, self.s.HEIGHT/2)
        
    def render(self):
        if self.s.SHOW_PARTICLES: 
            for particle in self.particles:
                particle.render(self.s)
    
    def step(self):
        "Each step calculates the next moment of the simulation"
        for force in self.s.UNARY_FORCES:
            for n in self.particles:
                forceVector = force(n, self.s, sim=self)
                n.apply_force(forceVector)
        for force in self.s.BINARY_FORCES:
            for n1, n2 in combinations(self.particles, 2):
                forceVector = force(n1, n2, self.s, sim=self)
                n1.apply_force(forceVector)
                n2.apply_force(forceVector * -1)
        for n in self.particles:
            n.step()
        
    def add_control_node(self, x, y):
        """
        Control nodes are a way to control the behavior of the simulation. 
        They are placed in position and never move. They affect other particles
        via binary forces. The justification for control nodes is that they are useful; 
        there are no physical particles that correspond to control particles.
        """
        controlNode = Particle(x, y, control=True, fixed=True)
        if min(particle.dist(controlNode) for particle in self.particles) > self.eta:
            self.particles.append(controlNode)
            
    def positions(self, with_control_nodes=True):
        """
        Returns PVector positions of all particles (and optionally control nodes) 
        """
        return [p.position for p in self.particles if (not p.control or with_control_nodes)]
