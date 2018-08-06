import csv
from node import Node

class Simulation:
    def __init__(self, wt, ht, nodes, unary_forces, binary_forces):
        self.wt = wt
        self.ht = ht
        self.center = Node(self.wt/2, self.ht/2)
        self.nodes = nodes
        self.unary_forces = unary_forces
        self.binary_forces = binary_forces
    
    def step(self):
        "Each step calculates the next moment of the simulation"
        self.update_neighbors()
        self.compute_forces()
        self.update_positions()
        
    def update_neighbors(self):
        """
        Each node has a list of neighbors, between whom forces are exerted.
        For now, each node is considered to include every node as its neighbors. 
        This is extremely inefficient, as we'll need to apply each force N*N 
        times, so later we might want to do something more clever like grouping
        nodes hierarchically. 
        """
        for node in self.nodes:
            node.neighbors = self.nodes
            
    def compute_forces(self):
        """
        Applies each unary force to each node, and each binary force to each pair of nodes.
        """
        for node in self.nodes:
            node.dx = 0
            node.dy = 0
        for node in self.nodes:
            if node.fixed: continue
            for force, strength in self.unary_forces:
                fx, fy = force(node, strength=strength, sim=self)
                node.dx += fx
                node.dy += fy
            for force, strength in self.binary_forces:
                for neighbor in node.neighbors:
                    if node is neighbor: continue
                    fx, fy = force(node, neighbor, strength=strength, sim=self)
                    node.dx += fx
                    node.dy += fy
            
    def update_positions(self):
        "Updates the position of each node based on the result of forces"
        for node in self.nodes:
            node.x += node.dx
            node.y += node.dy
            
    def export_csv(self, filename):
        with open(filename, 'w') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(["x", "y"])
            for node in self.nodes:
                writer.writerow([node.x, node.y])
        print("Saved simulation to {}".format(filename))
