from AbstractCellCluster import *

class AbstractBacteriaCellCluster(AbstractCellCluster):
    @abstractmethod
    def beDisrupted(self): #Return new bacteria count
        ...