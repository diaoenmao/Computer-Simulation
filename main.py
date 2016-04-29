from parameters import *
from oscillator import *
import initialize
import draw
from globals import *
from AbstractBacteriaCellCluster import *
from AbstractHost import *
from heapq import heappush, heappop
from time import sleep
import threading

#dfs
def timestep(o):
	assert(o is not None)
	assert(isinstance(o, AbstractHost))
	children = o.getChildren()
	if children is not None:
		for child in children:
			timestep(child)

def simulate():
	while(True):
		assert(objects[0].id == 1)
		head = objects[0]
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

blood_vessels = initialize.processInput(parameters.blood_vessel_file)
objects = initialize.buildGraph(blood_vessels)

#insert bacteria clusters
for id, cluster in parameters.bacteria_t0.items():
	id = int(id)
	assert(isinstance(cluster, AbstractBacteriaCellCluster))
	objects[id].enterBacteriaCluster(cluster)

for id, cluster in parameters.immune_t0.items():
	id = int(id)
	assert(isinstance(cluster, AbstractImmuneCellCluster))
	objects[id].enterImmuneCellCluster(cluster)

globals.objects = objects

threading.Thread(target=simulate).start()

draw.draw_body(globals.objects)
