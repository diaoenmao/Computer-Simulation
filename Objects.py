import types
import numpy as np
from parameters import *
from random import random, seed, gauss
from math import log
from heapq import heappush, heappop, heapify


def getDirection(node):
    (x1,y1) = node.start
    (x2,y2) = node.end
    if((x2-x1) == 0):
        if(y2 > y1):
            deg = 90
        else:
            deg = 270
    elif((y2-y1) == 0):
        if(x2>x1):
            deg = 0
        else:
            deg = 180
    else:
        deg = math.atan((y2-y1)/(x2-x1)) / math.pi * 180
        if(deg < 0):
            deg += 360
        if(y2<y1 and x2<x1):
            deg += 180
        if(y2>y1 and x2<x1):
            deg -= 180
    return deg

def genRandom(l=5, type='exponential'):
    if(type == 'exponential'):
        return np.random.exponential() + l
    elif(type == 'uniform'):
        return np.random.uniform()*l
    elif(type == 'normal'):
        return np.random.normal(loc=l)
    
def genID(N=5):
    ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))

#Parking, streets are all nodes.
#Attributes:
#   type: Either 0/1 0 -> street  1-> parking
#   start, end: tuple
#   capactiy: integer
#   minTravelTime: minimum travel time to exit this road
#   comment: string
#   id: assigned id for easy identification
#   exit: whether this node is a designated evacuation location 
#Each node is connected to the nodes that have start as this node's start.
class Node:
    TYPE_STREET = 0
    TYPE_PARKING = 1
    def __init__(self, type, start, end, capacity, minTravelTime, id, comment='', exit=False):
        assert(type == Node.TYPE_PARKING or type == Node.TYPE_STREET)
        self.type = type
        assert(len(start) == 2)
        self.start = start

        assert(len(end) == 2)
        self.end = end

        assert(start != end)
        assert(minTravelTime > 0)
        assert(capacity > 0)
        self.capacity = capacity
        self.comment = comment
        self.minTravelTime = minTravelTime
        self.id = id
        self.exit = exit
        self.__cars = []
        self.__children = []

    def enterCar(self, car):
        assert(self.canEnterCar())
        assert(isinstance(car, Car))
        self.__cars.append(car)
        car.setCurrentNode(self)

    def exitCar(self):
        return self.__cars.pop(0)
    def carCount(self):
        return len(self.__cars)
    def canEnterCar(self):
        return(self.carCount() < self.capacity)
    def setExit(self, isExit):
        self.exit = isExit
    def addChildNode(self, node):
        assert(isinstance(node, Node))
        self.__children.append(node)
    def getCarPosition(self, car):
        assert(isinstance(car, Car))
        ndx = 0
        for iCar in self.__cars:
            if(car.id == iCar.id):
                return ndx
            ndx += 1
        return -1
    def getChildren(self):
        return self.__children
    def getDirection(self):
        return getDirection(self)
    
    #To string to be used by print()
    def __repr__(self):
        if(self.type == Node.TYPE_STREET):
            nodeType = "\nStreet"
        else:
            nodeType = "\nParking"
        string = nodeType + " ID: " + str(self.id)
        if(self.exit):
            string += " is an exit. "
        if(DEBUG):        
            string += " From " + str(self.start) + " To " + str(self.end) \
                + " Capacity: " + str(self.capacity) + " Current: " + str(self.carCount()) + "\n"
            
            i = 1
            for car in self.__cars:
                string += "\t" + str(i) + ": " + str(car) + "\n"
                i += 1
            if(len(self.__children) > 0):
                string += "Children: \n"
                for child in self.__children:
                    if(child.type == Node.TYPE_STREET):
                        nodeType = "\tStreet"
                    else:
                        nodeType = "\tParking"
                    string += nodeType + " ID: " + str(child.id) + "\n"
        return string

#Car object to keep track of the car's current location and its path.
class Car:
    def __init__(self, id):
        self.__currentNode = None
        self.__path = []
        self.id = id
    def setCurrentNode(self, currentNode):
        assert(currentNode != self.__currentNode)
        assert(isinstance(currentNode, Node))
        self.__currentNode = currentNode
        self.__path.append(currentNode)
    def getDirection(self):
        return getDirection(self.__currentNode)
    def getCurrentNode(self):
        return self.__currentNode
    def __str__(self):
        return "Car id: " + str(self.id) + " at location: " + str(self.__currentNode.start)

def handleParking(events, event, time):
    #Check car's position in exit queue
    car = event.car
    assert(car != None)
    node = car.getCurrentNode()
    assert(node != None)
    carNdx = node.getCarPosition(car)
    assert(carNdx != -1)

    #can't exit
    if(carNdx > 0):
        time = time + node.minTravelTime
        heappush(events, (time, Event(car, Event.TYPE_IN_PARKING)))
        return
    
    if(len(node.getChildren()) > 1):
        print("Car faces intersection.")
        #insert new "at intersection" event
        newEvent = Event(car, Event.TYPE_AT_INTERSECTION) 
        heappush(events, (time + 1, newEvent))
    else:
        print("Car can exit.")
        #can exit.
        assert(len(node.getChildren()) == 1)
        exitedCar = node.exitCar()
        assert(exitedCar.id == car.id)

        #insert new "on street" event
        childNode = node.getChildren()[0]
        childNode.enterCar(car)
        newTime = time + genRandom(node.minTravelTime)
        newEvent = Event(car, Event.TYPE_ON_STREET)
        heappush(events, (newTime, newEvent))
def handleOnStreet(events, event, time):
    car = event.car
    assert(car != None)
    node = car.getCurrentNode()
    assert(node != None)
    exitedCar = node.exitCar()
    #assert(exitedCar.id == car.id)


def handleIntersection(events, event, time):
    car = event.car
    assert(car != None)
    node = car.getCurrentNode()
    assert(node != None)
    exitedCar = node.exitCar()
    assert(exitedCar.id == car.id)


def handleExit(events, event, time):
    pass

class Event:
    TYPE_IN_PARKING = 0
    TYPE_ON_STREET = 1
    TYPE_AT_INTERSECTION = 2
    TYPE_EXIT = 3
    def __init__(self, car, type):
        assert(isinstance(car, Car))
        self.car = car
        self.type = type
        if(type == Event.TYPE_IN_PARKING):
            self.eventHandler = handleParking
        elif(type == Event.TYPE_ON_STREET):
            self.eventHandler = handleOnStreet
        elif(type == Event.TYPE_AT_INTERSECTION):
            self.eventHandler = handleIntersection
        elif(type == Event.TYPE_EXIT):
            self.eventHandler = handleExit
        else:
            raise Exception('Uknown Event type: ' + type)