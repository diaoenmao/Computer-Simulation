import csv

#Process the input file and return the rows of split data.
def processInput(inputFile):
    rows = []
    with open(inputFile) as f:
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
            _from = row[7].split(',')
        else:
            _from = row[7]
        if(type(row[8]) is str):
            _to = row[8].split(',')
        else:
            _to = row[8]
        
        node = Node(namemo)
        nodes.append(node)

        #Set end
        if(node._to = 0):
            node.setTail(True)
    
    #Make node connections with its children.    
    nodes = sorted(nodes, key=lambda node: node.id)
    return nodes