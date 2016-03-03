import csv
import math
import networkx as nx
import matplotlib.pyplot as plt
from Objects import *
from parameters import *
from copy import deepcopy
def processInput(inputFile):
    rows = []
    with open(inputFile) as f:
        c = csv.reader(f, delimiter=',')
        for row in c:
            rows.append(row)

    return rows[1:]

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

def showGraph(nodes):
    nodes = deepcopy(nodes)
    nodes = sorted(nodes, key=lambda node: node.id)
    G=nx.Graph()
    colors = []
    for node in nodes:
        G.add_node(node.id, pos=node.end)
        children = node.getChildren()
        if(node.exit):
            colors.append(EXIT_NODE_COLOR)
        else:
            if(node.type == Node.TYPE_STREET):
                colors.append(STREET_NODE_COLOR)
            else:
                colors.append(PARKING_NODE_COLOR)
        for child in children:
            G.add_edge(node.id, child.id)
    pos=nx.get_node_attributes(G,'pos')
    pos=nx.spring_layout(G, pos=pos, fixed=pos.keys())
    nx.draw_networkx(G,pos,node_color=colors)
    plt.show()

def buildGraph(rows):
    nodes = []
    i = 1
    for row in rows:
        assert(len(row) == 7)
        if(row[0] == 'Street'):
            nodeType = Node.TYPE_STREET
        elif(row[0] == 'Parking'):
            nodeType = Node.TYPE_PARKING
        else:
            raise Exception('Uknown type: ' + row[0])
        node = Node(nodeType, (int(row[1]), int(row[2])), (int(row[3]), int(row[4])), int(row[5]), i, comment=row[6])
        nodes.append(node)
        if(node.end == (760,555) or node.end == (723,32) or node.end == (733,270)):
            node.setExit(True)
        i += 1
    nodes = sorted(nodes, key=lambda node: node.start)
    for node in nodes:
        findNode(nodes, node, 0, len(nodes) - 1)
    return nodes

rows = processInput('world.csv')
nodes = buildGraph(rows)
showGraph(nodes)