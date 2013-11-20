"""simple match making server server
   This server simply spawns instances of the kommunication_server and then
   gives the ip and port to the client for the two connections.

Usage:
 match_maker.py [--port=<port>]

Options:
  -h --help      Show this screen.
  --port=<port>  HTTP port [default: 5150].
"""

from docopt import docopt
from twisted.internet import protocol, reactor
from twisted.protocols import basic
from PubSubServer.kommunication_server import PubFactory


class MatchProtocol(basic.LineReceiver):

    def connectionMade(self):
        self.factory.clients.add(self)
        self.factory.attempt_to_make_a_match()

    def connectionLost(self, reason):
        self.factory.clients.remove(self)


class MatchFactory(protocol.ServerFactory):

    def __init__(self):
        self.clients = set()
        self.base_port = 6000
        self.new_match = True
        self.match_queue = []

    def get_base_port(self):
        return self.base_port

    def inc_base_port(self):
        self.base_port += 2

    def get_new_match(self):
        return self.new_match

    def attempt_to_make_a_match(self):
        if len(self.clients) > 1:
            # remove the top two clients for pairing
            player0 = self.clients.pop()
            player1 = self.clients.pop()

            # give the clients their port numbers.
            player0.transport.write('{"Tx" :%i, "Rx": %i}' % (self.base_port,
                                                              self.base_port + 1))
            player1.transport.write('{"Tx" :%i, "Rx": %i}' % (self.base_port + 1,
                                                              self.base_port))
            # spin up the rooms on the above ports
            reactor.listenTCP(self.base_port, PubFactory())
            reactor.listenTCP(self.base_port + 1, PubFactory())

            # ready the next set of ports.
            self.inc_base_port()

            # close the connections letting the clients know they are paired and ready to go.
            player0.transport.loseConnection()
            player1.transport.loseConnection()

    protocol = MatchProtocol


if __name__ == '__main__':
    arguments = docopt(__doc__)
    reactor.listenTCP(int(arguments['--port']), MatchFactory())
    reactor.run()