# from twisted.internet import reactor
# from twisted.internet.protocol import Factory, Protocol
# from twisted.internet.endpoints import TCP4ClientEndpoint
#
# class KommProtocol(Protocol):
#     def dataReceived(self, data):
#         stdout.write(data)
#
#
# class KommFactory(ClientFactory):
#     def startedConnecting(self, connector):
#         print 'Started to connect.'
#
#     def buildProtocol(self, addr):
#         print 'Connected.'
#         return Echo()
#
#     def clientConnectionLost(self, connector, reason):
#         print 'Lost connection.  Reason:', reason
#
#     def clientConnectionFailed(self, connector, reason):
#         print 'Connection failed. Reason:', reason
#
#
# from twisted.internet import reactor, protocol
# from twisted.protocols import basic
# from twisted.internet.protocol import Factory, Protocol
# from twisted.internet.endpoints import TCP4ClientEndpoint
# from PubSubServer.GetKommPorts import GetKommPorts
# from PubSubServer.config import HOST, PORT
# from json import loads
#
#
# class KommProtocol(basic.LineReceiver):
#
#     def __init__(self, _callback_fucnt):
#         self.ports_have_been_setup = False
#         self.callback_funct = _callback_fucnt
#
#     def dataReceived(self, data):
#         #self.callback_funct(data)
#         print data
#
#     def connectionMade(self):
#         self.factory.clients.add(self)
#         print 'Connection Made'
#
#     def sendMessage(self, msg):
#         self.transport.write(msg)
#
#     def connectionLost(self, reason):
#         pass
#
#
# class KommFactory(Protocol):
#     def __init__(self, _callback_funct):
#         self.callback_funct = _callback_funct
#         self.clients = set()
#
#     protocol = KommProtocol
#
#
# kp = GetKommPorts()
# kp.connect(HOST, PORT)
# raw_json_ports = kp.myreceive()
# komm_ports = loads(raw_json_ports)
#
#
# lPort0 = TCP4ClientEndpoint(reactor, 'localhost', 6000)
# d = lPort0.connect(KommFactory('recieve_callback_funct'))
# # lPort1 =  TCP4ClientEndpoint(reactor, HOST, komm_ports['Rx'])
# # e = lPort1.connect(KommFactory('recieve_callback_funct'))
# reactor.run()

from twisted.internet.protocol import Protocol, ClientFactory
from sys import stdout


class Echo(Protocol):
    def dataReceived(self, data):
        stdout.write(data)

    def connectionMade(self):
        print "connection made"
        self.transport.write("bbbbbbb")


class EchoClientFactory(ClientFactory):
    def startedConnecting(self, connector):
        print 'Started to connect.'

    def buildProtocol(self, addr):
        print 'Connected.'
        return Echo()


    def clientConnectionLost(self, connector, reason):
        print 'Lost connection.  Reason:', reason

    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed. Reason:', reason

from twisted.internet import reactor
reactor.connectTCP('localhost', 6000, EchoClientFactory())
reactor.run()