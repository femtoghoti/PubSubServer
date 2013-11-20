"""Match Maker (MM) is a simple program generates channels and distributes them to clients.
   Once a match has been made the connection to the clients is closed.  It is on the client to
   connect to the channel and take approperate action.

Usage:
 mm.py [--port=<port>]

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