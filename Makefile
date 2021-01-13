install:
	poetry install

build:
	poetry build

package-install:
	pip install --user dist/*.whl

lint:
	poetry run flake8 gendiff

gendiff:
	poetry run gendiff

.PHONY: all test clean
