help:
	cat Makefile

docs: .FORCE
	npm run start

nb: .FORCE
	jupyter lab

build: .FORCE
	yarn run build

install: .FORCE
	npm install -g npm@">=8.4.1"
	npm install --global yarn
	yarn install --frozen-lockfile
	pip install -Ur requirements.txt
	jupyter labextension install @jupyterlab/vega5-extension

.FORCE:
