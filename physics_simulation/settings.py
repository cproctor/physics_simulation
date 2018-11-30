# Size of window
WIDTH = 800
HEIGHT = 800

# Initial node layout
# Either "grid" or "random"
INITIAL_NODE_LAYOUT = "grid"

# In the particle simulation, particles have point masses that affect their
# momentum and gravitational attraction. Choose either "constant" or "random"
NODE_MASS = "random"

# If INITIAL_NODE_LAYOUT is "grid", will round to the closest perfect square. 
NUM_NODES = 49

# Only used if initial node layout is "grid". Adds some jitter
# to each node's position so they aren't completely regular.
GRID_JITTER = 2

# When LIVE, the simulation will start in a running state. 
# Use the space bar to control live state: once you press space bar,
# the simulation will only run while it is pressed. 
LIVE = True

# Press 's' to save a CSV file of node positions to this file. 
CSV_FILE = "simulation.csv"

REPULSION_STRENGTH = 10
PULL_TO_CENTER_STRENGTH = 0

AGGREGATION_MIDPOINT = 200   
AGGREGATION_STEEPNESS = 1

FRICTION_STRENGTH = 10

SHOW_RECTANGLE = True
SHOW_VORONOI_BOUNDARIES = True
SHOW_VORONOI_BEZIERS = False
VORONOI_BEZIER_INSET = 5
