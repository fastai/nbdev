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
	cd docusaurus && npm run start

docs: $(SRC)
	./mk_docs.sh
	
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
