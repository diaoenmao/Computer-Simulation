from parameters import *
from oscillator import *
import initialize
import draw
from globals import *
from AbstractBacteriaCellCluster import *
from heapq import heappush, heappop

#dfs
def timestep(o):
	assert(o is not None)
	assert(isinstance(o, AbstractHost))
	children = o.getChildren()
	for child in children:
		timestep(child)


blood_vessels = initialize.processInput(parameters.blood_vessel_file)
objects = initialize.buildGraph(blood_vessels)

"""
draw.draw_body(nodes)
"""

#insert bacteria clusters
for id, cluster in parameters.bacteria_t0.items():
	id = int(id)
	assert(isinstance(cluster, AbstractBacteriaCellCluster))
	objects[id].enterBacteriaCluster(cluster)

for id, cluster in parameters.immune_t0.items():
	id = int(id)
	assert(isinstance(cluster, AbstractImmuneCellCluster))
	objects[id].enterImmuneCellCluster(cluster)


while(True):
	assert(nodes[0].id == 1)
	head = nodes[0]
	initialVelocity = oscillator.getVelocity()
	#Get bacteria,
	while len(globals.terminalOutputEvent) > 0 and globals.terminalOutputEvent[0][0] <= globals.time:
		(time, cluster) = heappop(self.terminalOutputEvent)
		assert(isinstance(cluster, AbstractCellCluster))
		if isinstance(cluster, AbstractBacteriaCellCluster):
			head.enterBacteriaCluster(cluster)
		elif isinstance(cluster, AbstractImmuneCellCluster):
			head.enterImmuneCellCluster(cluster)
	
	flow = oscillator.getVolume()
	actualFlow = head.setFlow(flow)
	oscillator.setlastVolume(actualFlow)
	timestep(head)
	globals.time += 1