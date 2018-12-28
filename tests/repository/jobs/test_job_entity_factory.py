from unittest.mock import Mock
import pytest
from job_search.domain.jobs.value_objects.job_type import JobInfoPython
from job_search.domain.jobs.value_objects.simple_objects import LocationInfo, ContactInfo
from job_search.domain.jobs.job_repository import JobRepository
from job_search.repository.jobs.job_entity_factory import JobEntityFactory
from tests.repository.jobs import entity_comparer

A_COMPANY = 'Python Café'
A_COUNTRY = 'Canada'


@pytest.fixture
def a_job():
    a_title = 'Pythonista'
    a_company = A_COMPANY
    a_location = LocationInfo(city='Quebec City', state='Quebec', country=A_COUNTRY)
    a_description = 'This is a gold mine.'
    some_restrictions = ['No telecommuting', 'No remote work available']
    some_requirements = ['Degree in computer science', 'Deep knowledge of Python 3']
    an_about = ['Python Café is the number one company in providing caffeine to its employees']
    a_contact_info = ContactInfo(contact='Mr. Joshua', email='josh@python.org', website='https://www.pcafe.org')

    return JobInfoPython(title=a_title, company=a_company,
                         location=a_location, description=a_description,
                         restrictions=some_restrictions, about=an_about,
                         requirements=some_requirements, contact_info=a_contact_info)


@pytest.fixture
def repo_empty_mock():
    mock = Mock(spec=JobRepository)
    mock.find_company.return_value = None
    mock.find_location.return_value = None
    mock.find_city.return_value = None
    mock.find_state.return_value = None
    mock.find_country.return_value = None
    mock.find_contact_info.return_value = None
    mock.find_contact_name.return_value = None
    mock.find_contact_email.return_value = None
    mock.find_contact_website.return_value = None
    mock.find_source.return_value = None
    return mock


def test_givenAJobWithUniqueValues_whenAssemblingAJobEntity_thenAssembleCorrectly(a_job, repo_empty_mock):
    assembler = JobEntityFactory(repo_empty_mock)
    job_entity = assembler.create_job_entity(a_job)

    assert entity_comparer.are_equivalent(a_job, job_entity)
