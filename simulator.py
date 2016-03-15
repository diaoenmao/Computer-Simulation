import csv
import math
import networkx as nx
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from Objects import *
from parameters import *
from copy import deepcopy
from heapq import heappush, heappop, heapify
import time
import sys
sys.setrecursionlimit(10**6)

#Process the input file and return the rows of split data.
def processInput(inputFile):
    rows = []
    with open(inputFile) as f:
        c = csv.reader(f, delimiter=',')
        for row in c:
            rows.append(row)

    return rows[1:]

#Binary search for node in a list of nodes
def findNode(nodes, node, i, j):
    end = node.end
    if((j-i) == 1):
        if(nodes[i].start == end or nodes[j].start == end):
            #Check for left
            while(i >= 0 and nodes[i].start == end):
                node.addChildNode(nodes[i])
                i -= 1
            while(j < len(nodes) and nodes[j].start == end):
                node.addChildNode(nodes[j])
                j += 1
    else:
        n = int(math.ceil((j-i)/2.0)) + i
        if(nodes[n].start <= end):
            findNode(nodes, node, n, j)
        else:
            findNode(nodes, node, i, n)

#Graphing function to show the node connections
def showGraph(nodes):
    plt.clf()
    nodes = deepcopy(nodes)
    nodes = sorted(nodes, key=lambda node: node.id)
    G=nx.Graph()
    colors = []
    labels={}
    labelDict = {}
    for node in nodes:
        if str(node.start) not in labelDict.keys():
            labelDict[str(node.start)] = [node.id]
            labels[node.id] = node.carCount()
        else:
            allSamePositionedNodes = labelDict[str(node.start)]
            for nodeId in allSamePositionedNodes:
                labels[nodeId] += node.carCount()
        
        children = node.getChildren()
        if(node.exit):
            G.add_node(node.id, pos=node.end)
            colors.append(EXIT_NODE_COLOR)
            labels[node.id] = node.carCount()
        else:
            G.add_node(node.id, pos=node.start)
            if(node.type == Node.TYPE_STREET):
                colors.append(STREET_NODE_COLOR)
            else:
                colors.append(PARKING_NODE_COLOR)
        for child in children:
            G.add_edge(node.id, child.id)
    pos=nx.get_node_attributes(G,'pos')
    pos=nx.spring_layout(G, pos=pos, fixed=pos.keys())
    nx.draw(G,pos,node_color=colors)
    nx.draw_networkx_labels(G,pos,labels,font_size=16)
    plt.draw()

#Init function that builds the world using the parsed rows
def buildGraph(rows):
    nodes = []
    i = 1
    carId = 1
    events = []
    for row in rows:
        assert(len(row) == 7)

        #Get node type, whether street or parking
        if(row[0] == 'Street'):
            nodeType = Node.TYPE_STREET
            distance = int( math.sqrt((int(row[1]) - int(row[3])) ** 2 + (int(row[2]) - int(row[4])) ** 2) \
                * UNIT_LENGTH )
            capacity = int( 1.0 * distance / AVERAGE_CAR_SPACE_LENGTH ) * int(row[5])
            minTravelTime = int( 1.0 * distance / AVERAGE_CAR_SPEED )
        elif(row[0] == 'Parking'):
            nodeType = Node.TYPE_PARKING
            capacity = int(row[5])
            minTravelTime = 1
        else:
            raise Exception('Uknown type: ' + row[0])

        #Create node( type, (x1, x2), (y1, y2), capacity, minTravelTime, id, comment)
        node = Node(nodeType, (int(row[1]), int(row[2])), (int(row[3]), int(row[4])), capacity, minTravelTime, i, comment=row[6])
        nodes.append(node)

        #Set evcuation destinations
        if(node.end == (760,555) or node.end == (723,32) or node.end == (733,270)):
            node.setExit(True)
            node.capacity = 10000 #arbitrary big number

        #Create return path if not exit node and is a 2 way street
        if(row[0] == 'Street' and not node.exit):
            i += 1
            node = Node(nodeType, (int(row[3]), int(row[4])), (int(row[1]), int(row[2])), capacity, minTravelTime, i, comment=row[6])
            nodes.append(node)

        i += 1
        #Set initial cars in parking lots
        if(nodeType == Node.TYPE_PARKING):
            for n in range(node.capacity):
                car = Car(carId)
                time = minTravelTime + n + genRandom(1)
                heappush(events, (time, Event(car, Event.TYPE_IN_PARKING)))
                node.enterCar(car)
                carId += 1
    
    #Make node connections with its children.    
    nodes = sorted(nodes, key=lambda node: node.start)
    for node in nodes:
        findNode(nodes, node, 0, len(nodes) - 1)
    return (nodes, events)

def simulate():
    simulationTime = 0
    rows = processInput('world.csv')
    (nodes, events) = buildGraph(rows)
    itr = 0
    showGraph(nodes)
    plt.show(False)
    while len(events) > 0:
        (time, event) = heappop(events)
        simulationTime = time
        event.eventHandler(events, event, simulationTime)
        if(itr % 5000 == 0):
            showGraph(nodes)
            plt.pause(0.01)
        itr += 1


def printDistribution():
    n = 2500
    l = 5.0
    seed (20160224)
    e = [genRandom (l, type='exponential') for i in range (n)]
    u = [genRandom (l, type='uniform') for i in range (n)]
    g = [genRandom (l, type='normal') for i in range (n)]
    plt.figure(1)
    plt.hist (e)
    plt.show()
    plt.figure(2)
    plt.hist (u)
    plt.show()
    plt.figure(3)
    plt.hist (g)
    plt.show()

simulate()
