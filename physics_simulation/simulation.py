import csv
from node import Node
from voronoi import computeVoronoiDiagram
from inset_bezier import drawInsetBezier, drawShape
from itertools import combinations
from convex_polygon import ConvexPolygon
from collections import defaultdict
from functions import sample_dirichlet
from settings import *

class Simulation:
    def __init__(self, wt, ht, nodes, unary_forces, binary_forces):
        self.wt = wt
        self.ht = ht
        self.center = Node(self.wt/2, self.ht/2)
        self.nodes = nodes
        self.unary_forces = unary_forces
        self.binary_forces = binary_forces
        self.dirichlet_samples = [sample_dirichlet(VORONOI_VERTEX_TRIANGLE_SPACING) for i in range(len(nodes) ** 2)]
    
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
        if SHOW_VORONOI_VERTEX_TRIANGLES or SHOW_VORONOI_VERTEX_BEZIERS:
            neighbors = defaultdict(set)
            def edgeKey(edge):
                lId, aId, bId = edge
                return (vertices[aId][0] + vertices[bId][0], vertices[aId][1] + vertices[bId][1])
            sortedEdges = sorted(edges, key=edgeKey)
            for i, (lineId, aId, bId) in enumerate(sortedEdges):
                if aId == -1 or bId == -1: continue
                a = PVector(*vertices[aId])
                b = PVector(*vertices[bId])
                if USE_RANDOM_VORONOI_VERTEX_TRIANGLE_SPACING:
                    left, space, right = self.dirichlet_samples[i]
                else:
                    left, space, right = [1.0/3] * 3
                neighbors[aId].add(a + (b-a) * left)
                neighbors[bId].add(b + (a-b) * right)
            for id, points in neighbors.items():
                try:
                    shp = ConvexPolygon(list(points))
                    if SHOW_VORONOI_VERTEX_TRIANGLES:
                        stroke(255, 0, 255)
                        shp.draw()
                    if SHOW_VORONOI_VERTEX_BEZIERS:
                        stroke(0, 255, 255)
                        shp.drawBezier()
                except ConvexPolygon.TooFewPoints:
                    continue
        
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
            if SHOW_VORONOI_INSETS or SHOW_VORONOI_BEZIERS:
                try:
                    randomSeed(siteId)
                    insetLength = VORONOI_BEZIER_INSET_MEAN + randomGaussian() * VORONOI_BEZIER_INSET_STD
                    insetShape = ConvexPolygon(vertexVectors).inset(insetLength)
                    if SHOW_VORONOI_INSETS:
                        stroke(0, 255, 0)
                        insetShape.draw()
                    if SHOW_VORONOI_BEZIERS:
                        stroke(255,255,0)
                        insetShape.drawBezier()
                except (ConvexPolygon.TooFewPoints, ConvexPolygon.NoInset, ZeroDivisionError):
                    continue
                                            
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
        
        
        
        
        
        
        
