import csv
import os
import math
from parameters import parameters
from Node import *
from Point import *

#Process the input file and return the rows of split data.
def processInput(inputFile):
    current_directory = os.path.dirname(os.path.realpath(__file__))
    rows = []
    with open(current_directory + inputFile) as f:
        c = csv.reader(f, delimiter=',')
        for row in c:
            rows.append(row)

    return rows[1:]
def setStartEndNodes(node):
    none_point = Point(0,0,0)
    children = node.edges
    for child in children:
        if child.start == none_point:
            child.setStart(Point(node.end.x, node.end.y, node.end.z))
        if child.end == none_point:
            child.setEnd(Point(child.start.x + math.sin(math.radians(child.yaw)) * child.length * parameters.visualization_factor, \
                child.start.y + math.cos(math.radians(child.yaw)) * child.length * parameters.visualization_factor, \
                child.start.z + math.sin(math.radians(child.pitch))))
    for child in children:
        setStartEndNodes(child)

def setStartEndOrgans(organ):
    parents = organ.parents
    for parent in parents:
        organ.addStart(Point(parent.end.x, parent.end.y, parent.end.z))
        organ.addEnd(Point(parent.end.x + math.sin(math.radians(parent.yaw)) * parent.length * parameters.visualization_factor, \
            parent.end.y + math.cos(math.radians(parent.yaw)) * parent.length * parameters.visualization_factor, \
            parent.end.z + math.sin(math.radians(parent.pitch))))
        
def buildGraph(blood_vessels, organs_in):
    nodes = []
    organs = []
    for row in blood_vessels:
        assert(len(row) == 13)
        name = row[0]
        id = int(row[1])
        length = float(row[2])
        radius = float(row[3])
        wall_thickness = float(row[4])
        youngs_modulus = float(row[5])
        f0 = row[6]
        if(type(row[7]) is str):
            _from = [ int(numeric_string) for numeric_string in row[7].split(',') ]
        else:
            _from = [ int(numeric_string) for numeric_string in row[7] ]

        if(type(row[8]) is str):
            _to = [ int(numeric_string) for numeric_string in row[8].split(',') ]
        else:
            _to = [ int(numeric_string) for numeric_string in row[8].split(',') ]
        yaw = float(row[9])
        pitch = float(row[10])
        if(len(row[11]) > 0):
            x,y,z = row[11].split(',')
            p1 = Point(float(x),float(y),float(z))
            x,y,z = row[12].split(',')
            p2 = Point(float(x),float(y),float(z))
        else:
            p1 = Point(0,0,0)
            p2 = Point(0,0,0)
        node = Node(name, id, length, radius, wall_thickness, youngs_modulus, f0, _from, _to, yaw, pitch, p1, p2)
        nodes.append(node)
    
    #Make node connections with its children.    
    nodes = sorted(nodes, key=lambda node: node.id)
    start_node = None
    none_point = Point(0,0,0)
    for node in nodes:
        if start_node is None and not node.start == none_point:
            start_node = node
        for j in node._to:
            if(j>0):
                node.addEdge(nodes[j-1])
                nodes[j-1].setParent(node)
    
    setStartEndNodes(start_node)
    
    for row in organs_in:
        assert(len(row) == 7)
        name = row[0]
        id = int(row[1])
        mass = float(row[2])
        volume = float(row[3])
        if(type(row[4]) is str):
            _from = [ int(numeric_string) for numeric_string in row[4].split(',') ]
        else:
            _from = [ int(numeric_string) for numeric_string in row[4] ]
        sideLength = volume ** (1 / float(3))
        print(sideLength)
        length = volume ** (1 / float(3))
        start_points = []
        end_points = []
        organ = Organ(name, id, length, mass, sideLength, length, start_points, end_points)
        organs.append(organ)    
    
    #Make node connections with organs.     
    organs = sorted(organs, key=lambda node: node.id)
    start_node = None
    for organ in organs:
        for j in organ._from:
            if(j>0):
                nodes[j-1].addEdge(organ)
                organ.addParent(nodes[j-1])
        #Try to figure out start and end
        setStartEndOrgans(organ)

    return nodes