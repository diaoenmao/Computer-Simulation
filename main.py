from parameters import parameters
import initialize
import draw

rows = initialize.processInput(parameters.blood_vessel_file)
nodes = initialize.buildGraph(rows)
draw.draw_body(nodes)