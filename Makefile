# venv created with 'uv venv --python /Users/sanjaykapoor/.pyenv/shims/python3.12'
VENV = .venv
PIP = pip
PYTHON = $(VENV)/bin/python3
SHELL = /bin/bash

.PHONY: build clean console dev deploy install prd test

build:
	./scripts/vps/vps-utils build

console:
	python

deploy:
	./scripts/vps/vps-utils deploy --host 5.161.208.47 --user root

dev: 
	. $(VENV)/bin/activate && ./bin/app-server --port 9009

install: pyproject.toml
	uv sync

prd:
	. $(VENV)/bin/activate && ./bin/app-server --port 9009

test:
	. $(VENV)/bin/activate && pytest

clean:
	rm -rf __pycache__
	rm -rf $(VENV)
