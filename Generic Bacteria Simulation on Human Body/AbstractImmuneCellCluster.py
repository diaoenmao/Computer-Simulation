from AbstractCellCluster import *

class AbstractImmuneCellCluster(AbstractCellCluster):
    
    @abstractmethod
    def disrupt(self, bacteriaClusters): #Return T/F for changes
        ...
