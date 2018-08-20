# Forces are functions which take one or two Nodes (unary or binary) and return a 
# 2-dimensional PVector(x,y) 

from settings import *

from functions import make_sigmoid, make_exponential

def repulsion(n1, n2, sim=None):
    "Causes all nodes to be repelled from each other, like gravity but in reverse."
    v = n1.position - n2.position
    v.setMag(REPULSION_STRENGTH / (n1.position.dist(n2.position) ** 2))
    return v

aggregation_strength = make_sigmoid(AGGREGATION_MIDPOINT, AGGREGATION_STEEPNESS)

def control_node_aggregation(n1, n2, sim=None):
    "Pulls nodes toward control nodes"
    if not n2.control: return PVector(0,0)
    v = n2.position - n1.position
    v.setMag(aggregation_strength(n1.position.dist(n2.position)))
    return v

def pull_to_center(n, sim=None):
    "Pulls all nodes toward the center"
    v = sim.center.position - n.position
    v.setMag(PULL_TO_CENTER_STRENGTH)
    return v

def friction(n1, sim=None):
    v = n.velocity.copy() * -1
    v.setMag(FRICTION_STRENGTH)
    
