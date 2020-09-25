__version__ = "1.1.0"

from fastcore.imports import IN_IPYTHON
from .imports import *

if IN_IPYTHON:
    from .flags import *
    from .showdoc import show_doc
