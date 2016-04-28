from parameters import parameters
import initialize
import draw

blood_vessels = initialize.processInput(parameters.blood_vessel_file)
nodes = initialize.buildGraph(blood_vessels)
draw.draw_body(nodes)