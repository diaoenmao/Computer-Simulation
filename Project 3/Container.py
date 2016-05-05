class Container:
    def __init__(self):
        self.bacteriaClusters = []
        self.immuneCellClusters = [] 
    
    def getBacteriaClusters(self):
        return self.bacteriaClusters
    
    def getBacteriaClustersConcentration(self):
        return len(self.bacteriaClusters)
        
    def addBacteriaCluster(self, cluster):
        self.bacteriaClusters.append(cluster)
    
    def removeBacteriaCluster(self, cluster):
        self.bacteriaClusters.remove(cluster)
        
    def getImmuneCellClusters(self):
        return self.immuneCellClusters
        
    def getImmuneCellClustersConcentration(self):
        return len(self.immuneCellClusters)
        
    def addImmuneCellCluster(self, cluster):
        self.immuneCellClusters.append(cluster)

    def removeImmuneCellCluster(self, cluster):
        self.immuneCellClusters.remove(cluster)