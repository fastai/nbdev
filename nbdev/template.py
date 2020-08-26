makefile_tmpl = """.ONESHELL:
SHELL := /bin/bash
SRC = $(wildcard {nbs_path}/*.ipynb)

all: {lib_name} docs

{lib_name}: $(SRC)
	nbdev_build_lib
	touch {lib_name}

sync:
	nbdev_update_lib

docs_serve: docs
	cd docs && bundle exec jekyll serve

docs: $(SRC)
	nbdev_build_docs
	touch docs

test:
	nbdev_test_nbs

release: pypi
	nbdev_conda_package
	nbdev_bump_version

pypi: dist
	twine upload --repository pypi dist/*

dist: clean
	python setup.py sdist bdist_wheel

clean:
	rm -rf dist"""

topnav_tmpl = """topnav:
- title: Topnav
  items:
    - title: {host}
      external_url: {git_url}

#Topnav dropdowns
topnav_dropdowns:
- title: Topnav dropdowns
  folders:"""

config_tmpl = """repository: {user}/{lib_name}
output: web
topnav_title: {title}
site_title: {title}
company_name: {copyright}
description: {description}
# Set to false to disable KaTeX math
use_math: true
# Add Google analytics id if you have one and want to use it here
google_analytics:
# See http://nbdev.fast.ai/search for help with adding Search
google_search:

host: 127.0.0.1
# the preview server used. Leave as is.
port: 4000
# the port where the preview is rendered.

exclude:
  - .idea/
  - .gitignore
  - vendor
 
exclude: [vendor]

highlighter: rouge
markdown: kramdown
kramdown:
 input: GFM
 auto_ids: true
 hard_wrap: false
 syntax_highlighter: rouge

collections:
  tooltips:
    output: false

defaults:
  -
    scope:
      path: ""
      type: "pages"
    values:
      layout: "page"
      comments: true
      search: true
      sidebar: home_sidebar
      topnav: topnav
  -
    scope:
      path: ""
      type: "tooltips"
    values:
      layout: "page"
      comments: true
      search: true
      tooltip: true

sidebars:
- home_sidebar

theme: jekyll-theme-cayman"""

