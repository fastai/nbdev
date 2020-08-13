__version__ = "0.2.38"

from fastcore.utils import IN_IPYTHON

if IN_IPYTHON:
    from .flags import *
    from .showdoc import show_doc
    #from .export import notebook2script
