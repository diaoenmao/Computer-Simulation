from AbstractBacteriaCellCluster import *
from AbstractHost import *
from Point import *
from sequences import bacteriaClusterSq
import math
import parameters as p

class TestBacteriaCellCluster(AbstractBacteriaCellCluster):
    def __init__(self, cellCount):
        self.name = "Test bacteria cell"
        self.id = bacteriaClusterSq.getNextVal()
        self.isDead = False
        self.location = None
        self.host = None
        self.cellCount = cellCount
        self.lifespan = p.parameters.bacteria_lifespan

    def __lt__(self,other):
        return True

    def getCellCount(self):
        return int(self.cellCount)

    def enterHost(self, host):
        assert(isinstance(host, AbstractHost))
        self.location = None
        self.host = host

    def canExitHost(self):
        return True
 
    def exitHost(self):
        self.host = None

    def getName(self):
        return self.name

    def setRelativeLocation(self, point):
        assert(isinstance(point, Point))
        self.location = point

    def getRelativeLocation(self):
        return self.location

    def _reproduce(self): #private method
        self.cellCount += math.ceil(self.cellCount * p.parameters.bacteria_reproduction_rate)

    def death(self):
        self.isDead = True

    def _age(self):
        self.cellCount -= 1
        if(self.cellCount <= 0):
            self.isDead = True
        
    def getMoveSpeed(self):
        return 0.01

    def inContact(self, cluster):
        if self.isDead:
            return
        if(isinstance(cluster, TestBacteriaCellCluster)):
            cluster.death()
            
            #merge clusters
            self.cellCount += cluster.getCellCount()

    def timeStep(self):
        assert(self.host is not None)
        self._reproduce()
        self._age()

    def beDisrupted(self, count): #Return new bacteria count
        self.cellCount -= int(count/self.cellCount)

    def __repr__(self):
        return self.name + "\n    id: " + str(self.id) + str(self.location)