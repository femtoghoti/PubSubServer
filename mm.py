"""Match Maker (MM) is a simple program generates channels and distributes
   This server simply spawns instances of the kommunication_server and then
   gives the ip and port to the client for the two connections.

Usage:
 match_maker.py [--port=<port>]

Options:
  -h --help      Show this screen.
  --port=<port>  HTTP port [default: 5150].
"""

from docopt import docopt
from twisted.internet import reactor
from PubSubServer.match_maker import MatchFactory

if __name__ == '__main__':
    arguments = docopt(__doc__)
    reactor.listenTCP(int(arguments['--port']), MatchFactory())
    reactor.run()