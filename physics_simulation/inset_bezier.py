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
    
def edges(points):
    "Returns pairs of points forming edges"
    return tuples(points + [points[0]], 2)

def corners(points):
    "Returns triplets of points about each corner"
    return tuples([points[-1]] + points + [points[0]], 3)
        
def midpoint(p1, p2, inset=0):
    "Finds midpoint of two points, possibly with an inset."
    mp = (p1 + p2) / 2
    vec = p2 - p1
    insetVec = PVector(vec.y, -vec.x)
    insetVec.setMag(inset)
    return mp + insetVec

def insetVertices(points, inset):
    "returns vertices of the shape inset by a certain amount"
    result = []
    for a, b, c in corners(points):
        v = (b-a).setMag(1) + (b-c).setMag(1)
        v.setMag(inset)
        result.append(b-v)
    return result
        

def drawInsetBezier(points):
    midpoints = [midpoint(a, b) for a, b in edges(insetPts)]
    bzPts = iter(zip(midpoints, insetPts))
    beginShape()
    v0, cp0 = next(bzPts)
    vertex(v0.x, v0.y)
    for v, cp in bzPts:
        bezierVertex(cp.x, cp.y, cp.x, cp.y, v.x, v.y)
    bezierVertex(cp0.x, cp0.y, cp0.x, cp0.y, v0.x, v0.y)
    endShape()
    
def drawShape(points):
    beginShape()
    for v in points + [points[0]]:
        vertex(v.x, v.y)
    endShape()
