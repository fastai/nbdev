makefile_tmpl = """SRC = $(wildcard {nbs_path}/*.ipynb)

all: {lib_name} docs

{lib_name}: $(SRC)
	nbdev_build_lib
	touch {lib_name}

docs: $(SRC)
	nbdev_build_docs
	touch docs

test
	nbdev_test_nbs

pypi: dist
	twine upload --repository pypi dist/*

dist: clean
	python setup.py sdist bdist_wheel

clean:
	rm -rf dist"""

topnav_tmpl = """topnav:
- title: Topnav
  items:
    - title: GitHub
      external_url: https://github.com/{user}/{lib_name}

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
# Add Google analytics id if you have one and want to use it here
google_analytics:
# See Search docs on nbdev.fast.ai for help with adding Search
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

