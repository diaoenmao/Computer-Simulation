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
        self.exitBacteriaCountEvent = []
        self.immuneCellClusters = []
        self.bacteriaClusters = []
        if cluster is not None:
            assert(isinstance(cluster, AbstractBacteriaCellCluster))
            self.bacteriaClusters.append(cluster)

    def enterImmuneCellCluster(self, cluster):
        assert(isinstance(cluster, AbstractImmuneCellCluster))
        self.immuneCellClusters.append(cluster)

    def exitImmuneCellCluster(self, cluster):
        assert(cluster in self.immuneCellClusters)
        self.immuneCellClusters.remove(cluster)

    def getImmuneCellCount(self):
        count = 0
        for cluster in self.immuneCellClusters:
            count += cluster.getCellCount()

    def enterBacteriaCluster(self, cluster):
        assert(isinstance(cluster, AbstractBacteriaCellCluster))
        bacteriaClusters.append(cluster)
        heappush(self.exitBacteriaCountEvent, (globals.time + parameters.sink_travel_time, cluster))

    def timeStep(self):
        #Grow bacteria
        for cluster in self.bacteriaClusters:
            cluster.timeStep(self)

        #Immune response -> move, attack bacteria, remove infected host cells
        for cluster in self.immuneCellClusters:
            cluster.timeStep(self)

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
        while len(self.exitBacteriaCountEvent) > 0 and self.exitBacteriaCountEvent[0][0] <= globals.time:
            (time, bacteriaCount) = heappop(self.exitBacteriaCountEvent)
            exited += bacteriaCount
        return exited

    def __repr__(self):
        return "Sink: " + self.name + "\n" \
            + "    id: " + str(self.id) \
            + "    bacteria count: " + str(self.getBacteriaCount()) + "\n" \
            + "    immune cell count: " + str(self.getImmuneCellCount()) + " in " + len(self.immuneCellClusters) + " cluster(s)."
