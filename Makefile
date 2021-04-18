install:
	poetry install

build:
	poetry build

package-install:
	pip install --user dist/*.whl

package-uninstall-0.1.0:
	pip uninstall dist/hexlet_code-0.1.0-py3-none-any.whl

lint:
	poetry run flake8 gendiff

gendiff:
	poetry run gendiff

tests:
	poetry run pytest tests/tests.py

coverage:
	poetry run pytest --cov=gendiff --cov-report xml tests/tests.py

coverage-report:
	coverage report

.PHONY: gendiff gendiff tests
