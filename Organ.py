class Organ:

    def __init__(self, name, id, coverage, radius, health=100):
        self.name = name
        self.id = id
        self.length = length
        self.coverage = coverage
        self.radius = radius
        self.health = health
        
    def setHealth(self, heath):
        self.heath = heath
    
    def getHealth(self, heath):
        return self.health
        
    def OrganCellCount(self):
        cellCount = 0
        for node in coverage:
            cellCount += node.cellCount()
        return cellCount
        
    def OrganBacteriaCount(self):
        bacteriaCount = 0
        for node in coverage:
            bacteriaCount += node.bacteriaCount()
        return bacteriaCount
        
    def __repr__(self):
        return "Organ: " + self.name + "\n" \
            + "    id: " + str(self.id) + " coverage: " + str(self.coverage) + " \n" \
            + "    radius: " + self.radius + " radius: " + str(radius.end) + "\n" \ 
            + "    health: " + self.health + "\n" \
