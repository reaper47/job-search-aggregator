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

init_db:
	python3 ./job_search/repository/jobs/entities/job_entity.py

lint:
	flake8 --exclude=venv* --statistics --builtins="Job"

test:
	pytest -vv --cov=. --ignore=tests/__init__.py

coverage:
	pytest -vv --cov=. --cov-report=html
