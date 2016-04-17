class Parameter:
    pass

parameters = Parameter()

#import file
parameters.body_mesh_file = '/data/body_mesh.obj'
parameters.blood_vessel_file = '/data/data.csv'

#Visualization parameters
parameters.visualization_factor = 13

#Simulation parameters
parameters.blood_density = 1.05 #g/cm^3
parameters.viscosity = 0.04 #poise
parameters.wall_viscoelasticity = 15 #degree
parameters.poission_ratio = 0.5 
parameters.nominal_reflection_coefficient = 0.8
parameters.artery_terminal_time = 1 #?

parameters.bacteria_colony_max_cells = 10**9
parameters.bacteria_death_rate = None
