# Size of window
WIDTH = 800
HEIGHT = 800
# When LIVE, the simulation will start in a running state. 
# Use the space bar to control live state: once you press space bar,
# the simulation will only run while it is pressed. 
LIVE = True
# Press 's' to save a CSV file of node positions to this file. 
CSV_FILE = "simulation.csv"
SHOW_RECTANGLE = True
SHOW_VORONOI_BOUNDARIES = True
SHOW_VORONOI_INSETS = True
SHOW_VORONOI_BEZIERS = True
# Determines how much the bezier curves should be inset within Voronoi boundaries.
VORONOI_BEZIER_INSET = 20

# =================================================================================
# Node initialization
# =================================================================================
# Either "grid", "circle", "two_circles", or "random"
INITIAL_NODE_LAYOUT = "grid"
# In the particle simulation, particles have point masses that affect their
# momentum and possibly how forces act on them. Choose either "constant" or "random" mass.
NODE_MASS = "constant"
# If INITIAL_NODE_LAYOUT is "grid", NUM_NODES will be rounded to the closest perfect square. 
NUM_NODES = 25
# Only used if initial node layout is "grid". Adds some jitter
# to each node's position so they aren't completely regular.
GRID_JITTER = 0

# =================================================================================
# Forces
# =================================================================================
# The particle simulation updates at every step based on forces. Some are unary (operating 
# on individual nodes) and some are binary (operating on pairs of nodes). 

# Repulsion is like gravity, but in reverse, causing nodes to be pushed away from one another.
REPULSION_STRENGTH = 1000

# Pulls nodes to the center. Helpful 
PULL_TO_CENTER_STRENGTH = 0

# Aggregation pulls nodes toward control nodes (added by clicking)
AGGREGATION_STRENGTH = 1
AGGREGATION_MIDPOINT = 200   
AGGREGATION_STEEPNESS = 1

# Friction causes nodes to decelerate. Should be between 0 and 1.
FRICTION_STRENGTH = 0.2
