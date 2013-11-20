STARTING_PORT = 6000

# attempt to import production settings, so they can overwrite dev options
try:
    from .local_settings import *
except ImportError:
    pass
