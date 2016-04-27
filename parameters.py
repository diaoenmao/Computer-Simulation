class Parameter:
    pass

#Follow base SI units: meter, kg, s

parameters = Parameter()

#import file
parameters.body_mesh_file = '/data/body_mesh.obj'
parameters.blood_vessel_file = '/data/data.csv'

#Visualization parameters
parameters.visualization_factor = 13

#Simulation parameters
parameters.blood_density = 1.05e3 #kg/m^3
parameters.viscosity = 0.04 #poise
parameters.wall_viscoelasticity = 15 #degree
parameters.poission_ratio = 0.5 
parameters.nominal_reflection_coefficient = 0.8
parameters.sink_travel_time = 10 #? s
parameters.vein_travel_time = 20 #? s

parameters.bacteria_colony_max_cells = 1e9
parameters.bacteria_colony_max_radius = 0.01 #m
parameters.bacteria_colony_depth = 0.001 #m
parameters.organ_grid_resolution = 1e-4 #m

#Time parameters
parameters.delta_t = 1 #s
parameters.bacteria_lifespan = 3600 #s
parameters.bacteria_reproduction_rate = 5e-5