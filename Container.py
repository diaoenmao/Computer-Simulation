class Container:
    def __init__(self):
        self.bacteriaClusters = []
        self.immuneCellClusters = [] 
    
    def interact(self):
        if not self.bacteriaClusters and not self.immuneCellClusters
            for bacteriaCluster1 in bacteriaClusters:
                for bacteriaCluster2 in bacteriaClusters:
                    bacteriaCluster1.inContact(bacteriaCluster2)
                    bacteriaCluster2.inContact(bacteriaCluster1)
            for immuneCellCluster1 in immuneCellClusters:
                for immuneCellCluster2 in immuneCellClusters:
                    immuneCellCluster1.inContact(immuneCellCluster2)
                    immuneCellCluster2.inContact(immuneCellCluster1)
            for bacteriaCluster in bacteriaClusters:
                for immuneCellCluster in immuneCellClusters:
                    bacteriaCluster.inContact(cluster)
                    immuneCellCluster.inContact(bacteriaCluster)