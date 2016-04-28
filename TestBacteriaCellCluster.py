from AbstractCellCluster import * 
from Point import *
from sequences import bacteriaClusterSq

class TestBacteriaCellCluster(AbstractCellCluster):
	def __init__(self, host):
		self.name = "Test bacteria cell"
        self.id = bacteriaClusterSq.getNextVal()
        self.isDead = False
        self.location = None
        self.host = None

    def getCellcount(self):


    def getName(self):
        return self.name

    def setRelativeLocation(self, point):
        assert(isinstance(point, Point))
        self.location = point

    def getRelativeLocation(self):
        return self.location

    def _reproduce(self): #private method
        ...

    def _move(self):
        ...

    def death(self):
        ...

    def getMoveSpeed(self):
        ...

    def inContact(self, cluster):
        ...

    def timeStep(self, host):
        ...

    def beDisrupted(self): #Return new bacteria count
    	...

    def __repr__(self):
        ...