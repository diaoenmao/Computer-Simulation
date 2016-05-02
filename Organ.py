from Point import *
from Container import *
from AbstractHost import *
import Node
import numpy as np
from globals import globals
from parameters import *
from heapq import heappush, heappop
from AbstractBacteriaCellCluster import *

class Organ(AbstractHost):
    #retention rate.
    def __init__(self, name, id, mass, sideLength, length, _from, start_points, end_points, health=100):
        self.name = name
        self.id = id
        self.mass = mass
        self.sideLength = sideLength
        self.length = length
        self.start_points = start_points
        self.end_points = end_points
        self.parents = []
        self.health = health
        self.bacteriaClusters = []
        self.immuneCellClusters = []
        self._from = _from
        self._sideLengthBoxes = round(0.5+(float(sideLength) / parameters.organ_grid_resolution))
        self._lengthBoxes = round(0.5+(float(length) / parameters.organ_grid_resolution))
        self._grid = np.empty((self._sideLengthBoxes, self._sideLengthBoxes, self._lengthBoxes), dtype=Container)
        for i in range(self._sideLengthBoxes):
            for j in range(self._sideLengthBoxes):
                for k in range(self._lengthBoxes):
                    self._grid[i][j][k] = Container()
        xs = np.random.uniform(0, self._sideLengthBoxes, 2)
        ys = np.random.uniform(0, self._sideLengthBoxes, 2)
        zs = np.random.uniform(0, self._lengthBoxes, 2)
        self._grid_entrance = Point(int(xs[0]), int(ys[0]), int(zs[0]))

        self._grid_exit = Point(int(xs[1]), int(ys[1]), int(zs[1]))
        self.volume = sideLength ** 2 * length
        self.residualVolume = 0
        self._flowEvent = []
        self.bacteriaCountHistory = []

    def getCellCountHistory(self):
        return self.bacteriaCountHistory

    def setHealth(self, heath):
        self.heath = heath
    
    def getHealth(self, heath):
        return self.health
    
    def setFlow(self, flow): #return actualFlow
        if (self.residualVolume + flow) > self.volume:
            flow = self.volume - self.residualVolume
            self.residualVolume = self.volume
        else:
            self.residualVolume += flow
        heappush(self._flowEvent, (globals.time + int(self.length / (self.getFlowVelocity() * parameters.delta_t)), flow))
        return flow

    def setParent(self, parents): #may be used to calculate this velocity
        self.parents = parents

    def addParent(self, parent):
        assert(isinstance(parent, Node.Node))
        self.parents.append(parent)

    def addStart(self, start_point):
        assert(isinstance(start_point, Point))
        self.start_points.append(start_point)

    def addEnd(self, end_point):
        assert(isinstance(end_point, Point))
        self.end_points.append(end_point)

    def getChildren(self): #return both nodes and organs
        return None
        
    def getFlowVelocity(self):
        return parameters.sink_velocity

    def enterImmuneCellCluster(self, cluster):
        assert(isinstance(cluster, AbstractImmuneCellCluster))
        self.immuneCellClusters.append(cluster)
        container = self._grid[self._grid_entrance.x][self._grid_entrance.y][self._grid_entrance.z]
        assert container is not None

        container.immuneCellClusters.append(cluster)
        cluster.enterHost(self)
        cluster.setRelativeLocation(self._grid_entrance)

    def exitImmuneCellCluster(self):
        for cluster in self.immuneCellClusters:
            if not cluster.canExitHost():
                continue
            point = cluster.getRelativeLocation()
            assert point is not None
            if point == self._grid_exit:
                #exit
                cluster.exitHost()
                self.immuneCellClusters.remove(cluster)
                self._grid[self._grid_exit.x][self._grid_exit.y][self._grid_exit.z].removeBacteriaCluster(cluster)
                heappush(globals.terminalOutputEvent, (globals.time + parameters.vein_travel_time, cluster))                

    def getImmuneCellCount(self):
        cellCount = 0
        for node in self.immuneCellClusters:
            cellCount += node.getCellCount()
        return cellCount
        
    def getBacteriaCount(self):
        bacteriaCount = 0
        for node in self.bacteriaClusters:
            bacteriaCount += node.getCellCount()
        return bacteriaCount
    
    def getBacteriaClusters(self):
        return self.bacteriaClusters

    def getImmuneCellClusters(self):
        return self.immuneCellClusters

    def enterBacteriaCluster(self, cluster):
        assert(isinstance(cluster, AbstractBacteriaCellCluster))
        self.bacteriaClusters.append(cluster)
        container = self._grid[self._grid_entrance.x][self._grid_entrance.y][self._grid_entrance.z]
        assert container is not None

        container.bacteriaClusters.append(cluster)
        cluster.enterHost(self)
        cluster.setRelativeLocation(self._grid_entrance)

    def exitBacteriaCluster(self):
        for cluster in self.bacteriaClusters:
            if not cluster.canExitHost():
                continue
            point = cluster.getRelativeLocation()
            assert point is not None
            if point == self._grid_exit:
                #exit
                cluster.exitHost()
                self._grid[self._grid_exit.x][self._grid_exit.y][self._grid_exit.z].removeBacteriaCluster(cluster)
                self.bacteriaClusters.remove(cluster)
                heappush(globals.terminalOutputEvent, (globals.time + parameters.vein_travel_time, cluster))                
                
    def interact(self):
        if self.bacteriaClusters:
            for bacteriaCluster1 in self.bacteriaClusters:
                for bacteriaCluster2 in self.bacteriaClusters:
                    if(bacteriaCluster1.getRelativeLocation()==bacteriaCluster2.getRelativeLocation()):
                        bacteriaCluster1.inContact(bacteriaCluster2)
                        bacteriaCluster2.inContact(bacteriaCluster1)
        if self.immuneCellClusters:
            for immuneCellCluster1 in self.immuneCellClusters:
                for immuneCellCluster2 in self.immuneCellClusters:
                    if(immuneCellCluster1.getRelativeLocation()==immuneCellCluster2.getRelativeLocation()):
                        immuneCellCluster1.inContact(immuneCellCluster2)
                        immuneCellCluster2.inContact(immuneCellCluster1)
        if self.bacteriaClusters and self.immuneCellClusters:
            for bacteriaCluster in self.bacteriaClusters:
                for immuneCellCluster in self.immuneCellClusters:
                    if(bacteriaCluster.getRelativeLocation()==immuneCellCluster.getRelativeLocation()):
                        bacteriaCluster.inContact(cluster)
                        immuneCellCluster.inContact(bacteriaCluster)

    def moveClusters(self):
        print(self.bacteriaClusters)
        for bacteriaCluster in self.bacteriaClusters:
            index = bacteriaCluster.getRelativeLocation()
            assert index is not None
            move_range = max(int(bacteriaCluster.getMoveSpeed() / parameters.organ_grid_resolution), 1)
            concentration = []
            for i in range(-move_range,move_range+1):
                if int(index.x + i) < 0 or int(index.x + i) >= len(self._grid):
                    continue
                for j in range(-move_range,move_range+1):
                    if int(index.y + j) < 0 or int(index.y + j) >= len(self._grid[0]):
                        continue
                    for k in range(-move_range,move_range+1):
                        if int(index.z + k) < 0 or int(index.z + k) >= len(self._grid[0][0]):
                            continue
                        concentration.append((self._grid[index.x + i][index.y + j][index.z + k].getBacteriaClustersConcentration(), (index.x + i, index.y + j, index.z + k)))
            
            if len(concentration) == 0:
                print(len(self._grid))
                print(index)
            print(len(self._grid))
            print(index)
            concentration, loc = min(concentration)
            (new_x, new_y, new_z) = loc
            assert new_x >= 0 and new_x < len(self._grid)
            assert new_y >= 0 and new_y < len(self._grid[0])
            assert new_z >= 0 and new_z < len(self._grid[0][0])

            if(index.x != new_x or index.y != new_y or index.z != new_z):
                self._grid[index.x][index.y][index.z].removeBacteriaCluster(bacteriaCluster)
                self._grid[new_x][new_y][new_z].addBacteriaCluster(bacteriaCluster)
                bacteriaCluster.setRelativeLocation(Point(new_x, new_y, new_z))

        for immuneCellCluster in self.immuneCellClusters:
            index = immuneCellCluster.getRelativeLocation()
            move_range = max(int(immuneCellCluster.getMoveSpeed() / parameters.organ_grid_resolution), 1)
            concentration = []
            for i in range(-move_range, move_range+1):
                if (index.x + i) < 0 or (index.x + i) >= len(self._grid):
                    continue
                for j in range(-move_range, move_range+1):
                    if (index.y + j) < 0 or (index.y + j) >= len(self._grid[0]):
                        continue
                    for k in range(-move_range, move_range+1):
                        if (index.z + k) < 0 or (index.z + k) >= len(self._grid[0][0]):
                            continue
                        concentration.append((self._grid[index.x + i][index.y + j][index.z + k].getImmuneCellClustersConcentration(), (index.x + i, index.y + j, index.z + k)))
           
            concentration, loc = min(concentration)
            (new_x, new_y, new_z) = loc
            assert new_x >= 0 and new_x < len(self._grid)
            assert new_y >= 0 and new_y < len(self._grid[0])
            assert new_z >= 0 and new_z < len(self._grid[0][0])
            if(index.x != new_x or index.y != new_y or index.z != new_z):
                self._grid[index.x][index.y][index.z].removeImmuneCellClusterCluster(immuneCellCluster)
                self._grid[new_x][new_y][new_z].addImmuneCellClusterCluster(immuneCellCluster)
                immuneCellCluster.setRelativeLocation(Point(new_x, new_y, new_z))
    
    def timeStep(self):
        if globals.time % parameters.cell_count_history_interval == 0:
            self.bacteriaCountHistory.append(self.getBacteriaCount())

        #Move, Grow bacteria
        for cluster in self.bacteriaClusters:
            cluster.timeStep()

        #Immune response -> move, attack bacteria, remove infected host cells
        for cluster in self.immuneCellClusters:
            cluster.timeStep()
        
        while len(self._flowEvent) > 0 and self._flowEvent[0][0] <= globals.time:
            (time, flow) = heappop(self._flowEvent)
            self.residualVolume -= flow
            assert(self.residualVolume >= 0)

        #Calculate new cells position
        self.moveClusters()
            
        #Interactions betwee cell clusters
        self.interact()
        #exits
        self.exitBacteriaCluster()
        self.exitImmuneCellCluster()

    def __repr__(self):
        return "Organ: " + self.name + "\n" \
            + "    id: " + str(self.id) + " mass: " + str(self.mass) + " \n" \
            + "    length: " + str(self.length) + "\n" \
            + "    side length: " + str(self.sideLength) + "\n" \
            + "    health: " + str(self.health) + "\n" \
