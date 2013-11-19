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
        if self.factory.get_new_match():
            base_port = self.factory.get_base_port()
            self.transport.write('{"Tx" :%i, "Rx": %i}' % (base_port,
                                                           base_port + 1))
            self.factory.toggle_new_match()
            self.transport.loseConnection()
            reactor.listenTCP(base_port, PubFactory())
            reactor.listenTCP(base_port + 1, PubFactory())
        else:
            base_port = self.factory.get_base_port()
            self.transport.write('{"Tx" :%i, "Rx": %i}' % (base_port + 1,
                                                           base_port))
            self.factory.inc_base_port()
            self.factory.toggle_new_match()
            self.transport.loseConnection()


class MatchFactory(protocol.ServerFactory):

    def __init__(self):
        self.base_port = 6000
        self.new_match = True

    protocol = MatchProtocol

    def get_base_port(self):
        return self.base_port

    def inc_base_port(self):
        self.base_port += 2

    def get_new_match(self):
        return self.new_match

    def toggle_new_match(self):
        if self.new_match:
            self.new_match = False
        else:
            self.new_match = True


if __name__ == '__main__':
    arguments = docopt(__doc__)
    reactor.listenTCP(int(arguments['--port']), MatchFactory())
    reactor.run()