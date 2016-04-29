class Parameter:
    pass

#Follow base SI units: meter, kg, s

parameters = Parameter()

#import file
parameters.body_mesh_file = '/data/body_mesh.obj'
parameters.blood_vessel_file = '/data/data.csv'

#Visualization parameters
parameters.visualization_factor = 13
parameters.refresh_interval = 1#s

#Simulation parameters
parameters.blood_density = 1.05e3 #kg/m^3
parameters.viscosity = 0.004 #Pa * s 
parameters.wall_viscoelasticity = 15 #degree
parameters.poission_ratio = 0.5 
parameters.bpm = 60
parameters.stroke_volume = 94e-6
parameters.qrs_interval = 0.1 #s
parameters.ejection_velocity = 0.4 #m/s
parameters.sink_velocity = 3e-4 #m/s
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
parameters.bacteria_reproduction_rate = 5e-5 #1/s

#initial bacteria infestation
parameters.bacteria_t0 = {} #id: cluster 
parameters.immune_t0 = {} #id: cluster