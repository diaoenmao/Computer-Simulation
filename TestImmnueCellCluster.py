from AbstractImmuneCellCluster import *
from Point import *
from sequences import immuneCellClusterSq

class TestImmuneCellCluster(AbstractImmuneCellCluster):
	def __init__(self, host):
		self.name = "Test immune cell"
        self.id = immuneCellClusterSq.getNextVal()
        self.isDead = False
        self.location = None
        self.host is not None

    def getCellcount(self):
        return 0

    def getName(self):
        return self.name
    
    def setRelativeLocation(self, point):
        assert(isinstance(point, Point))
        self.location = point
    
    def getRelativeLocation(self):
        return self.location
    
    def _reproduce(self): #private method
        return

    def death(self):
        self.isDead = True
    
    def getMoveSpeed(self):
        return 0

    def inContact(self, cluster):
        self.isDead = True
        return cluster
    
    def timeStep(self):
        assert(self.host is not None)
        assert(self.location is not None)
        self._reproduce()
        self._move()

    def _move():
        return

    def __repr__(self):
        return self.name + "\n    id: " + str(self.id)
    
    def enterHost(self, host):
        self.host = host

    def canExitHost(self):
        return True
  
    def exitHost(self):
        self.host = None
    
    def disrupt(self, bacteriaClusters): #Return new bacteria count or None
        assert(self.host is not None)
        assert(self.location is not None)
        return False
