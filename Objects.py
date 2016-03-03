import types
from parameters import *
from copy import deepcopy
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

def genID(N=5):
    ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))

class Node:
    TYPE_STREET = 0
    TYPE_PARKING = 1
    def __init__(self, type, start, end, capacity, id, comment='', exit=False):
        assert(type == Node.TYPE_PARKING or type == Node.TYPE_STREET)
        self.type = type
        assert(len(start) == 2)
        self.start = start

        assert(len(end) == 2)
        self.end = end

        assert(start != end)
        assert(capacity > 0)
        self.capacity = capacity
        self.comment = comment
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
        return self.__cars.pop()
    def carCount(self):
        return len(self.__cars)
    def canEnterCar(self):
        return(self.carCount() < self.capacity)
    def setExit(self, isExit):
        self.exit = isExit
    def addChildNode(self, node):
        assert(isinstance(node, Node))
        self.__children.append(node)
    def getChildren(self):
        return deepcopy(self.__children)
    def getDirection(self):
        return getDirection(self)
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

class Car:
    def __init__(self, initial):
        assert(isinstance(initial, Node))
        assert((initial.type == Node.TYPE_PARKING))
        self.__currentNode = initial
        self.__path = [initial]
        self.__nextEvent = None
    def setCurrentNode(self, currentNode):
        assert(isinstance(initial, Node))
        assert((initial.type == Node.TYPE_STREET))
        self.__currentNode = currentNode
        self.__path.append(currentNode)
    def getDirection(self):
        return getDirection(self.__currentNode)
    def __str__(self):
        return "Car at location: " + str(self.__currentNode.start) + " next event: " + str(self.__nextEvent)