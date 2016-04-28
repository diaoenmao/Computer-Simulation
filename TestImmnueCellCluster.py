from AbstractImmuneCellCluster import *
from Point import *
from sequences import immuneCellClusterSq

class TestImmuneCellCluster(AbstractImmuneCellCluster):
	def __init__(self, host, cellCount):
		self.name = "Test immune cell"
        self.id = immuneCellClusterSq.getNextVal()
        self.isDead = False
        self.location = None
        self.host = None
        self.cellCount = cellCount

    def getCellcount(self):
        return self.cellCount

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
        if self.isDead:
            return
        if(isinstance(cluster, TestImmuneCellCluster)):
            cluster.death()
            
            #merge clusters
            self.cellCount += cluster.getCellcount()
		if(isinstance(cluster, TestbacteriaClusters)):
			cluster.beDisrupted(self.cellCount)
			self.disrupt(cluster.getCellcount())
			
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
        self.location = None

    def canExitHost(self):
        return True
  
    def exitHost(self):
        self.host = None
    
    def disrupt(self, count): #Return T / F if disrupt
        assert(self.host is not None)
        assert(self.location is not None)
        return
