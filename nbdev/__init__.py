__version__ = "0.2.18"

from .imports import IN_IPYTHON

if IN_IPYTHON:
    from .flags import *