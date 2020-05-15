__version__ = "0.2.19"

from .imports import IN_IPYTHON

if IN_IPYTHON:
    from .flags import *
    from .showdoc import show_doc
    from .export import notebook2script