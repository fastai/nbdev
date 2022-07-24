""" A preprocessor that extracts all of the attachments from the notebook file.
The extracted attachments are returned in the 'resources' dictionary.

Based on the ExtractOutputsProcessor in nbconvert... the license for nbconvert is:

# Licensing terms

This project is licensed under the terms of the Modified BSD License
(also known as New or Revised or 3-Clause BSD), as follows:

- Copyright (c) 2001-2015, IPython Development Team
- Copyright (c) 2015-, Jupyter Development Team

All rights reserved. """

import sys,os
from binascii import a2b_base64
from traitlets import Unicode, Set
from nbconvert.preprocessors.base import Preprocessor

class ExtractAttachmentsPreprocessor(Preprocessor):
    "Extracts all of the outputs from the notebook file."
    output_filename_template = Unicode( "attach_{cell_index}_{name}").tag(config=True)
    extract_output_types = Set( {'image/png', 'image/jpeg', 'image/svg+xml', 'application/pdf'}).tag(config=True)

    def preprocess_cell(self, cell, resources, cell_index):
        output_files_dir = resources.get('output_files_dir', None)
        if not isinstance(resources['outputs'], dict): resources['outputs'] = {}

        for name, attach in cell.get("attachments", {}).items():
            for mime, data in attach.items():
                if mime not in self.extract_output_types: continue
                # Binary files are base64-encoded, SVG is already XML
                if mime in {'image/png', 'image/jpeg', 'application/pdf'}: data = a2b_base64(data)
                elif sys.platform == 'win32': data = data.replace('\n', '\r\n').encode("UTF-8")
                else: data = data.encode("UTF-8")
                filename = self.output_filename_template.format( cell_index=cell_index, name=name)
                if output_files_dir is not None: filename = os.path.join(output_files_dir, filename)
                if name.endswith(".gif") and mime == "image/png": filename = filename.replace(".gif", ".png")
                resources['outputs'][filename] = data
                attach_str = "attachment:"+name
                if attach_str in cell.source: cell.source = cell.source.replace(attach_str, filename)

        return cell, resources

