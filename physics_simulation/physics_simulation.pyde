# In this sketch, each point exerts forces on its neighbors. 
# This allows local structure, such as a consistent spacing between points. 

from forces import *
from node import Node, random_nodes, node_grid, node_circle
from simulation import Simulation
from math import sqrt
from settings import *

if INITIAL_NODE_LAYOUT == 'random':
    nodes = random_nodes(WIDTH, HEIGHT, NUM_NODES)
elif INITIAL_NODE_LAYOUT == 'grid':
    gridSize = int(sqrt(NUM_NODES))
    nodes = node_grid(350, 350, 100, 100, gridSize, gridSize, jitter=2)
elif INITIAL_NODE_LAYOUT == 'circle':
    nodes = node_circle(PVector(WIDTH/2, HEIGHT/2), (WIDTH+HEIGHT)/8, NUM_NODES)
elif INITIAL_NODE_LAYOUT == 'two_circles':
    nodes = (node_circle(PVector(WIDTH/2, HEIGHT/2), (WIDTH+HEIGHT)/16, NUM_NODES/2) + 
             node_circle(PVector(WIDTH/2, HEIGHT/2), (WIDTH+HEIGHT)/8, NUM_NODES/2))
else:
    raise ValueError("Invalid value for INITIAL_NODE_LAYOUT")

if NODE_MASS == "random":
    for node in nodes:
        node.mass = randomGaussian() * 10
    
sim = Simulation(
    wt=WIDTH, 
    ht=HEIGHT, 
    nodes = nodes,
    unary_forces=[
        pull_to_center, 
        friction
    ],
    binary_forces=[
        repulsion,
        control_node_aggregation,
    ], 
)

def setup():
    size(WIDTH, HEIGHT)
    background(0)
    noStroke()
    for node in sim.nodes:
        node.draw()
    sim.drawVoronoi()
    sim.label_nodes()
    
def draw():
    background(1)
    noStroke()
    if SHOW_NODES:
        for node in sim.nodes:
            node.draw()
    if SHOW_RECTANGLE:
        sim.drawRectangle()
    sim.drawVoronoi()
    if LIVE:
        sim.step()
    
def mouseClicked():
    add_attractor(mouseX, mouseY)
    
def keyPressed():
    if key == ' ':
        global LIVE
        LIVE = True
    if key == 's':
        sim.export_csv(CSV_FILE)
    
def keyReleased():
    if key == ' ':
        global LIVE
        LIVE = False
        
def add_attractor(x, y):  
    attractor = Node(x, y, control=True, fixed=True)
    # Prevent nodes on top of each other (zero-division error)
    for node in sim.nodes: 
        if node.position.dist(attractor.position) < 0.01:
            return
    sim.nodes.append(attractor)  
