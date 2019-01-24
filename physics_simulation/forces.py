# Forces are functions which take one or two Nodes (unary or binary) and return a 
# 2-dimensional PVector(x,y) 

from functions import make_sigmoid, make_exponential

def gravity(n1, n2, s, sim=None):
    "Causes all nodes to be repelled from each other, like gravity but in reverse."
    v = n2.position - n1.position
    v.setMag(s.GRAVITY_STRENGTH * n1.mass * n2.mass / (n1.position.dist(n2.position) ** 2))
    return v

def control_node_aggregation(n1, n2, s, sim=None):
    "Pulls nodes toward control nodes"
    if not n2.control: return PVector(0,0)
    v = n2.position - n1.position
    sig = make_sigmoid(s.AGGREGATION_MIDPOINT, s.AGGREGATION_STEEPNESS)
    v.setMag(s.AGGREGATION_STRENGTH * sig(n1.position.dist(n2.position)))
    return v

def pull_to_center(n, s, sim=None):
    "Pulls all nodes toward the center"
    v = sim.center.position - n.position
    v.setMag(s.PULL_TO_CENTER_STRENGTH)
    return v

def friction(n, s, sim=None):
    v = n.velocity * -1.0
    v.setMag(s.FRICTION_STRENGTH * v.mag())
    return v
