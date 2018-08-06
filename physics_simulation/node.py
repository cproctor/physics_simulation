class Node:
    def __init__(self, x, y, size=1, control=False, fixed=False):
        self.x = x
        self.y = y
        self.size = size
        self.control = control
        self.fixed = fixed
        self.neighors = []
        
    def distance(self, other_node):
        return sqrt((other_node.x - self.x) ** 2 + (other_node.y - self.y) ** 2)
    
    def vector_to(self, other_node, length=1):
        vector_length = self.distance(other_node)
        unit_vector = [(other_node.x - self.x)/vector_length, (other_node.y - self.y)/vector_length]
        return [sqrt(length) * i for i in unit_vector]
    
# Generating functions
def random_nodes(wt, ht, count):
    return [Node(random(wt), random(ht), 1) for i in range(count)]

def node_grid(wt, ht, rows, cols, jitter=0):
    xSpace = wt/cols
    ySpace = ht/rows
    grid = [Node(i + xSpace/2, j + ySpace/2) for i in range(0, wt, xSpace) for j in range(0, ht, ySpace)]
    if jitter:
        for node in grid:
            node.x += randomGaussian() * jitter
            node.y += randomGaussian() * jitter
    return grid
