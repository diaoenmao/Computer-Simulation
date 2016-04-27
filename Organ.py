from Node import *
from AbstractSink import *
import numpy as np
from globals import globals
from parameters import *

class Organ(AbstractSink):
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
        self._grid = np.empty((sideLengthBoxes, sideLengthBoxes, lengthBoxes), dtype=Container)
        xs = np.random(0, self._sideLengthBoxes, 2)
        zs = np.random(0, self._sideLengthBoxes, 2)
        ys = np.random(0, self._lengthBoxes, 2)
        self._grid_entrance = Point(int(xs[0]), int(ys[0]), int(zs[0]))
        self._grid_exit = Point(int(xs[1]), int(ys[1]), int(zs[1]))
    def setHealth(self, heath):
        self.heath = heath
    
    def getHealth(self, heath):
        return self.health
    
    def enterImmuneCellCluster(self, cluster):
        self.immuneCellClusters.append(cluster)
    
    def exitImmuneCellCluster(self,  cluster):
        assert(cluster in immuneCellClusters)
        immuneCellClusters.remove(cluster)

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

    def enterBacteriaCluster(self, cluster):
        bacteriaClusters.append(cluster)
        location = np.random.uniform(0, self._sideLengthBoxes, 2)
        location.append(np.random.uniform(0, self._lengthBoxes))
        location = [int(i) for i in location]
        container = self._grid[location[0]][location[1]][location[2]]
        assert container is not None

        container.bacteriaClusters.append(cluster)

    def exitBacteriaCluster(self):
        ...

    def timeStep(self):
        #Grow bacteria
        for cluster in self.bacteriaClusters:
            cluster.timeStep(self)

        #Immune response -> move, attack bacteria, remove infected host cells
        for cluster in self.immuneCellClusters:
            cluster.timeStep(self)

        self.exitBacteriaCluster()
    def __repr__(self):
        return "Organ: " + self.name + "\n" \
            + "    id: " + str(self.id) + " coverage: " + str(self.coverage) + " \n" \
            + "    length: " + self.length + "\n" \
            + "    side length: " + self.sideLength + "\n" \
            + "    health: " + self.health + "\n" \
