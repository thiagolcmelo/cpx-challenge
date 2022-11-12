.DEFAULT_GOAL := build

build:
	python3 setup.py build
.PHONY:build

install:
	python3 setup.py install
.PHONY:install

test:
	black .
	coverage run -m pytest
	coverage report -m
.PHONY:test