__all__ = ['on_test_nb_begin', 'on_test_nb_end', 'on_doc_nb_begin', 'on_doc_nb_preprocess_end', 'on_doc_nb_end']

def on_test_nb_begin(nb, file_name, flags):
    "Called before testing a notebook. Return the notebook to be tested"
    return nb

def on_test_nb_end(file_name):
    "Called after testing a notebook"
    pass

def on_doc_nb_begin(nb, file_name, output_type):
    "Called before converting a notebook to documentation. Return the notebook to be converted"
    return nb

def on_doc_nb_preprocess_end(nb, file_name, output_type):
    "Called after pre-processing a notebook, before converting to documentation. Return the notebook to be converted"
    return nb

def on_doc_nb_end(file_name, output_type):
    "Called after converting a notebook to documentation"
    pass