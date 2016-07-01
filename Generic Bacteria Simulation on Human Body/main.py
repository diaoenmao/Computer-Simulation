from parameters import *
from oscillator import *
import initialize
import draw
from globals import *
from AbstractBacteriaCellCluster import *
from AbstractHost import *
from heapq import heappush, heappop
from time import sleep
import threading
import webbrowser
from SocketServerProtocol import *
from autobahn.twisted.websocket import WebSocketServerFactory
import sys
from twisted.python import log
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.static import File
from autobahn.twisted.resource import WebSocketResource

#dfs
def timestep(o):
    assert(o is not None)
    assert(isinstance(o, AbstractHost))
    children = o.getChildren()
    o.timeStep()
    if children is not None:
        for child in children:
            timestep(child)

def simulate():
    if parameters.verbose:
        print("Starting simulation")
    while(True):
        if SocketServerProtocol.connection is not None:
            s = "Test"
            payload = s.encode('utf8')
            SocketServerProtocol.connection.sendMessage(payload, False)
            print("sending message")
        else:
            print("Protocol is none")

        assert(objects[0].id == 1)
        head = objects[0]
        initialVelocity = oscillator.getVelocity()
        #Get bacteria,
        while len(globals.terminalOutputEvent) > 0 and globals.terminalOutputEvent[0][0] <= globals.time:
            (time, cluster) = heappop(globals.terminalOutputEvent)
            assert(isinstance(cluster, AbstractCellCluster))
            if isinstance(cluster, AbstractBacteriaCellCluster):
                head.enterBacteriaCluster(cluster)
            elif isinstance(cluster, AbstractImmuneCellCluster):
                head.enterImmuneCellCluster(cluster)
        flow = oscillator.getVolume()
        actualFlow = head.setFlow(flow)
        oscillator.setlastVolume(actualFlow)
        head._velocity = initialVelocity
        timestep(head)
        
        if parameters.verbose:
            for id, cluster in parameters.bacteria_t0.items():
                if cluster.host is None:
                    print("cluster id", id, "not in host")
                else:
                    print("cluster id ", id, "in", cluster.host.id)
        
        sleep(1)
        globals.time += 1

def serve():
    log.startLogging(sys.stdout)

    factory = WebSocketServerFactory(u"ws://127.0.0.1:8080")
    factory.protocol = SocketServerProtocol

    resource = WebSocketResource(factory)
    root = File("server")
    root.putChild(b"ws", resource)

    site = Site(root)
    reactor.listenTCP(8080, site)

    reactor.run()

blood_vessels = initialize.processInput(parameters.blood_vessel_file)
organs = initialize.processInput(parameters.organ_file)
objects = initialize.buildGraph(blood_vessels, organs)

#insert bacteria clusters
for id, cluster in parameters.bacteria_t0.items():
    id = int(id)
    assert(isinstance(cluster, AbstractBacteriaCellCluster))
    objects[id].enterBacteriaCluster(cluster)

for id, cluster in parameters.immune_t0.items():
    id = int(id)
    assert(isinstance(cluster, AbstractImmuneCellCluster))
    objects[id].enterImmuneCellCluster(cluster)

globals.objects = objects
threading.Thread(target=simulate).start()
webbrowser.open('http://127.0.0.1:8080/')
serve()


