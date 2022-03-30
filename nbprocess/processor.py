#export
from functools import wraps
from nbconvert.preprocessors import Preprocessor
from nbconvert import MarkdownExporter
from nbconvert.preprocessors import TagRemovePreprocessor
from nbprocess.extract_attachments import ExtractAttachmentsPreprocessor
from nbconvert.writers import FilesWriter

def preprocess_cell(func):
    @wraps(func, updated=())
    class _C(Preprocessor):
        def preprocess_cell(self, cell, resources, index):
            res = func(cell)
            if res: cell = res
            return cell, resources
    return _C

def preprocess(func):
    @wraps(func, updated=())
    class _C(Preprocessor):
        def preprocess(self, nb, resources):
            res = func(nb)
            if res: nb = res
            nb.cells = list(nb.cells)
            return nb, resources
    return _C

