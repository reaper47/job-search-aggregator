PY = python3
PIP = pip3

clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

install:
	${PIP} install -r requirements.txt
	${PIP} install -e .
	make init_db
	make clean

init_db:
	${PY} ./job_search/repository/jobs/entities/job_entity.py

run:
	${PY} ./job_search/interface/gui/job_search_aggregator.py

run2:
	${PY} ./job_search/interface/gui/main.py

lint:
	flake8 --exclude=venv* --statistics --builtins="Job"

test:
	pytest -vv --cov=. --ignore=tests/__init__.py

coverage:
	pytest -vv --cov=. --cov-report=html
