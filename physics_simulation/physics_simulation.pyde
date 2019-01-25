add_library('svg')
from controls import KeyControls
from simulation import Simulation
from mesh import Mesh
import settings
import particle
import forces
import styles

# =================================================================
# INSTRUCTIONS
# - This is a pretty complex simulation, but it's entirely controlled
#   by a collection of settings. 
# - There are several predefined different collections of settings
#   below. Uncomment the one you want to use. 
# - You can also define your own settings. See 'settings.py'.
#   
s = settings.DefaultSettings()
# s = settings.SolarSystemSettings()
# s = settings.BubblesSettings()
# s = settings.MySettings()
# =================================================================

sim = Simulation(s)
mesh = Mesh(sim.positions(), s)

def setup():
    size(s.WIDTH, s.HEIGHT)
    background(0)
    mesh.render()
    sim.render()
    
def draw():
    global mesh
    background(1)
    mesh.render()
    sim.render()
    if s.LIVE:
        sim.step()
        mesh = Mesh(sim.positions(), s)
       
# ----------------------------------------------------------------------
# The rest is just defining the controls: binding key-presses to actions
# ----------------------------------------------------------------------
 
def run():
    s.LIVE = True
def pause():
    s.LIVE = False
def toggle_particles():
    s.SHOW_PARTICLES = not s.SHOW_PARTICLES
def toggle_mesh_triangles():
    s.SHOW_MESH_TRIANGLES = not s.SHOW_MESH_TRIANGLES
def toggle_voronoi_sites():
    s.SHOW_VORONOI_SITES = not s.SHOW_VORONOI_SITES
def toggle_voronoi_site_insets():
    s.SHOW_VORONOI_SITE_INSETS = not s.SHOW_VORONOI_SITE_INSETS
def toggle_voronoi_inset_beziers():
    s.SHOW_VORONOI_INSET_BEZIERS = not s.SHOW_VORONOI_INSET_BEZIERS
def save_to_svg():
    beginRecord(SVG, s.SVG_FILENAME);
    mesh.render()
    sim.render()
    endRecord()
    print("Saved current view to {}".format(s.SVG_FILENAME))

controls = KeyControls(s.__doc__.strip())
controls.bind_press(' ', "run the simulation", run)
controls.bind_release(' ', "pause the simulation", pause)
controls.bind_press('p', "Show/hide particles", toggle_particles)
controls.bind_press('t', "Show/hide mesh triangles", toggle_mesh_triangles)
controls.bind_press('v', "Show/hide voronoi sites", toggle_voronoi_sites)
controls.bind_press('i', "Show/hide voronoi insets", toggle_voronoi_site_insets)
controls.bind_press('b', "Show/hide voronoi beziers", toggle_voronoi_inset_beziers)
controls.bind_press('s', "Save current view to SVG", save_to_svg)
controls.show_help()
    
def mouseClicked():
    global mesh
    sim.add_control_node(mouseX, mouseY)
    mesh = Mesh(sim.positions(), s)
    mesh.render()
    sim.render()
    
def keyPressed():
    controls.handle_press()
    
def keyReleased():
    controls.handle_release()
