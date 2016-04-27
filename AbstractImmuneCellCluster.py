from AbstractCellCluster import *

class AbstractImmuneCellCluster(AbstractCellCluster):
    @abstractmethod
    def enterHost(self, host):
        ...

    @abstractmethod
    def canExitHost(self):
        ...

    @abstractmethod 
    def exitHost(self):
        ...

    @abstractmethod
    def disrupt(self, bacteriaClusters): #Return T/F for changes
        ...
