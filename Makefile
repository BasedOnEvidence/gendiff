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

tests:
	poetry run pytest --cov=gendiff --cov-report xml tests/tests.py

coverage:
	poetry run pytest --cov=gendiff --cov-report xml tests/tests.py

coverage-report:
	coverage report

.PHONY: gendiff gendiff tests
