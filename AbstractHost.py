from abc import *

class AbstractHost(metaclass=ABCMeta):
    @abstractmethod
    def setFlow(self, flow): #return actualFlow
        ...

    @abstractmethod
    def setParent(self, parent): #may be used to calculate this velocity
        ...

    @abstractmethod
    def getFlowVelocity(self):
        ...

    @abstractmethod
    def getChildren(self):
        ...

    @abstractmethod
    def enterImmuneCellCluster(self, cluster):
        ...

    @abstractmethod
    def exitImmuneCellCluster(self):
        ...

    @abstractmethod
    def getImmuneCellCount(self):
        ...

    @abstractmethod
    def getBacteriaCount(self):
        ...

    @abstractmethod
    def getImmuneCellClusters(self):
        ...

    @abstractmethod
    def getBacteriaClusters(self):
        ...

    @abstractmethod
    def exitBacteriaCluster(self):
        ...

    @abstractmethod
    def enterBacteriaCluster(self, cluster):
        ...
        
    @abstractmethod
    def timeStep(self):
        ...

    @abstractmethod
    def __repr__(self):
        ...
