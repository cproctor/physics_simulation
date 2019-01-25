# Physics Simulation

![Insets](https://raw.githubusercontent.com/cproctor/physics_simulation/master/insets.png)
![Beziers](https://raw.githubusercontent.com/cproctor/physics_simulation/master/beziers.png)

This Processing project overlays two different phenomena:

- First, it's a physics simulation. Particles are subjected to forces, and time moves
  forward one step at a time (the 'tick model'). For example, using `SolarSystemSettings`, 
  you can create a realistic simulation of a solar system (though collisions are not modeled).
  However, forces can be arbitrarily defined, and don't have to match physical reality. For example, 
  using `BubblesSettings`, particles repel one another but are all pulled toward the center. 
- Second, particle positions are used as the basis of a mesh supporting some neat tools from 
  computational geometry. The mesh can be 
  [triangulated](https://en.wikipedia.org/wiki/Delaunay_triangulation), and 
  a [Voronoi diagram](https://en.wikipedia.org/wiki/Voronoi_diagram) can be generated.
  [Inset polygons](https://en.wikipedia.org/wiki/Straight_skeleton) can be created, and a 
  [Bezier curve](https://en.wikipedia.org/wiki/B%C3%A9zier_curve) can be fitted to the inset polygon. 

What's the point? First, it's fun to play with and can function as a microworld for exploring various
dynamics. Second, it's potentially a useful tool for generating organic forms for use in digital 
fabrication processes. 

## Installation

You'll need [Processing3](https://processing.org/download/) and its [Python mode](https://github.com/jdf/processing.py#python-mode-for-processing). 
Assuming you're reading this from the [GitHub repository](https://github.com/cproctor/physics_simulation), 
click the green "Clone or Download" button above, and download a zip file. Unzip it, drag 
the `physics_simulation` folder into your main `processing` folder, and you should be ready to open 
the simulation in Processing. 

## Usage

There are several ways to interact with the simulation. 
- First, you can choose which settings to use. In the main `physics_simulation` file, 
  simply uncomment one of the lines selecting different bundles of settings. 
- While the simulation is running, you can click anywhere to add control nodes. Depending
  on the settings you're using, these will have different effects. 
- There are various key commands you can use. The options should be printed to the console
  when you run the simulation. 
- You can also define your own settings in `settings.py`. `DefaultSettings` provides default values
  for every setting, and explains what they do. You could just change values in 
  `DefaultSettings` directly, but it's a better idea to use `MySettings` (scroll to the bottom of the file)
  to override values, so that the defaults are still there in case you want to go back to them. 

If you run the simulation and nothing happens, there are two possibilities:
- Maybe `LIVE` is set to `False` in your current settings. Try pressing the space bar to run the simulation. 
- Maybe there are no forces acting on the nodes. Try clicking somewhere to add a control node. 
