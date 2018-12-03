import csv
from node import Node
from voronoi import computeVoronoiDiagram
from inset_bezier import drawInsetBezier, drawShape
from itertools import combinations
from settings import *

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
        for force in self.unary_forces:
            for n in self.nodes:
                forceVector = force(n, sim=self)
                n.apply_force(forceVector)
        for force in self.binary_forces:
            for n1, n2 in combinations(self.nodes, 2):
                forceVector = force(n1, n2, sim=self)
                n1.apply_force(forceVector)
                n2.apply_force(forceVector * -1)
        for n in self.nodes:
            n.step()
         
    def drawRectangle(self):   
        noFill()
        stroke(255)
        rect(WIDTH/4, HEIGHT/4, WIDTH/2, HEIGHT/2)
            
    def export_csv(self, filename):
        with open(filename, 'w') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(["x", "y"])
            for node in self.nodes:
                writer.writerow([node.x, node.y])
        print("Saved simulation to {}".format(filename))
        
    def drawVoronoi(self):
        vertices, coeffs, edges, polygons = computeVoronoiDiagram([n.position for n in self.nodes])
        for siteId, edges in polygons.items():
            if not self._polygon_is_closed(edges): continue
            vertexIds = [v1 for lId, v1, v2 in edges] + [v2 for lId, v1, v2 in edges]
            vertexCoords = set([vertices[vId] for vId in vertexIds])
            vertexVectors = [PVector(x, y) for x, y in vertexCoords]
            vertexVectors = self._order_vertices(self.nodes[siteId].position, vertexVectors)
            
            if SHOW_VORONOI_BOUNDARIES:
                stroke(0,0,255)
                noFill()
                drawShape(vertexVectors)
            if SHOW_VORONOI_BEZIERS:
                shp = ConvexPolygon(vertexVectors).inset(VORONOI_BEZIER_INSET)
                if SHOW_VORONOI_INSETS:
                    stroke(0, 255, 0)
                    shp.draw()
                
                stroke(255,255,0)
                drawInsetBezier(vertexVectors, inset=VORONOI_BEZIER_INSET, drawInsetShape=SHOW_VORONOI_INSETS)
                        
    def _polygon_is_closed(self, edges):
        for edge in edges:
            lineId, v1, v2 = edge
            if v1 == -1 or v2 == -1:
                return False
        return True
    
    def _order_vertices(self, center, vertices):
        """
        We are given a bunch of edges that make a polygon around a node, but they
        are sometimes in the wrong order. So we can take a vector pointing straight up
        from the center, and take the vector from the center to each vertex. We can sort
        the points by the size of angle their corresponding vectors make with the upward
        vector. 
        """
        up = PVector(0, 1)
        return sorted(vertices, key=lambda v: self._cos(up, v - center))
    
    def label_nodes(self):
        fill(200)
        for i, n in enumerate(self.nodes):
            text(i, n.position.x + 10, n.position.y + 10)
            
    def _cos(self, v1, v2):
        "The native PVector implementation does not retain sign information, so we re-implement it here."
        sign = 1 if v2.x >= v1.x else -1
        return sign * PVector.angleBetween(v1, v2)
        
        
        
        
        
        
        
