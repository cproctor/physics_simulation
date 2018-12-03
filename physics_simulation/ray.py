class Ray:
    "A representation of a position and direction"
    def __init__(self, pos, dir):
        self.pos = pos
        self.dir = dir
        self.dest = pos + dir
        try:
            self.slope = self.dir.y / self.dir.x
            self.intercept = self.pos.y - self.slope * self.pos.x
        except ZeroDivisionError:
            self.slope = None
            self.intercept = None
        
    def __repr__(self):
        return "<Ray pos=({},{}) dir=({}, {})>".format(self.pos.x, self.pos.y, self.dir.x, self.dir.y)
        
    def slide(self, param):
        return Ray(self.pos + self.dir * param, self.dir)
    
    def draw(self):
        line(self.pos.x, self.pos.y, self.dest.x, self.dest.y)
        ellipse(self.pos.x, self.pos.y, 5, 5)
        
    @classmethod
    def intersection(cls, a, b):
        if (a.slope == b.slope): 
            raise Ray.HasNoIntersection("Rays {} and {} are parallel.".format(a, b))
        elif a.slope is None:
            x = a.pos.x
            y = b.slope * x + b.intercept
        elif b.slope is None:
            x = b.pos.x
            y = a.slope * x + a.intercept
        else:    
            x = (b.intercept - a.intercept) / (a.slope - b.slope)
            y = a.slope * x + a.intercept
        return PVector(x, y)

    class HasNoIntersection(Exception):
        pass
