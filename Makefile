.ONESHELL:
SHELL := /bin/bash
SRC = $(wildcard nbs/*.ipynb)

all: nbprocess docs

nbprocess: $(SRC)
	nbprocess_export
	touch nbprocess

sync:
	nbdev_update_lib

docs_serve:
	cd docusaurus
	npm run start

docs: docusaurus
	cd docusaurus/
	npm run build
	cd ..
	rm -rf docs
	mv docusaurus/build docs
	cp docs_src/CNAME docs/

.PHONY: docusaurus
docusaurus:
	nbprocess_docs --path nbs --dest docusaurus/docs

test:
	nbdev_test_nbs

release: pypi conda_release
	nbdev_bump_version

conda_release:
	fastrelease_conda_package

pypi: dist
	twine upload --repository pypi dist/*

dist: clean
	python setup.py sdist bdist_wheel

clean:
	rm -rf dist

install-docs:
	cd docusaurus
	npm install -g npm@">=8.4.1"
	npm install package-lock.json

install: install-docs
	pip install .

