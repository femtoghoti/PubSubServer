STARTING_PORT = 6000
MAX_MESSAGE_LENGTH = 128
HOST = 'localhost'
PORT = 5150

# attempt to import production settings, so they can overwrite dev options
try:
    from .local_settings import *
except ImportError:
    pass
