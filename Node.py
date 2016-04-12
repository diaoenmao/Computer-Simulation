class Node:

    def __init__(self, name, id, length, radius, wall_thickness, youngs_modulus, f0, _from, _to, p1, p2, isTail=False):
        self.name = name
        self.id = id
        self.length = length
        self.radius = radius
        self.wall_thickness = wall_thickness
        self.youngs_modulus = youngs_modulus
        self.f0 = f0
        self._from = _from
        self._to = _to
        self.start = p1
        self.end = p2
        self.tail = isTail
        self.edges =[]
    def setTail(self, isTail):
        self.tail = isTail
    
    def addEdge(self, edge):
        self.edges.append(edge)
    
    def __repr__(self):
        return "Node: " + self.name + "\n" \
            + "    id: " + str(self.id) + " length: " + str(self.length) + " \n" \
            + "    radius: " + self.radius + " wall thickness: " + str(self.wall_thickness) + "\n" \
            + "    E: " + str(self.youngs_modulus) + "\n" \
            + "    start: " + str(self.start) + " end: " + str(self.end) + "\n"
