import paths # noqa
from pathlib import Path
from unittest import mock

import pytest
from helpers.stubs import RequestsStub
from python_org import PythonOrg

BASE_DIR = Path(__file__).parent
A_JOB_POSTINGS = f'{BASE_DIR}/samples/job_posting.html'
with open(A_JOB_POSTINGS) as f:
    SOME_JOBS = f.read()

with open(f'{BASE_DIR}/samples/job_post.html') as f:
    A_JOB_POST = f.read()


@pytest.fixture
def python_org():
    return PythonOrg()


@pytest.fixture
@mock.patch('python_org.requests')
def python_org_brewed(mock_requests):
    python_org = PythonOrg()
    mock_requests.get.return_value = RequestsStub(SOME_JOBS)
    python_org.prepare_soup()
    return python_org


@mock.patch('python_org.requests')
def test_givenAJobPosting_whenPreparingTheSoup_thenAllPagesShouldBeScraped(mock_requests, python_org):
    mock_requests.get.return_value = RequestsStub(SOME_JOBS)
    npages_expected = 2

    python_org.prepare_soup()

    assert npages_expected == len(python_org.pages)


@mock.patch('python_org.requests')
def test_givenABrewedPythonSoup_whenFetchingJobs_thenScrapeInfoFromAllJobs(mock_requests, python_org_brewed):
    mock_requests.get.return_value = RequestsStub(A_JOB_POST)
    a_job = {
        'title': 'Quantitative Data Engineer',
        'company': 'Tudor Investment Corporation',
        'location': 'New York, New York, United States',
        'description': 'We are looking for an outstanding engineer.',
        'restrictions': ['No telecommuting', 'No Agencies Please'],
        'requirements': ['Proficiency in Python', 'Experience in Python', 'Experience in C'],
        'about': [],
        'contact_info': {
            'contact': 'Morgan Nelson',
            'email': 'morgan.nelson@tudor.com',
            'website': 'https://boards.greenhouse.io/'
        }
    }
    jobs_expected = [a_job]*4

    jobs = python_org_brewed.fetch_jobs()

    assert jobs_expected == jobs
