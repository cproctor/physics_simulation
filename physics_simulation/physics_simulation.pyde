# In this sketch, each point exerts forces on its neighbors. 
# This allows local structure, such as a consistent spacing between points. 

from forces import repulsion, pull_to_center, aggregation, personal_space, change_size
from node import Node, random_nodes, node_grid
from simulation import Simulation

WIDTH = 800
HEIGHT = 800
NUM_NODES = 300
CLICK_RADIUS = 50
LIVE = False
CSV_FILE = "simulation.csv"

sim = Simulation(
    wt=WIDTH, 
    ht=HEIGHT, 
    nodes = node_grid(WIDTH, HEIGHT, 15, 15, jitter=20),
    unary_forces=[[pull_to_center, 0]],
    binary_forces=[
        #[repulsion, 0.1],
        [aggregation, 1],
        [personal_space, 3],
        [change_size, 20]
    ], 
)

def setup():
    size(WIDTH, HEIGHT)
    noStroke()
    
def draw():
    background(1)
    noStroke()
    for node in sim.nodes:
        if node.control:
            fill(0,0,255)
            ellipse(node.x, node.y, 10, 10)
        else:
            fill(255)
            ellipse(node.x, node.y, node.size, node.size)
    noFill()
    stroke(255)
    rect(WIDTH/4, HEIGHT/4, WIDTH/2, HEIGHT/2)
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
    sim.nodes.append(attractor)  
    
def increase_mass(x, y):
    click = Node(x, y)
    for node in sim.nodes:
        if node.distance(click) < CLICK_RADIUS:
            node.mass += 0.1
