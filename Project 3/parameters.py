<<<<<<< HEAD
import math
DEBUG = 1
PARKING_NODE_COLOR = '#FF0099'
EXIT_NODE_COLOR = 'r'
STREET_NODE_COLOR = 'g'
COP_NODE_COLOR = '#3c3ccc'
VISUAL = 1
COP_MODE = 0
COP_INTERSECTION_THRESHOLD = 0
COP_CONGESTION_THRESHOLD = 0.5
COP_EVACUATION_THRESHOLD = 0
DEPTH_OF_AWARENESS = 1
EAST_TENDENCY = 0
SPACE_TIME_TRADEOFF = 1
DEAD_END = []
IF_MUTATE = 0
#Simulation parameter
UNIT_LENGTH = math.ceil(5000/738)   #ft
AVERAGE_CAR_SPACE_LENGTH = 20 #ft
AVERAGE_CAR_SPEED = 37 #ft/s

=======
import TestBacteriaCellCluster as t
class Parameter:
    pass

#Follow base SI units: meter, kg, s

parameters = Parameter()

#debug
parameters.verbose = True

#import file
parameters.body_mesh_file = '/data/body_mesh.obj'
parameters.blood_vessel_file = '/data/data.csv'
parameters.organ_file = '/data/organ.csv'

#Visualization parameters
parameters.visualization_factor = 13
parameters.refresh_interval = 25#s
parameters.color_gradient = "FF0000,FE0400,FE0800,FD0C00,FD1000,\
FD1400,FC1800,FC1C00,FC2000,FB2400,FB2800,FA2C00,FA3000,FA3400,\
F93800,F93C00,F94000 F94000,F84400,F84800,F84C00,F75000,F75500,\
F65900,F65D00,F66100,F56500,F56900,F56D00,F47100,F47500,F47900,\
F37D00,F38100,F28500,F28900,F28D00,F19100,F19500,F19900,F09D00,\
F0A100,F0A500,EFAA00,EFAE00,EEB200,EEB600,EEBA00,EDBE00,EDC200,\
EDC600,ECCA00,ECCE00,ECD200,EBD600,EBDA00,EADE00,EAE200,EAE600,\
E9EA00,E9EE00,E9F200,E8F600,E8FA00,E8FF00"
parameters.cell_count_color_mapping = 1e8
parameters.cell_count_history_interval = 1 #collect cell count every x time intervals
parameters.flow_history_interval = 1

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
parameters.sink_travel_time = 10 #? time intervals
parameters.vein_travel_time = 20 #? time intervals

parameters.bacteria_colony_max_cells = 1e9
parameters.bacteria_colony_max_radius = 0.01 #m
parameters.bacteria_colony_depth = 0.001 #m
parameters.organ_grid_resolution = 1e-3 #m

#Time parameters
parameters.delta_t = 0.5#s
parameters.bacteria_lifespan = 36000 #s
parameters.bacteria_reproduction_rate = 5e-5 #1/s

#initial bacteria infestation
parameters.bacteria_t0 = {
	"10": t.TestBacteriaCellCluster(100),
	"11": t.TestBacteriaCellCluster(10000000),
	"12": t.TestBacteriaCellCluster(100000000000),
	"13": t.TestBacteriaCellCluster(1000000000),
	"14": t.TestBacteriaCellCluster(10000),
	"15": t.TestBacteriaCellCluster(1000),
	"16": t.TestBacteriaCellCluster(1000)
} #id: cluster 
parameters.immune_t0 = {} #id: cluster
>>>>>>> d5868687bcab3127bf957151560d7b04efce1d46
