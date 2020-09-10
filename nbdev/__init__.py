__version__ = "1.0.16"

from fastcore.imports import IN_IPYTHON
from .imports import *

if IN_IPYTHON:
    from .flags import *
    from .showdoc import show_doc
    from .export import notebook2script
