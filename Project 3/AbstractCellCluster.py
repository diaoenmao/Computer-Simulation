from abc import *

class AbstractCellCluster(metaclass=ABCMeta):
    @abstractmethod
    def getCellCount(self):
        ...

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
    def getName(self):
        ...

    @abstractmethod
    def setRelativeLocation(self, point):
        ...

    @abstractmethod
    def getRelativeLocation(self):
        ...

    @abstractmethod
    def _reproduce(self): #private method
        ...

    @abstractmethod
    def _age(self): #private method
        ...

    @abstractmethod
    def death(self):
        ...

    @abstractmethod
    def getMoveSpeed(self):
        ...

    @abstractmethod
    def inContact(self, cluster):
        ...

    @abstractmethod
    def timeStep(self, host):
        ...

    @abstractmethod
    def __repr__(self):
        ...