import pyvista as pv

# Tube dimensions
inner_diameter = 0.021
outer_diameter = 0.026
height = 0.1

# Create the outer cylinder
outer_cylinder = pv.Cylinder(radius=outer_diameter/2, height=height, resolution=100).triangulate()

# Create the inner cylinder
inner_cylinder = pv.Cylinder(radius=inner_diameter/2, height=height, resolution=100).triangulate()

# Create the tube by subtracting the inner cylinder from the outer cylinder
tube = outer_cylinder - inner_cylinder

# Plot the tube
p = pv.Plotter()
p.add_mesh(tube, color='blue')

# Adjust the lighting
p.lighting = True  # Enable lighting
p.ambient_intensity = 0.5  # Adjust ambient light intensity
p.specular_intensity = 0.6  # Adjust specular light intensity

# Adjust the camera position
p.camera_position = [(1.5, -1.5, 1.5), (0, 0, 0), (0, 0, 1)]  # Set camera position as (x, y, z) coordinates

p.show()