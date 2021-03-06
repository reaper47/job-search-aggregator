from pathlib import Path
from unittest import mock
import pytest
from tests.helpers.stubs import RequestsStub
from job_search.domain.jobs.sources.python_org import PythonOrg
from job_search.domain.jobs.value_objects.simple_objects import Job

BASE_DIR = Path(__file__).parent
with open(f'{BASE_DIR}/samples/job_posting.html') as f:
    SOME_JOBS = f.read()
with open(f'{BASE_DIR}/samples/job_post.html') as f:
    A_JOB_POST = f.read()

MOCK_REQUESTS = 'job_search.domain.jobs.sources.python_org.requests'


@pytest.fixture
def python_org():
    return PythonOrg()


@pytest.fixture
@mock.patch(MOCK_REQUESTS)
def python_org_brewed(mock_requests):
    python_org = PythonOrg()
    mock_requests.get.return_value = RequestsStub(SOME_JOBS)
    python_org.prepare_soup()
    return python_org


@mock.patch(MOCK_REQUESTS)
def test_givenAJobPosting_whenPreparingTheSoup_thenAllPagesShouldBeScraped(mock_requests, python_org):
    mock_requests.get.return_value = RequestsStub(SOME_JOBS)
    npages_expected = 2

    python_org.prepare_soup()

    assert npages_expected == len(python_org.pages)


@mock.patch(MOCK_REQUESTS)
def test_givenABrewedPythonSoup_whenFetchingJobs_thenScrapeInfoFromAllJobs(mock_requests, python_org_brewed):
    mock_requests.get.return_value = RequestsStub(A_JOB_POST)
    a_job = Job(title='Quantitative Data Engineer',
                company='Tudor Investment Corporation',
                location='New York, New York, United States',
                description=('We are looking for an outstanding engineer.\n\n'
                             '- Design\n- Explore\n- Eat\n\n'
                             'Your main tasks and responsibilities include stuff.'),
                restrictions=['No telecommuting', 'No Agencies Please'],
                requirements=['Proficiency in Python', '- Experience in Python', '- Experience in C', 'Django'],
                about='About us\n\n- Competitive salary\n- Supported learning\n\nCome work',
                contact_info={
                    'contact': 'Morgan Nelson',
                    'email': 'morgan.nelson@tudor.com',
                    'website': 'https://boards.greenhouse.io/'})
    jobs_expected = [a_job]*4

    jobs = python_org_brewed.fetch_jobs()

    assert jobs_expected == jobs
