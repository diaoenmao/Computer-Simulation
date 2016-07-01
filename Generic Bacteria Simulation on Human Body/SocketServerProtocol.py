from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory


class SocketServerProtocol(WebSocketServerProtocol):
    connection = None
    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")
        SocketServerProtocol.connection = self
        print(SocketServerProtocol.connection)


    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))

