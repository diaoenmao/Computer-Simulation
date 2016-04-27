from abc import *

class AbstractHost(metaclass=ABCMeta):
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
    def __repr__(self):
        ...
