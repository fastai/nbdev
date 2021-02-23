.ONESHELL:
SHELL := /bin/bash

SRC = $(wildcard nbs/*.ipynb)

all: nbdev docs

nbdev: $(SRC)
	nbdev_build_lib
	touch nbdev

docs_serve: docs
	cd docs && bundle exec jekyll serve

docs: $(SRC)
	nbdev_build_docs
	touch docs

test:
	nbdev_test_nbs --flags ''

release: pypi
	fastrelease_conda_package --upload_user fastai
	nbdev_bump_version

conda_release:
	fastrelease_conda_package --mambabuild --upload_user fastai

pypi: dist
	twine upload --repository pypi dist/*

dist: clean
	python setup.py sdist bdist_wheel

clean:
	rm -rf dist

