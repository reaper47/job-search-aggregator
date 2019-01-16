import pytest
from unittest.mock import Mock
from job_search.domain.jobs.job_repository import JobRepository
from job_search.domain.jobs.value_objects.job_type import JobInfo, JobTypeSource
from job_search.domain.jobs.value_objects.simple_objects import ContactInfo, LocationInfo
from job_search.application.services.jobs.job_factory import JobFactory
from job_search.application.services.jobs.job_service import JobService


@pytest.fixture
def mock_job_factory():
    return Mock(spec=JobFactory)


@pytest.fixture
def mock_repo(a_job):
    mock = Mock(spec=JobRepository)
    mock.load.return_value = a_job
    mock.load_all_jobs.return_value = [a_job, a_job]
    return mock


@pytest.fixture
def a_job() -> JobInfo:
    uid = 'QCQC-PC-P'
    a_title = 'Pythonista'
    a_company = 'Python Café'
    a_location = LocationInfo(city='Quebec City', state='Quebec', country='Canada', lat=0, lng=0)
    a_description = 'This is a gold mine.'
    some_restrictions = ['No telecommuting', 'No remote work available']
    some_requirements = ['No remote work available', 'Deep knowledge of Python 3']
    an_about = ['Python Café is the number one company in providing caffeine to its employees']
    a_contact_info = ContactInfo(contact='Mr. Joshua', email='josh@python.org', website='https://www.pcafe.org')
    a_source = JobTypeSource.PYTHON_ORG.value
    is_pinned = False

    return JobInfo(uid=uid, title=a_title, company=a_company,
                   location=a_location, description=a_description,
                   restrictions=some_restrictions, about=an_about,
                   requirements=some_requirements, contact_info=a_contact_info,
                   source=a_source, pinned=is_pinned)


@pytest.fixture
def job_service(mock_repo):
    return JobService(mock_repo)


def test_whenConsultingAJob_thenReturnTheRightJob(a_job, job_service):
    job_found = job_service.consult_job(a_job.uid)

    assert a_job == job_found


def test_whenGatheringAllJobs_thenReturnAllJobsInTheRepository(a_job, job_service):
    jobs_found = job_service.gather_all_jobs()

    some_jobs = [a_job, a_job]
    assert some_jobs == jobs_found
