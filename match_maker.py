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
        self.factory.push_to_queue(self)


class MatchFactory(protocol.ServerFactory):

    def __init__(self):
        self.base_port = 6000
        self.new_match = True
        self.match_queue = []

    def get_base_port(self):
        return self.base_port

    def inc_base_port(self):
        self.base_port += 2

    def get_new_match(self):
        return self.new_match
1
    def push_to_queue(self, protocol):
        self.match_queue.append(protocol)
        if len(self.match_queue) > 1:
            player0 = self.match_queue.pop()
            player1 = self.match_queue.pop()

            player0.transport.write('{"Tx" :%i, "Rx": %i}' % (self.base_port,
                                                              self.base_port + 1))
            player1.transport.write('{"Tx" :%i, "Rx": %i}' % (self.base_port + 1,
                                                              self.base_port))
            self.inc_base_port()
            reactor.listenTCP(self.base_port, PubFactory())
            reactor.listenTCP(self.base_port + 1, PubFactory())
            player0.transport.loseConnection()
            player1.transport.loseConnection()


    protocol = MatchProtocol


if __name__ == '__main__':
    arguments = docopt(__doc__)
    reactor.listenTCP(int(arguments['--port']), MatchFactory())
    reactor.run()