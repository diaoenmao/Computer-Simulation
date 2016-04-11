from parameters import parameters
import initialize
import draw

rows = initialize.processInput(parameters.blood_vessel_file)
nodes = initialize.buildGraph(rows)
print(nodes)
draw.draw_body(nodes)