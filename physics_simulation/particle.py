class Particle:
    def __init__(self, x, y, mass=1.0, control=False, fixed=False):
        self.mass = mass
        self.control = control
        self.fixed = fixed
        self.position = PVector(x, y)
        self.velocity = PVector(0,0)
        self.acceleration = PVector(0,0)
        
    def __repr__(self):
        return "<Particle at ({}, {})>".format(self.position.x, self.position.y)
        
    def dist(self, other):
        "Returns the distance to the other particle"
        return PVector.dist(self.position, other.position)
    
    def apply_force(self, force_vector):
        "Uses F=MA to update acceleration based on force applied."
        self.acceleration += force_vector / self.mass
    
    def step(self):
        "Updates the particle through a moment in time."
        self.velocity += self.acceleration
        if not self.fixed:
            self.position += self.velocity
        self.acceleration = PVector(0,0)
        
    def render(self, s):
        if self.control:
            s.CONTROL_NODE_STYLE()
            ellipse(self.position.x, self.position.y, s.CONTROL_NODE_SIZE, s.CONTROL_NODE_SIZE)
        else:
            s.PARTICLE_STYLE()
            ellipse(self.position.x, self.position.y, s.PARTICLE_SIZE, s.PARTICLE_SIZE)
   
# --------------------------------------------------- 
# Functions for generating initial particle positions
# --------------------------------------------------- 

def gaussian(cx, cy, std, n):
    return [Particle(cx + randomGaussian() * std, cy + randomGaussian() * std) for _ in range(n)]
    
def gaussian_moving(xMean, yMean, posStd, vMean, vStd, n):
    particles = gaussian(xMean, yMean, posStd, count)
    for p in particles: 
        p.velocity = PVector(vMean + randomGaussian() * vStd, 0).rotate(random(TWO_PI))
    return particles

def grid(x, y, wt, ht, rows, cols, jitter=0):
    xSpace = wt/cols
    ySpace = ht/rows
    grid = [Particle(x + i + xSpace/2, y + j + ySpace/2) for i in range(0, wt, xSpace) for j in range(0, ht, ySpace)]
    if jitter:
        for particle in grid:
            particle.position.x += randomGaussian() * jitter
            particle.position.y += randomGaussian() * jitter
    return grid

def ring(c, r, n):
    return [Particle(c.x + r()*cos(float(i)/n * TWO_PI), c.y + r()*sin(float(i)/n * TWO_PI)) for i in range(n)]

def planets(cx, cy, rMean, rStd, n, sun_mass=100, planet_velocity=1):
    sun = Particle(cx, cy, mass=sun_mass)
    planets = ring(sun.position, lambda: rMean + randomGaussian() * rStd, n)
    for p in planets:
        p.velocity.x = -(p.position - sun.position).y
        p.velocity.y = (p.position - sun.position).x
        p.velocity.setMag(planet_velocity)
    return [sun] + planets
