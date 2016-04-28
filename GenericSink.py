from AbstractImmuneCellCluster import *
from AbstractBacteriaCellCluster import *
from AbstractHost import *
from parameters import * 
from sequences import bacteriaClusterSq
from heapq import heappush, heappop
from globals import globals

class GenericSink(AbstractHost):
    def __init__(self, name, cluster):
        self.name = name
        self.id = bacteriaClusterSq.getNextVal()
        self.exitBacteriaClusterEvent = []
        self.exitImmuneCellClusterEvent = []
        self.immuneCellClusters = []
        self.bacteriaClusters = []
        if cluster is not None:
            assert(isinstance(cluster, AbstractBacteriaCellCluster))
            self.bacteriaClusters.append(cluster)

    def enterImmuneCellCluster(self, cluster):
        assert(isinstance(cluster, AbstractImmuneCellCluster))
        self.immuneCellClusters.append(cluster)
        heappush(self.exitImmuneCellClusterEvent, (globals.time + parameters.sink_travel_time, cluster))
        cluster.enterHost(self)

    def exitImmuneCellCluster(self):
        assert False #detect bacteria
        if False:
            ...
        exited = 0
        while len(self.exitImmuneCellClusterEvent) > 0 and self.exitImmuneCellClusterEvent[0][0] <= globals.time:
            (time, cluster) = heappop(self.exitImmuneCellClusterEvent)
            if not cluster.canExitHost():
                heappush(self.exitImmuneCellClusterEvent, (globals.time + parameters.sink_travel_time, cluster))
            else:
                self.immuneCellClusters.remove(cluster)
                exited += cluster.getImmuneCellCount()
        return exited

    def getImmuneCellCount(self):
        count = 0
        for cluster in self.immuneCellClusters:
            count += cluster.getCellCount()

    def enterBacteriaCluster(self, cluster):
        assert(isinstance(cluster, AbstractBacteriaCellCluster))
        bacteriaClusters.append(cluster)
        heappush(self.exitBacteriaClusterEvent, (globals.time + parameters.sink_travel_time, cluster))
        cluster.enterHost(self)

    def timeStep(self):
        #Grow bacteria
        for cluster in self.bacteriaClusters:
            cluster.timeStep(self)

        #Immune response -> move, attack bacteria, remove infected host cells
        for cluster in self.immuneCellClusters:
            cluster.timeStep(self)

        #calculate exit flow

        #interations

        #exits
        self.exitBacteriaCluster()
        self.exitImmuneCellCluster()

    def getBacteriaCount(self):
        count = 0
        for cluster in self.bacteriaClusters:
            count += cluster.getCellCount()
        return count

    def getBacteriaClusters(self):
        return self.bacteriaClusters

    def getImmuneCellClusters(self):
        return self.immuneCellClusters

    def exitBacteriaCluster(self):
        exited = 0
        while len(self.exitBacteriaClusterEvent) > 0 and self.exitBacteriaClusterEvent[0][0] <= globals.time:
            (time, cluster) = heappop(self.exitBacteriaClusterEvent)
            if not cluster.canExitHost():
                heappush(self.exitBacteriaClusterEvent, (globals.time + parameters.sink_travel_time, cluster))
            else:
                self.bacteriaClusters.remove(cluster)
                exited += cluster.getBacteriaCount()
        return exited

    def setFlow(self, flow): #return actualFlow
        assert False
        return flow

    def setParent(self, p): #may be used to calculate this velocity
        assert(isinstance(p, Node))
        self._parent = p

    def getFlowVelocity(self):
        return parameters.sink_velocity

    def __repr__(self):
        return "Sink: " + self.name + "\n" \
            + "    id: " + str(self.id) \
            + "    bacteria count: " + str(self.getBacteriaCount()) + "\n" \
            + "    immune cell count: " + str(self.getImmuneCellCount()) + " in " + len(self.immuneCellClusters) + " cluster(s)."
