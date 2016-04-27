from AbstractHost import *

class AbstractSink(AbstractHost):

    @abstractmethod
    def timeStep(self):
        ...

