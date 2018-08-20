class Node:
    def __init__(self, x, y, mass=1, control=False, fixed=False):
        self.mass = mass
        self.control = control
        self.fixed = fixed
        self.position = PVector(x, y)
        self.velocity = PVector(0,0)
        self.acceleration = PVector(0,0)
    
    def apply_force(self, force_vector):
        "Uses F=MA to update acceleration based on force applied."
        self.acceleration += force_vector / self.mass
    
    def step(self):
        "Updates the node through a moment in time."
        self.velocity += self.acceleration
        if not self.fixed:
            self.position += self.velocity
        self.acceleration = PVector(0,0)
        
    def draw(self):
        if self.control:
            fill(0,0,255)
            ellipse(self.position.x, self.position.y, 10, 10)
        else:
            fill(255)
            ellipse(self.position.x, self.position.y, 5, 5)
            #ellipse(node.x, node.y, node.size, node.size)
        
    
# Generating functions
def random_nodes(wt, ht, count):
    return [Node(random(wt), random(ht), 1) for i in range(count)]

def node_grid(x, y, wt, ht, rows, cols, jitter=0):
    xSpace = wt/cols
    ySpace = ht/rows
    grid = [Node(x + i + xSpace/2, y + j + ySpace/2) for i in range(0, wt, xSpace) for j in range(0, ht, ySpace)]
    if jitter:
        for node in grid:
            node.position.x += randomGaussian() * jitter
            node.position.y += randomGaussian() * jitter
    return grid
