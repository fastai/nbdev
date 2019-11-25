docs: $(wildcard nbs/*.ipynb)
	nbdev_build_docs

pypi: dist
	twine upload --repository pypi dist/*

dist: clean
	python setup.py sdist bdist_wheel

clean:
	rm -rf dist

