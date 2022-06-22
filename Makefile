.ONESHELL:
SHELL := /bin/bash
SRC = $(wildcard nbs/*.ipynb)

nbprocess: $(SRC)
	nbprocess_export
	touch nbprocess

sync:
	nbprocess_update

deploy: docs
	nbprocess_ghp_deploy

preview: ## Live preview quarto docs with hot reloading.
	nbprocess_sidebar
	nbprocess_export
	IN_TEST=1 &&  nbprocess_quarto --preview

prepare: ## Export notebooks to python modules, test code and clean notebooks.
	nbprocess_export
	nbprocess_test
	nbprocess_clean

docs: .install
	nbprocess_export
	nbprocess_quarto

test:
	nbprocess_test

release: pypi conda_release
	nbprocess_bump_version

conda_release:
	fastrelease_conda_package

pypi: dist
	twine upload --repository pypi dist/*

dist: clean
	python setup.py sdist bdist_wheel

clean:
	rm -rf dist

.install: install_quarto
	pip install -e .[dev]
	touch .install

install_quarto:
	./install_quarto.sh

.FORCE:

