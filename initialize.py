import csv
import os
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
    
def buildGraph(rows):
    nodes = []
    events = []
    for row in rows:
        assert(len(row) == 9)
        name = row[0]
        id = row[1]
        length = row[2]
        radius = row[3]
        wall_thickness = row[4]
        youngs_modulus = row[5]
        f0 = row[6]
        if(type(row[7]) is str):
            _from = [ int(numeric_string) for numeric_string in row[7].split(',') ]
        else:
            _from = [ int(numeric_string) for numeric_string in row[7] ]

        if(type(row[8]) is str):
            _to = [ int(numeric_string) for numeric_string in row[8].split(',') ]
        else:
            _to = [ int(numeric_string) for numeric_string in row[8].split(',') ]
        p1 = Point(0,0,0)
        p2 = Point(0,0,0)
        node = Node(name, id, length, radius, wall_thickness, youngs_modulus, f0, _from, _to, p1, p2)
        nodes.append(node)

        #Set end
        if(node._to == 0):
            node.setTail(True)
    
    #Make node connections with its children.    
    nodes = sorted(nodes, key=lambda node: node.id)
    for a_node in nodes:
        for i in a_node._from:
            if(i>0):
                a_node.addEdge(nodes[i-1])
        for j in a_node._to:
            if(j>0):
                a_node.addEdge(nodes[j-1])
    return nodes