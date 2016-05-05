class Sequence:
    def __init__(self, prefix):
        self._id = 0
        self._prefix = prefix
    def getNextVal(self):
        self._id += 1
        return self._id
    def reset():
        self._id = 0

bacteriaClusterSq = Sequence("B_")
immuneCellClusterSq = Sequence("I_")
