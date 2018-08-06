# Forces are functions which takes two Nodes and returns a (x,y)
# position update caused by the force. 

FORCE_MAX = 10
PERSONAL_SPACE = 20
AGGREGATION_MIDPOINT = 500
AGGREGATION_STEEPNESS = 0.5
SIZE_MIDPOINT = 0
SIZE_STEEPNESS = 0.01

from functions import make_sigmoid, make_exponential

def repulsion(n1, n2, strength=1, sim=None):
    "Causes all nodes to be repelled from each other, like gravity but in reverse."
    distance = min((strength * n1.size * n1.size) / (n1.distance(n2) ** 2), FORCE_MAX)
    return [i for i in n2.vector_to(n1, length=distance)]

aggregation_strength = make_sigmoid(AGGREGATION_MIDPOINT, AGGREGATION_STEEPNESS)

def aggregation(n1, n2, strength=1, sim=None):
    "Applies gravity for control nodes"
    if not n2.control: 
        return [0,0]
    else:
        return n1.vector_to(n2, length=aggregation_strength(n1.distance(n2)))
    
def personal_space(n1, n2, strength=1, sim=None):
    "Enforces "
    if n1.distance(n2) < n1.size + n2.size + PERSONAL_SPACE:
        return n2.vector_to(n1, length=strength * n1.size)
    else:
        return [0,0]
    
def pull_to_center(n1, strength=1, sim=None):
    "Pulls nodes toward the center"
    return [strength * i for i in n1.vector_to(sim.center, length=1)]

node_size = make_sigmoid(SIZE_MIDPOINT, SIZE_STEEPNESS)

def change_size(n1, n2, strength=1, sim=None):
    "A fake force which causes the size of nodes to change"
    if n2.control:
        n1.size = max(n1.size, strength * node_size(n1.distance(n2)))
    return [0,0]
    
