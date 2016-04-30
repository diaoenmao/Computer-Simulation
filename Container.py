class Container:
    def __init__(self):
        self.bacteriaClusters = []
        self.immuneCellClusters = [] 
    
    def getBacteriaClusters():
        return self.bacteriaClusters
    
    def getBacteriaClustersConcentration():
        return len(self.bacteriaClusters)
        
    def addBacteriaCluster(cluster):
        self.bacteriaClusters.append(cluster)
    
    def removeBacteriaCluster(cluster):
        self.bacteriaClusters.remove(cluster)
        
    def getImmuneCellClusters():
        return self.immuneCellClusters
        
    def getImmuneCellClustersConcentration():
        return len(self.immuneCellClusters)
        
    def addImmuneCellCluster(cluster):
        self.immuneCellClusters.append(cluster)

    def removeImmuneCellCluster(cluster):
        self.immuneCellClusters.remove(cluster)