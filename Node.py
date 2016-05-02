from Point import *
from Organ import Organ
from AbstractHost import *
from AbstractBacteriaCellCluster import *
from AbstractImmuneCellCluster import *
from GenericSink import *
from parameters import * 
from globals import globals
import math
import numpy as np

class Node(AbstractHost):

    def __init__(self, name, id, length, radius, wall_thickness, youngs_modulus, f0, _from, _to, yaw, pitch, p1, p2):
        assert(isinstance(p1, Point))
        assert(isinstance(p2, Point))
        self.name = name
        self.id = id
        self.length = float(length) / 100
        self.radius = float(radius) / 100
        self.wall_thickness = wall_thickness / 100
        self.youngs_modulus = float(youngs_modulus) * 1e5 #pascal
        self.f0 = float(f0)
        self._from = _from
        self._to = _to
        self.start = p1
        self.end = p2
        self.yaw = yaw
        self.pitch = pitch
        self.immuneCellClusters = []
        self.bacteriaClusters = []
        self.edges = []
        self._resistance = (8 * self.length * parameters.viscosity) / (math.pi * (self.radius) ** 4 )
        self._sinks = []
        if  self._to == [0]:
            self.setTail(True)
        else:
            self.setTail(False)
        if self.id == 1: #ascending aorta
            self._velocity = parameters.ejection_velocity
        else:
            self._velocity = 0
        self.volume = self.radius ** 2 * math.pi * self.length
        self.residualVolume = 0
        self.parent = None
        self.bacteriaCountHistory = []

    def getCellCountHistory(self):
        return self.bacteriaCountHistory

    def setTail(self, isTail):
        self._tail = isTail
        if self._tail and len(self._sinks) == 0:
            genericSink = GenericSink("Sink for Node id: " + str(self.id) + ", " + self.name, None)
            cNaught = (self.youngs_modulus * self.wall_thickness / (2 * parameters.blood_density * self.radius)) ** 0.5
            zNaught = parameters.blood_density * cNaught / (1 - parameters.poission_ratio) ** 0.5 
            self._resistance += zNaught * (1 + parameters.nominal_reflection_coefficient) / (1 - parameters.nominal_reflection_coefficient)
            self._sinks.append(genericSink)

    def isTail(self):
        return self._tail
    
    def addEdge(self, edge):
        assert(isinstance(edge, Node))
        self.edges.append(edge)

    def setStart(self, start):
        assert(isinstance(start, Point))
        self.start = start
    
    def setEnd(self, end):
        assert(isinstance(end, Point))
        self.end = end

    def addOrgan(self, organ):
        assert(isinstance(organ, Organ))
        if len(self._sinks) == 1 and isinstance(self._sinks[0], GenericSink):
            self._sinks = []
        self._sinks.append(organ)

    def getFlowVelocity(self):
        return self._velocity

    def getChildren(self): #return both nodes and organs
        if len(self._sinks) == 0:
            return self.edges
        
        children = []
        for edge in self.edges:
            children.append(edge)
        children.extend(self._sinks)
        return children

    def enterImmuneCellCluster(self, cluster):
        assert(isinstance(cluster, AbstractImmuneCellCluster))
        self.immuneCellClusters.append(cluster)
        cluster.enterHost(self)

    def exitImmuneCellCluster(self, cluster):
        assert(isinstance(cluster, AbstractImmuneCellCluster))
        assert(cluster in self.immuneCellClusters)
        assert(cluster.canExitHost())
        self.immuneCellClusters.remove(cluster)
        cluster.exitHost()
        if self._tail:
            heappush(globals.terminalOutputEvent, (globals.time + parameters.vein_travel_time, cluster))

    def getImmuneCellCount(self):
        count = 0
        for cluster in self.immuneCellClusters:
            count += cluster.getCellCount()
        return count

    def getBacteriaCount(self):
        count = 0
        for cluster in self.bacteriaClusters:
            count += cluster.getCellCount()
        return count

    def getImmuneCellClusters(self):
        return self.immuneCellClusters

    def getBacteriaClusters(self):
        return self.bacteriaClusters

    def exitBacteriaCluster(self, cluster):
        assert(isinstance(cluster, AbstractBacteriaCellCluster))
        assert(cluster in self.bacteriaClusters)
        assert(cluster.canExitHost())
        self.bacteriaClusters.remove(cluster)
        cluster.exitHost()
        if self._tail:
            heappush(globals.terminalOutputEvent, (globals.time + parameters.vein_travel_time, cluster))                

    def enterBacteriaCluster(self, cluster):
        assert(isinstance(cluster, AbstractBacteriaCellCluster))
        self.bacteriaClusters.append(cluster)
        cluster.enterHost(self)

    def setFlow(self, flow): #return actualFlow
        assert(flow >= 0)
        if (self.residualVolume + flow) > self.volume:
            flow = self.volume - self.residualVolume
            self.residualVolume = self.volume
        else:
            self.residualVolume += flow
        return flow

    def setParent(self, p): #may be used to calculate this velocity
        assert(isinstance(p, Node))
        self._parent = p

    def getFlowVelocity(self):
        if self.parent is not None:
            self._velocity = self.parent.radius / self.radius * self.parent._velocity
        return self._velocity

    def timeStep(self):
        if globals.time % parameters.cell_count_history_interval == 0:
            self.bacteriaCountHistory.append(self.getBacteriaCount())

        assert(len(self.edges) > 0 or len(self._sinks) > 0)
        hosts = self.getChildren()
        flows = []
        actualFlow = 0

        for node in hosts:
            node_velocity = self.getFlowVelocity()
            deltaP = 0.5 * parameters.blood_density * abs(self._velocity ** 2 - node_velocity ** 2)
            flowRate = deltaP / self._resistance
            flow = flowRate * parameters.delta_t
            flows.append(flow)
        if sum(flows) > self.residualVolume:
            if not globals.printed_lowering_delta_t_message:
                print('******Please consider lowering delta_t.******')
                globals.printed_lowering_delta_t_message = True
            factor = self.residualVolume / sum(flows)
            flows = [float(i) * factor for i in flows ]


        for flow, host in zip(flows, hosts):
            flow = host.setFlow(flow)
            actualFlow += flow

        approxBacteriaCellsToExit = actualFlow / self.volume * self.getBacteriaCount()
        approxImmuneCellsToExit = actualFlow / self.volume * self.getImmuneCellCount()
        
        #Handle bacteria and immune cells
        cellsLeftCount = 0
        for cluster in self.bacteriaClusters:
            if not cluster.canExitHost():
                continue
            #random child node to enter
            hostToEnter = int(np.random.uniform(0, len(hosts)))
            self.exitBacteriaCluster(cluster)
            hosts[hostToEnter].enterBacteriaCluster(cluster)
            cluster.enterHost(hosts[hostToEnter])
            cellsLeftCount += cluster.getCellCount()
            if cellsLeftCount >= approxBacteriaCellsToExit:
                break

        cellsLeftCount = 0
        for cluster in self.immuneCellClusters:
            if not cluster.canExitHost():
                continue
            #random child node to enter
            hostToEnter = int(np.random.uniform(0, len(hosts)))
            self.exitImmuneCellCluster(cluster)
            hosts[hostToEnter].enterImmuneCellCluster(cluster)
            cluster.enterHost(hosts[hostToEnter])
            cellsLeftCount += cluster.getCellCount()
            if cellsLeftCount >= approxImmuneCellsToExit:
                break

        self.residualVolume -= actualFlow
        assert(self.residualVolume >= 0 and self.residualVolume <= self.volume)
        
    def __repr__(self):
        return "Node: " + self.name + "\n" \
            + "    id: " + str(self.id) + " length: " + "{:.2f}".format(self.length) + " \n" \
            + "    radius: " + "{:.2f}".format(self.radius) + " wall thickness: " + "{:.2f}".format(self.wall_thickness) + "\n" \
            + "    E: " + "{:.2f}".format(self.youngs_modulus) + " yaw: " + str(self.yaw) + " pitch: " + str(self.pitch) + "\n" \
            + "    start: " + str(self.start) + " end: " + str(self.end) + "\n"
