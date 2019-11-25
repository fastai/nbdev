# Welcome to nbdev




`nbdev` is a library that allows you to fully develop a library in [jupyter notebooks](https://jupyter.org/), putting all your code, tests and documentation in one place. Using the interactive enviromnent, you can easily debug and refactor your code. By simply adding `#export` flags to the cells that define the functions you want to keep, you can then convert your notebook in a standard python module with just one command in the console or one line of code at the end of your notebook:

![An exported cell](nbs/images/export_example.png)

Here the function `add_init` is defined in the first cell (marked with the export flag) and tested in the second cell. In the last cell of your notebook, you can then run:
<div class="codecell" markdown="1">
<div class="input_area" markdown="1">

```python
from nbdev.export import *
notebook2script()
```

</div>
<div class="output_area" markdown="1">

    Converted 00_export.ipynb.
    Converted 01_sync.ipynb.
    Converted 02_showdoc.ipynb.
    Converted 03_export2html.ipynb.
    Converted 04_test.ipynb.
    Converted 05_cli.ipynb.
    Converted 99_index.ipynb.


</div>

</div>

Or in the command line, you can run:
``` bash
nbdev_build_lib
```
as long as you are somewhere in the folder where you are developing your library.

Since you are in a notebook, you can also add text, links or images that will be kept along with the tests when you generate the documentation of your library. The cells where your code is defined will be hidden and replaced by a satandard documentation of your function, showing its name, arguments, docstring, and link to the source code on github. For instance, the cells before are converted to:

![doc example](nbs/images/doc_example.png)

In the other pages of the documentation, you can get more details about:
- the [export](http://nbdev.fast.ai/export.html) functionality from jupyter noteboks to a python library
- the [cli](http://nbdev.fast.ai/cli.html) commands you can use with nbdev in a terminal
- how [export2html](http://nbdev.fast.ai/export2html.html) buils a documentation for your libary
- how [sync](http://nbdev.fast.ai/sync.html) can allow you to export back form the pyhton modules to the jupyter notebook
- how [test](http://nbdev.fast.ai/test.html) put in your notebooks can be run in parallel to export a CI from your notebooks

## Installing

nbdev is is on PyPI so you can just run
``` 
pip install nbdev
```
For a developer install, use the following
```
git clone https://github.com/fastai/nbdev
cd nbdev
pip install -e .
```

## Contributing

If you want to contribute to `nbdev`, be sure to review the [contributions guidelines](https://github.com/fastai/nbdev/blob/master/CONTRIBUTING.md). This project adheres to fastai`s [code of conduct](https://github.com/fastai/nbdev/blob/master/CODE-OF-CONDUCT.md). By participating, you are expected to uphold this code. In general, the fastai project strives to abide by generally accepted best practices in open-source software development.

Make sure you have the git hooks we use installed by running
```
nbdev_install_git_hooks
```
in the cloned repository folder. 

## Copyright

Copyright 2019 onwards, fast.ai, Inc. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this project's files except in compliance with the License. A copy of the License is provided in the LICENSE file in this repository.
