__all__ = ['begin_test_nb', 'after_test_nb', 'begin_doc_nb', 'after_doc_nb_preprocess', 'after_doc_nb']

def begin_test_nb(nb, file_name, flags):
    "Called before testing a notebook. Return the notebook to be tested"
    return nb

def after_test_nb(file_name):
    "Called after testing a notebook"
    pass

def begin_doc_nb(nb, file_name, output_type):
    "Called before converting a notebook to documentation. Return the notebook to be converted"
    return nb

def after_doc_nb_preprocess(nb, file_name, output_type):
    "Called after pre-processing a notebook, before converting to documentation. Return the notebook to be converted"
    return nb

def after_doc_nb(file_name, output_type):
    "Called after converting a notebook to documentation"
    pass