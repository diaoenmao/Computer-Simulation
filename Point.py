class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def __repr__(self):
        return "(" + "{:.2f}".format(self.x) + ", " + "{:.2f}".format(self.y) + ", " + "{:.2f}".format(self.z) + ")"
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)
        else:
            return False