import forces
import particle
import styles

# Don't change anything in DefaultSettings. Instead, use MySettings (below), or other subclasses. 
# That way, if you don't like your changes the defaults are still available. 
class DefaultSettings:
    """
    A static grid of points. Click to add control nodes. Particles are attracted to control nodes.
    """
    
    # Initial particles. You can change these values; see other settings below for other ways to initialize particles. 
    PARTICLES = particle.grid(x=200, y=200, wt=400, ht=400, rows=4, cols=4, jitter=0)
    
    # Size of window
    WIDTH = 800
    HEIGHT = 800

    # Whether the simulation should run on its own
    LIVE = False
    
    # View options. 
    SHOW_PARTICLES = True
    SHOW_MESH_TRIANGLES = True
    SHOW_VORONOI_SITES = False
    SHOW_VORONOI_SITE_INSETS = False
    SHOW_VORONOI_INSET_BEZIERS = False
    
    # Styling and parameters for view options
    MESH_TRIANGLE_STYLE = styles.grey_lines
    VORONOI_SITE_STYLE = styles.blue_lines
    CONTROL_NODE_SIZE = 15
    CONTROL_NODE_STYLE = styles.magenta_fill
    PARTICLE_SIZE = 10
    PARTICLE_STYLE = styles.dark_grey_fill
    VORONOI_SITE_INSETS = [10, 20, 30]
    VORONOI_SITE_INSET_STYLE = styles.thin_green_lines
    VORONOI_BEZIER_INSET = 10
    VORONOI_INSET_BEZIER_STYLE = styles.thin_yellow_lines
    
    # The particle simulation updates at every step based on forces. Some are unary (operating 
    # on individual nodes) and some are binary (operating on pairs of nodes). 
    UNARY_FORCES= [forces.pull_to_center, forces.friction]
    BINARY_FORCES= [forces.gravity, forces.control_node_aggregation]

    # Gravity causes particles to be drawn together (may be set negative)
    GRAVITY_STRENGTH = 0

    # Pulls particles to the center.
    PULL_TO_CENTER_STRENGTH = 0

    # Aggregation pulls nodes toward control nodes (added by clicking)
    AGGREGATION_STRENGTH = 1
    AGGREGATION_MIDPOINT = 200   
    AGGREGATION_STEEPNESS = 1

    # Friction causes nodes to decelerate. Should be between 0 and 1.
    FRICTION_STRENGTH = 0
    
    SVG_FILENAME = "particles.svg"
    
class SolarSystemSettings(DefaultSettings):
    "Planets orbiting a sun"
    PARTICLES = particle.planets(cx=400, cy=400, rMean=100, rStd=10, n=5, planet_velocity=10)
    GRAVITY_STRENGTH = 100
    LIVE = True
    
class BubblesSettings(DefaultSettings):
    """
    Particles have negative gravity, so they are repelled from one another. 
    Balancing this, there is a constant pull toward the center. Also, there is friction 
    so that particles come to a halt. 
    """
    PARTICLES = particle.gaussian(cx=400, cy=400, std=40, n=20)
    LIVE = True
    GRAVITY_STRENGTH = -1000
    PULL_TO_CENTER_STRENGTH = 0.5
    FRICTION_STRENGTH = 0.2
    SHOW_VORONOI_SITES = True
    SHOW_MESH_TRIANGLES = False
    
class MySettings(DefaultSettings):
    "My custom settings. Over-ride defaults here instead of changing them, so that if you don't like what you did, you can always go back to the defaults."
    # Since this is a subclass of DefaultSettings, all of its properties are inherited unless you declare new values. 
