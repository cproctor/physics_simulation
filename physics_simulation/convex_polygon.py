from ray import Ray

def tuples(iterable, n):
    """
    Returns an overlapping iterator containing tuples:
    tuples([1,2,3,4,5], 3) -> [(1,2,3), (2,3,4), (3,4,5)]
    """
    it = iter(iterable)
    try:
        ngram = [next(it) for _ in range(n)]
        while True: 
            yield tuple(ngram)
            ngram = ngram[1:] + [next(it)]
    except StopIteration:
        return
    
def near(v0, v1, eta=0.00001):
    return PVector.dist(v0, v1) < eta

class ConvexPolygon:
    def __init__(self, points):
        if len(points) < 3: raise self.TooFewPoints("Cannot create a polygon with {}".format(points))
        self.points = points
        
    def edges(self):
        "Pairs of points forming edges"
        return tuples(self.points + [self.points[0]], 2)
    
    def midpoints(self):
        return [(a+b)/2 for a, b in self.edges()]
    
    def corners(self):
        "Triplets of points about each corner"
        return tuples([self.points[-1]] + self.points + [self.points[0]], 3)
    
    def inset(self, i, depth=0):
        "Bumps all edges in by i"
        print("In inset with depth {}".format(depth))
        if i == 0: return self
        bisectors = self.bisector_rays(i)
        bisectorPairs = tuples(bisectors + [bisectors[0]], 2)
        angles = self.corner_angles()
        anglePairs = tuples(angles + [angles[0]], 2)
        edgeEventInsets = []

        for (a, b), (angA, angB) in zip(bisectorPairs, anglePairs):
            try:
                x = Ray.intersection(a, b)
                intersectionInsetA = PVector.dist(a.pos, x) * sin(angA/2)
                intersectionInsetB = PVector.dist(b.pos, x) * sin(angB/2)
                dst = min(intersectionInsetA, intersectionInsetB)
                edgeEventInsets.append(dst if dst < i else None)
            except Ray.HasNoIntersection:
                edgeEventInsets.append(None)
        if any(edgeEventInsets):            
            minDist = min(d for d in edgeEventInsets if d)
            insets = self.bisector_rays(minDist)
            pts = [a.dest for a, b in tuples(insets + [insets[0]], 2) if not near(a.dest, b.dest)]
            if depth > self.MAX_INSET_DEPTH:
                raise self.NoInset
            return ConvexPolygon(pts).inset(i - minDist, depth=depth+1)
        else:
            pts = [b.dest for b in bisectors]
            return ConvexPolygon(pts)
    
    def bisector_rays(self, rayLen):
        "Returns rays bisecting each corner"
        rays = []
        for a, b, c in self.corners():
            angle = PVector.angleBetween(b-a, b-c)
            bisector = (a-b).setMag(1) + (c-b).setMag(1)
            bisector.setMag(rayLen/sin(angle/2))
            rays.append(Ray(b, bisector))
        return rays
    
    def corner_angles(self):
        return [PVector.angleBetween(b-a, b-c) for a, b, c in self.corners()]
    
    def draw(self):
        beginShape()
        for v in self.points + [self.points[0]]:
            vertex(v.x, v.y)
        endShape()
                
    def drawBezier(self):
        bzPts = iter(zip(self.midpoints(), self.points))
        beginShape()
        v0, cp0 = next(bzPts)
        vertex(v0.x, v0.y)
        for v, cp in bzPts:
            bezierVertex(cp.x, cp.y, cp.x, cp.y, v.x, v.y)
        bezierVertex(cp0.x, cp0.y, cp0.x, cp0.y, v0.x, v0.y)
        endShape()
    
    MAX_INSET_DEPTH = 5
    class TooFewPoints(Exception): pass
    class NoInset(Exception): pass
