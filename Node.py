from Point import *
from Organ import *
from AbstractHost import *
from AbstractBacteriaCellCluster import *
from AbstractImmuneCellCluster import *
from GenericSink import *
from parameters import * 
import math

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
        if  self._to == [0]:
            self.setTail(True)

    def setTail(self, isTail):
        self._tail = isTail
        if not self._tail and hasattr(self, '_sinks'):
            del self._sinks
        if self._tail and not hasattr(self, '_sinks'):
            self._sinks = []
            genericSink = GenericSink("Sink for Node id: " + str(self.id) + ", " + self.name, None)
            cNaught = (self.youngs_modulus * self.wall_thickness / (2 * parameters.blood_density * self.radius)) ** 0.5
            zNaught = parameters.blood_density * cNaught / (1 - parameters.poission_ratio) ** 0.5 
            print( self._resistance )
            self._resistance += zNaught * (1 + parameters.nominal_reflection_coefficient) / (1 - parameters.nominal_reflection_coefficient)
            print( self._resistance )

    def isTail(self):
        return self._tail
    
    def addEdge(self, edge):
        self.edges.append(edge)
    
    def setStart(self, start):
        assert(isinstance(start, Point))
        self.start = start
    
    def setEnd(self, end):
        assert(isinstance(end, Point))
        self.end = end

    def addOrgan(self, organ):
        assert(self._tail)
        assert(isinstance(organ, Organ))
        self._sinks.append(organ)

    def enterImmuneCellCluster(self, cluster):
        assert(isinstance(cluster, AbstractImmuneCellCluster))
        self.immuneCellClusters.append(cluster)

    def exitImmuneCellCluster(self):
        assert(isinstance(cluster, AbstractImmuneCellCluster))
        assert(cluster in self.immuneCellClusters)
        self.immuneCellClusters.remove(cluster)

    def getImmuneCellCount(self):
        count = 0
        for cluster in self.immuneCellClusters:
            count += cluster.getCellCount()

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
        self.bacteriaClusters.remove(cluster)

    def enterBacteriaCluster(self, cluster):
        assert(isinstance(cluster, AbstractBacteriaCellCluster))
        self.bacteriaClusters.append(cluster)

    def timeStep(self):
        assert False
        deltaP = 0.5 * parameters.blood_density * ()
        flow = deltaP * self._resistance

    def __repr__(self):
        return "Node: " + self.name + "\n" \
            + "    id: " + str(self.id) + " length: " + "{:.2f}".format(self.length) + " \n" \
            + "    radius: " + "{:.2f}".format(self.radius) + " wall thickness: " + "{:.2f}".format(self.wall_thickness) + "\n" \
            + "    E: " + "{:.2f}".format(self.youngs_modulus) + " yaw: " + str(self.yaw) + " pitch: " + str(self.pitch) + "\n" \
            + "    start: " + str(self.start) + " end: " + str(self.end) + "\n"
