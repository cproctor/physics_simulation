# In this sketch, each point exerts forces on its neighbors. 
# This allows local structure, such as a consistent spacing between points. 

from forces import *
from node import Node, random_nodes, node_grid
from simulation import Simulation
from settings import *

nodes = node_grid(350, 350, 100, 100, 5, 5, jitter=2)
for node in nodes:
    node.mass = randomGaussian() * 10

sim = Simulation(
    wt=WIDTH, 
    ht=HEIGHT, 
    #nodes = node_grid(0, 0, WIDTH, HEIGHT, 5, 5, jitter=0),
    nodes = nodes,
    unary_forces=[
        pull_to_center
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
    for node in sim.nodes:
        node.draw()
        
        if node.control:
            fill(0,0,255)
            ellipse(node.position.x, node.position.y, 10, 10)
        else:
            fill(255)
            ellipse(node.position.x, node.position.y, 5, 5)
            #ellipse(node.x, node.y, node.size, node.size)

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
    if key == 'v':
        sim.drawVoronoi()
    
def keyReleased():
    if key == ' ':
        global LIVE
        LIVE = False
        
def add_attractor(x, y):  
    attractor = Node(x, y, control=True, fixed=True)
    sim.nodes.append(attractor)  
    
def increase_mass(x, y):
    click = Node(x, y)
    for node in sim.nodes:
        if node.distance(click) < CLICK_RADIUS:
            node.mass += 0.1
