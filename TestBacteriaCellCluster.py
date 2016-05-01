from AbstractCellCluster import * 
from Point import *
from sequences import bacteriaClusterSq
import math

class TestBacteriaCellCluster(AbstractCellCluster):
    def __init__(self, host):
        self.name = "Test bacteria cell"
        self.id = bacteriaClusterSq.getNextVal()
        self.isDead = False
        self.location = None
        self.host = None
        self.cellCount = cellCount
        self.lifespan = parameters.bacteria_lifespan

    def getCellcount(self):
        return int(self.cellCount)

    def getName(self):
        return self.name

    def setRelativeLocation(self, point):
        assert(isinstance(point, Point))
        self.location = point

    def getRelativeLocation(self):
        return self.location

    def _reproduce(self): #private method
        self.cellCount += math.ceil(self.cellCount * parameters.bacteria_reproduction_rate)

    def death(self):
        self.isDead = True

    def _age(self):
        self.cellCount -= 1
        if(self.cellCount <= 0)
            self.isDead = True
        
    def getMoveSpeed(self):
        return 0

    def inContact(self, cluster):
        if self.isDead:
            return
        if(isinstance(cluster, TestBacteriaCellCluster)):
            cluster.death()
            
            #merge clusters
            self.cellCount += cluster.getCellcount()

    def timeStep(self, host):
        assert(self.host is not None)
        assert(self.location is not None)
        self._reproduce()
        self._age()

    def beDisrupted(self, count): #Return new bacteria count
        self.cellCount -= int(count/self.cellCount)

    def __repr__(self):
        return self.name + "\n    id: " + str(self.id)