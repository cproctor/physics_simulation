from convex_polygon import ConvexPolygon
from voronoi import SiteList, Context, voronoi

class Mesh:
    """
    A mesh is a graph (nodes and edges between nodes) which  
    nodes should be a list of PVectors.
    This gets pretty mathy pretty fast--I'm happy to talk through it if anyone's interested, 
    but I 
    """
    
    def __init__(self, nodes, s):
        self.s = s
        self.nodes = nodes
        self.sites = SiteList(nodes)
        self.context = Context()
        voronoi(self.sites, self.context)
        
    def render(self):
        if self.s.SHOW_MESH_TRIANGLES:
            self.s.MESH_TRIANGLE_STYLE()
            self.render_mesh()
        if self.s.SHOW_VORONOI_SITES:
            self.s.VORONOI_SITE_STYLE()
            self.render_voronoi_sites()
        if self.s.SHOW_VORONOI_SITE_INSETS:
            self.s.VORONOI_SITE_INSET_STYLE()
            self.render_voronoi_site_insets()
        if self.s.SHOW_VORONOI_INSET_BEZIERS:
            self.s.VORONOI_INSET_BEZIER_STYLE()
            self.render_voronoi_inset_beziers()
        
    def render_mesh(self):
        for tri in self.triangles():
            tri.render()
            
    def render_voronoi_sites(self):
        for pgon in self.site_polygons():
            pgon.render()
            
    def render_voronoi_site_insets(self):
        for insetLength in self.s.VORONOI_SITE_INSETS:
            for pgon in self.site_polygons():
                try:
                    pgon.inset(insetLength).render()
                except (ConvexPolygon.NoInset, ConvexPolygon.TooFewPoints, ZeroDivisionError):
                    pass
                    
    def render_voronoi_inset_beziers(self):
        for pgon in self.site_polygons():
            try:
                pgon.inset(self.s.VORONOI_BEZIER_INSET).render_bezier()
            except (ConvexPolygon.NoInset, ConvexPolygon.TooFewPoints, ZeroDivisionError):
                pass
        
    def triangles(self):
        tris = [[self.nodes[i] for i in tri] for tri in self.context.triangles]
        return [ConvexPolygon(tri) for tri in tris]
    
    def site_polygons(self):
        "Returns ConvexPolygons for each closed voronoi site"
        closedPolygons = [(siteId, pgon) for siteId, pgon in self.context.polygons.items() if self._site_is_closed(pgon)]
        return [self._build_convex_polygon(siteId, pgon) for siteId, pgon in closedPolygons]
        
    def _build_convex_polygon(self, siteId, pgon):
        "pgon should be a list of (lineId, vertexId0, vertexId1)"
        vertexIds = set([e[1] for e in pgon] + [e[2] for e in pgon])
        vertexCoords = [self.context.vertices[vId] for vId in vertexIds]    
        vertexVectors = self._order_vertices(self.nodes[siteId], [PVector(x, y) for x, y in vertexCoords])
        return ConvexPolygon(vertexVectors)     
          
    def _site_is_closed(self, edges):
        return all(self._edge_is_finite(e) for e in edges)
    
    def _edge_is_finite(self, edge):
        return -1 not in edge
    
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
    
    def _cos(self, v1, v2):
        "The native PVector implementation does not retain sign information, so we re-implement it here."
        sign = 1 if v2.x >= v1.x else -1
        return sign * PVector.angleBetween(v1, v2)
        
        
        
        
        
#------------------------------------------------------------------
def computeVoronoiDiagram(points):
    """ Takes a list of point objects (which must have x and y fields).
        Returns a 3-tuple of:

           (1) a list of 2-tuples, which are the x,y coordinates of the 
               Voronoi diagram vertices
           (2) a list of 3-tuples (a,b,c) which are the equations of the
               lines in the Voronoi diagram: a*x + b*y = c
           (3) a list of 3-tuples, (l, v1, v2) representing edges of the 
               Voronoi diagram.  l is the index of the line, v1 and v2 are
               the indices of the vetices at the end of the edge.  If 
               v1 or v2 is -1, the line extends to infinity.
    """
    siteList = SiteList(points)
    context  = Context()
    voronoi(siteList,context)
    return (context.vertices, context.lines, context.edges, context.polygons)

#------------------------------------------------------------------
def computeDelaunayTriangulation(points):
    """ Takes a list of point objects (which must have x and y fields).
        Returns a list of 3-tuples: the indices of the points that form a
        Delaunay triangle.
    """
    siteList = SiteList(points)
    context  = Context()
    context.triangulate = true
    voronoi(siteList,context)
    return context.triangles

        
        
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
            
            if SHOW_NESTED_VORONOI_INSETS:
                insetShape = ConvexPolygon(vertexVectors)
                noFill()
                stroke(255, 255, 255)
                for i in range(0, 100, 20):
                    try:
                        insetShape.inset(i).draw()
                    except (ConvexPolygon.NoInset, ConvexPolygon.TooFewPoints, ZeroDivisionError):
                        continue
                        
            if SHOW_VORONOI_BOUNDARIES:
                stroke(0,0,255)
                noFill()
                drawShape(vertexVectors)
            if SHOW_VORONOI_INSETS or SHOW_VORONOI_BEZIERS:
                noFill()
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
        for i, n in enumerate(self.nodes):
            text(i, n.position.x + 10, n.position.y + 10)
            
    self.dirichlet_samples = [sample_dirichlet(VORONOI_VERTEX_TRIANGLE_SPACING) for i in range(len(particles) ** 2)]
        
        
        
