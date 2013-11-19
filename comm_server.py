"""simple communication server

Usage:
 kommunication_server.py [--port=<port>]

Options:
  -h --help      Show this screen.
  --port=<port>  HTTP port [default: 5000].
"""

from docopt import docopt
from twisted.internet import reactor
from PubSubServer.kommunication_server import PubFactory

if __name__ == '__main__':
    arguments = docopt(__doc__)
    reactor.listenTCP(int(arguments['--port']), PubFactory())
    reactor.run()