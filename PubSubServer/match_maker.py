from twisted.internet import protocol, reactor
from twisted.protocols import basic
from PubSubServer.kommunication_server import PubFactory
from PubSubServer.config import STARTING_PORT


class MatchProtocol(basic.LineReceiver):

    def connectionMade(self):
        self.factory.clients.add(self)
        self.factory.attempt_to_make_a_match()

    # def connectionLost(self, reason):
    #     self.factory.clients.remove(self)


class MatchFactory(protocol.ServerFactory):

    def __init__(self):
        self.clients = set()
        self.base_port = STARTING_PORT

    def inc_base_port(self):
        self.base_port += 2

    def attempt_to_make_a_match(self):
        if len(self.clients) > 1:
            # remove the top two clients for pairing
            player0 = self.clients.pop()
            player1 = self.clients.pop()

            # spin up the rooms on the ports
            reactor.listenTCP(self.base_port, PubFactory())
            reactor.listenTCP(self.base_port + 1, PubFactory())

            # give the clients their port numbers.
            player0.transport.write('{"Tx" :%i, "Rx": %i}' % (self.base_port,
                                                              self.base_port + 1))
            player1.transport.write('{"Tx" :%i, "Rx": %i}' % (self.base_port + 1,
                                                              self.base_port))
            # ready the next set of ports.
            self.inc_base_port()

            # close the connections letting the clients know they are paired and ready to go.
            player0.transport.loseConnection()
            player1.transport.loseConnection()

    protocol = MatchProtocol