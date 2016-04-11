class Node:

    def __init__(self, name, id, length, radius, wall_thickness, youngs_modulus, f0, _from, _to, (x1,y1), (x2,y2), isTail=False):
        self.name = name
        self.id = id
        self.length = length
        self.radius = radius
        self.wall_thickness = wall_thickness
        self.youngs_modulus = youngs_modulus
        self.f0 = f0
        self._from = _from
        self._to = _to
        self.start = (x1,y1)
        self.end = (x2,y2)
        self.tail = isTail
		self.edge =[]
    def setTail(self, isTail):
        self.tail = isTail
    
	def addEdge(self, edge):
		self.edge.append(edge)
	
    def __repr__(self):
        return "Node: " + name + ", " + id + ", " + length + ", " + radius + ", " + wall_thickness + ", " + youngs_modulus + "\n" \
        + ", " + f0 + ", " + _from +  ", " + _to +  ", " + start +  ", " + end +  ", " + tail + "\n"