
[![CI](https://github.com/fastai/nbprocess/actions/workflows/test.yaml/badge.svg)](https://github.com/fastai/nbprocess/actions/workflows/test.yaml)
[![Deploy to GitHub
Pages](https://github.com/fastai/nbprocess/actions/workflows/deploy.yaml/badge.svg)](https://github.com/fastai/nbprocess/actions/workflows/deploy.yaml)

# nbprocess

> Process and export Jupyter Notebooks fast

This will become v2 of nbdev in the near-ish future.

## Install

With pip:

    pip install nbprocess

With conda:

    conda install -c fastai nbprocess

## How to use

By default docs are exported for use with [Quarto](https://quarto.org/).
To install Quarto on Ubuntu, run `make install`. See the Quarto docs for
other platforms.

The following CLI tools are provided:

-   `nbprocess_create_config`: Create `settings.ini` skeleton
-   `nbprocess_export`: Export notebooks to Python modules
-   `nbprocess_update`: Update Python modules from a notebook
-   `nbprocess_fix`: Fix merge conflicts in notebooks
-   `nbprocess_filter`: A filter for Quarto
-   `nbprocess_quarto`: Create Quarto web site
-   `nbprocess_new`: Create a new `nbprocess` project
-   `nbprocess_migrate_directives`: helps you migrate all your
    directives from nbdev v1 to v2.
