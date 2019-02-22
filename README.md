# Job Search Aggregator [![CircleCI](https://circleci.com/gh/reaper47/job-search-aggregator.svg?style=svg)](https://circleci.com/gh/reaper47/job-search-aggregator) ![ScreenShot](https://github.com/reaper47/job-search-aggregator/blob/master/tests/.caverage.svg)

Collect current job posts from various companies around the world.

## Background

The goal of this project is to collect and display job offerings from various websites. The hexagonal software architecture is used. Test-driven-development practices are applied to ensure development quality.

The project consists of three layers: the domain, the application and the infrastructure. The domain layer consists of all business logic related to scraping individual websites. The application layer consists of a job service whose purpose is to interact with the database. A second service is responsible for scraping websites and pushing the jobs into the database. The infrastructure layer consists of a GUI and a repository. The GUI is developed with PySide2 considering the license is LGPL. It shows a list view of all jobs in the database. When a user selects a job, the corresponding information is displayed. The repository consists of the SQLAlchemy ORM with an SQLite backend.

Continuous integration with CircleCI has been set up. A build badge is displayed on the GitHub page every time a build finished running. Also, a badge indicating the percentage of the code covered by tests is shown. Finally, testing Python code is done with pytest.

## The GUI

The graphical user interface is built with PySide2. It consists of a scrollable list to the left and an information panel to the right. Each item in the scrollable lists shows a job's title, company and work location. Detailed information on the job post is shown in the information panel when the user selects an item. Furthermore, the user can interact with the map.

![ScreenShot](/job_search/interface/assets/img/the_gui.png)

## Installation (Linux)

1. `git clone https://github.com/reaper47/job-search-aggregator.git`
1. `cd job-search-aggregator/`
1. `python3 -m venv ../job_search` -> create a virtual environment
1. `. ../job_search/bin/activate` -> activate the virtual environment
1. `make install`
1. `python3 example_scraping.py` -> populate the database
1. `make run` -> run the GUI application

## Other Commands

- `make test` -> run all tests
- `make coverage` -> generate the coverage files under /htmlcov/index.html
- `make lint` -> lint all Python files with Flake8
- `make clean` -> remove all the junk
