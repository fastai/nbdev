""" A preprocessor that extracts all of the attachments from the notebook file.
The extracted attachments are returned in the 'resources' dictionary.

Based on the ExtractOutputsProcessor in nbconvert... the license for
nbconvert is

# Licensing terms

This project is licensed under the terms of the Modified BSD License
(also known as New or Revised or 3-Clause BSD), as follows:

- Copyright (c) 2001-2015, IPython Development Team
- Copyright (c) 2015-, Jupyter Development Team

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.

Redistributions in binary form must reproduce the above copyright notice, this
list of conditions and the following disclaimer in the documentation and/or
other materials provided with the distribution.

Neither the name of the Jupyter Development Team nor the names of its
contributors may be used to endorse or promote products derived from this
software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

## About the Jupyter Development Team

The Jupyter Development Team is the set of all contributors to the Jupyter project.
This includes all of the Jupyter subprojects.

The core team that coordinates development on GitHub can be found here:
https://github.com/jupyter/.

## Our Copyright Policy

Jupyter uses a shared copyright model. Each contributor maintains copyright
over their contributions to Jupyter. But, it is important to note that these
contributions are typically only changes to the repositories. Thus, the Jupyter
source code, in its entirety is not the copyright of any single person or
institution.  Instead, it is the collective copyright of the entire Jupyter
Development Team.  If individual contributors want to maintain a record of what
changes/contributions they have specific copyright on, they should indicate
their copyright in the commit message of the change, when they commit the
change to one of the Jupyter repositories.

With this in mind, the following banner should be used in any source code file
to indicate the copyright and license terms:

    # Copyright (c) Jupyter Development Team.
    # Distributed under the terms of the Modified BSD License.
"""

from binascii import a2b_base64
import sys
import os

from traitlets import Unicode, Set
from nbconvert.preprocessors.base import Preprocessor

class ExtractAttachmentsPreprocessor(Preprocessor):
    """
    Extracts all of the outputs from the notebook file.  The extracted
    outputs are returned in the 'resources' dictionary.
    """

    output_filename_template = Unicode( "attach_{cell_index}_{name}").tag(config=True)
    extract_output_types = Set( {'image/png', 'image/jpeg', 'image/svg+xml', 'application/pdf'}).tag(config=True)

    def preprocess_cell(self, cell, resources, cell_index):
        """
        Apply a transformation on each cell,

        Parameters
        ----------
        cell : NotebookNode cell
            Notebook cell being processed
        resources : dictionary
            Additional resources used in the conversion process.  Allows
            preprocessors to pass variables into the Jinja engine.
        cell_index : int
            Index of the cell being processed (see base.py)
        """

        output_files_dir = resources.get('output_files_dir', None)
        if not isinstance(resources['outputs'], dict): resources['outputs'] = {}

        for name, attach in cell.get("attachments", {}).items():
            for mime, data in attach.items():
                if mime not in self.extract_output_types: continue

                # Binary files are base64-encoded, SVG is already XML
                if mime in {'image/png', 'image/jpeg', 'application/pdf'}: data = a2b_base64(data)
                elif sys.platform == 'win32': data = data.replace('\n', '\r\n').encode("UTF-8")
                else: data = data.encode("UTF-8")
                filename = self.output_filename_template.format( cell_index=cell_index, name=name,)
                if output_files_dir is not None: filename = os.path.join(output_files_dir, filename)
                if name.endswith(".gif") and mime == "image/png": filename = filename.replace(".gif", ".png")
                resources['outputs'][filename] = data
                attach_str = "attachment:"+name
                if attach_str in cell.source: cell.source = cell.source.replace(attach_str, filename)

        return cell, resources
