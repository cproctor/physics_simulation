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
SHOW_VORONOI_BOUNDARIES = False
SHOW_VORONOI_INSETS = False
SHOW_VORONOI_BEZIERS = False
SHOW_VORONOI_VERTEX_TRIANGLES = False
SHOW_VORONOI_VERTEX_BEZIERS = True

# Determines how much the bezier curves should be inset within Voronoi boundaries.
# If you don't want variation, set standard deviation to zero.
VORONOI_BEZIER_INSET_MEAN = 50
VORONOI_BEZIER_INSET_STD = 5

# When drawing voronoi vertex triangles, determines where triangle vertices should fall
# along each voronoi edge. Should be three numbers, used to parametrize a dirichlet 
# distribution. The expected spacing will be proportional to these numbers. So for example
# [1,2,1] would give an expected spacing of triangle vertices 25% of the way along 
# each edge. Scale up the numbers for a more diffuse sample.
# Set USE_RANDOM_VORONOI_VERTEX_TRIANGLE_SPACING to False for deterministic even spacing.
USE_RANDOM_VORONOI_VERTEX_TRIANGLE_SPACING = False
VORONOI_VERTEX_TRIANGLE_SPACING = [10, 10, 10]

# =================================================================================
# Node initialization
# =================================================================================
# Either "grid", "circle", "two_circles", or "random"
INITIAL_NODE_LAYOUT = "random"
# In the particle simulation, particles have point masses that affect their
# momentum and possibly how forces act on them. Choose either "constant" or "random" mass.
NODE_MASS = "constant"
# If INITIAL_NODE_LAYOUT is "grid", NUM_NODES will be rounded to the closest perfect square. 
NUM_NODES = 36
# Only used if initial node layout is "grid". Adds some jitter
# to each node's position so they aren't completely regular.
GRID_JITTER = 5

# =================================================================================
# Forces
# =================================================================================
# The particle simulation updates at every step based on forces. Some are unary (operating 
# on individual nodes) and some are binary (operating on pairs of nodes). 

# Repulsion is like gravity, but in reverse, causing nodes to be pushed away from one another.
REPULSION_STRENGTH = 800

# Pulls nodes to the center. Helpful 
PULL_TO_CENTER_STRENGTH = 0

# Aggregation pulls nodes toward control nodes (added by clicking)
AGGREGATION_STRENGTH = 1
AGGREGATION_MIDPOINT = 200   
AGGREGATION_STEEPNESS = 1

# Friction causes nodes to decelerate. Should be between 0 and 1.
FRICTION_STRENGTH = 0.4
