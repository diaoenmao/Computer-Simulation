from Point import *
class Node:

    def __init__(self, name, id, length, radius, wall_thickness, youngs_modulus, f0, _from, _to, yaw, pitch, p1, p2, isTail=False):
        assert(isinstance(p1, Point))
        assert(isinstance(p2, Point))
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
        self.yaw = yaw
        self.pitch = pitch
        self.cells = []
        self.bacteria = []
        
    def setTail(self, isTail):
        self.tail = isTail
    
    def addEdge(self, edge):
        self.edges.append(edge)
    def setStart(self, start):
        assert(isinstance(start, Point))
        self.start = start
    def setEnd(self, end):
        assert(isinstance(end, Point))
        self.end = end
    def cellCount(self):
        return length(cells)
    def bacteriaCount(self):
        return length(bacteria)
    def __repr__(self):
        return "Node: " + self.name + "\n" \
            + "    id: " + str(self.id) + " length: " + "{:.2f}".format(self.length) + " \n" \
            + "    radius: " + "{:.2f}".format(self.radius) + " wall thickness: " + "{:.2f}".format(self.wall_thickness) + "\n" \
            + "    E: " + "{:.2f}".format(self.youngs_modulus) + " yaw: " + str(self.yaw) + " pitch: " + str(self.pitch) + "\n" \
            + "    start: " + str(self.start) + " end: " + str(self.end) + "\n"
