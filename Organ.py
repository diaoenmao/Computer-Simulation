from Node import *
from AbstractHost import *
import numpy as np
from globals import globals
from parameters import *

class Organ(AbstractHost):
    #retention rate.
    def __init__(self, name, id, coverage, sideLength, length, health=100):
        self.name = name
        self.id = id
        self.length = length
        self.coverage = coverage
        if converge is not None:
            for node in converge:
                assert(isinstance(node, Node))
        self.sideLength = sideLength
        self.health = health
        self.bacteriaClusters = []
        self.immuneCellClusters = []
        self._sideLengthBoxes = round((sideLength + 0.5) / parameters.organ_grid_resolution)
        self._lengthBoxes = round((length + 0.5 ) / parameters.organ_grid_resolution)
        self._grid = np.empty((self._sideLengthBoxes, self._sideLengthBoxes, self._lengthBoxes), dtype=Container)
        xs = np.random(0, self._sideLengthBoxes, 2)
        zs = np.random(0, self._sideLengthBoxes, 2)
        ys = np.random(0, self._lengthBoxes, 2)
        self._grid_entrance = Point(int(xs[0]), int(ys[0]), int(zs[0]))
        self._grid_exit = Point(int(xs[1]), int(ys[1]), int(zs[1]))
        self.volume = sideLength ** 2 * length
        self.residualVolume = 0
        self._flowEvent = []
    def setHealth(self, heath):
        self.heath = heath
    
    def getHealth(self, heath):
        return self.health
    
    def setFlow(self, flow): #return actualFlow
        if (self.residualVolume + flow) > self.volume:
            flow = self.volume - self.residualVolume
            self.residualVolume = self.volume
        else:
            self.residualVolume += flow
        heappush(self._flowEvent, (globals.time + int(self.length / (self.getFlowVelocity() * parameters.delta_t)), flow))
        return flow

    def setParent(self, parent): #may be used to calculate this velocity
        self.parent = parent

    def getFlowVelocity(self):
        return parameters.sink_velocity

    def enterImmuneCellCluster(self, cluster):
        assert(isinstance(cluster, AbstractImmuneCellCluster))
        self.immuneCellClusters.append(cluster)
        container = self._grid[self._grid_entrance.x][self._grid_entrance.y][self._grid_entrance.z]
        assert container is not None

        container.immuneCellClusters.append(cluster)
        cluster.enterHost(self)
        cluster.setRelativeLocation(self._grid_entrance)

    def exitImmuneCellCluster(self):
        for cluster in self.immuneCellClusters:
            if not cluster.canExitHost():
                continue
            point = cluster.getRelativeLocation()
            assert point is not None
            if point == self._grid_exit:
                #exit
                cluster.exitHost(self)
                self.immuneCellClusters.remove(cluster)

    def getImmuneCellCount(self):
        cellCount = 0
        if self.converge is None:
            return cellCount
        for cluster in self.immuneCellClusters:
            cellCount += node.cellCount()
        return cellCount
        
    def getBacteriaCount(self):
        bacteriaCount = 0
        for node in self.bacteriaClusters:
            bacteriaCount += node.bacteriaCount()
        return bacteriaCount
    
    def getBacteriaClusters(self):
        return self.bacteriaClusters

    def getImmuneCellClusters(self):
        return self.immuneCellClusters

    def enterBacteriaCluster(self, cluster):
        assert(isinstance(cluster, AbstractBacteriaCellCluster))
        bacteriaClusters.append(cluster)
        container = self._grid[self._grid_entrance.x][self._grid_entrance.y][self._grid_entrance.z]
        assert container is not None

        container.bacteriaClusters.append(cluster)
        cluster.enterHost(self)
        cluster.setRelativeLocation(self._grid_entrance)

    def exitBacteriaCluster(self):
        for cluster in self.bacteriaClusters:
            if not cluster.canExitHost():
                continue
            point = cluster.getRelativeLocation()
            assert point is not None
            if point == self._grid_exit:
                #exit
                cluster.exitHost(self)
                self.bacteriaClusters.remove(cluster)
                
    def interact(self):
        if not self.bacteriaClusters:
            for bacteriaCluster1 in bacteriaClusters:
                for bacteriaCluster2 in bacteriaClusters:
                    if(bacteriaCluster1.getRelativeLocation()==bacteriaCluster2.getRelativeLocation()):
                        bacteriaCluster1.inContact(bacteriaCluster2)
                        bacteriaCluster2.inContact(bacteriaCluster1)
        if not self.immuneCellClusters:
            for immuneCellCluster1 in immuneCellClusters:
                for immuneCellCluster2 in immuneCellClusters:
                    if(immuneCellCluster1.getRelativeLocation()==immuneCellCluster2.getRelativeLocation()):
                        immuneCellCluster1.inContact(immuneCellCluster2)
                        immuneCellCluster2.inContact(immuneCellCluster1)
        if not self.bacteriaClusters and not self.immuneCellClusters:
            for bacteriaCluster in bacteriaClusters:
                for immuneCellCluster in immuneCellClusters:
                    if(bacteriaCluster.getRelativeLocation()==immuneCellCluster.getRelativeLocation()):
                        bacteriaCluster.inContact(cluster)
                        immuneCellCluster.inContact(bacteriaCluster)
                    
    def timeStep(self):
        #Move, Grow bacteria
        for cluster in self.bacteriaClusters:
            cluster.timeStep(self)

        #Immune response -> move, attack bacteria, remove infected host cells
        for cluster in self.immuneCellClusters:
            cluster.timeStep(self)
        
        while len(self._flowEvent) > 0 and self._flowEvent[0][0] <= globals.time:
            (time, flow) = heappop(self._flowEvent)
            self.residualVolume -= flow
            assert(self.residualVolume > 0)

        #Calculate new cells position
        self.interact()
        #Interactions betwee cell clusters

        #exits
        self.exitBacteriaCluster()
        self.exitImmuneCellCluster()
        assert False

    def __repr__(self):
        return "Organ: " + self.name + "\n" \
            + "    id: " + str(self.id) + " coverage: " + str(self.coverage) + " \n" \
            + "    length: " + self.length + "\n" \
            + "    side length: " + self.sideLength + "\n" \
            + "    health: " + self.health + "\n" \
