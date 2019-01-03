from unittest.mock import Mock
import pytest
from job_search.domain.jobs.value_objects.job_type import JobInfo, JobTypeSource
from job_search.domain.jobs.value_objects.simple_objects import ContactInfo, LocationInfo
from job_search.domain.jobs.job_repository import JobRepository
from job_search.repository.jobs.job_entity_factory import JobEntityFactory
from job_search.repository.jobs.entities.job_entity import (RestrictionEntity, RestrictionNameEntity,
                                                            RequirementEntity, RequirementNameEntity)
from tests.repository.jobs import entity_comparer

A_COMPANY = 'Python Café'
A_COUNTRY = 'Canada'
A_RESTRICTION = 'No telecommuting'
ANOTHER_RESTRICTION = 'No remote work available'
A_REQUIREMENT = 'Degree in computer science'
ANOTHER_REQUIREMENT = 'Deep knowledge of Python 3'


@pytest.fixture
def a_job() -> JobInfo:
    uid = 'PY-QCQC-PC-P'
    a_title = 'Pythonista'
    a_company = A_COMPANY
    a_location = LocationInfo(city='Quebec City', state='Quebec', country=A_COUNTRY, lat=0, lng=0)
    a_description = 'This is a gold mine.'
    some_restrictions = [A_RESTRICTION, ANOTHER_RESTRICTION]
    some_requirements = [A_REQUIREMENT, ANOTHER_REQUIREMENT]
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
def mock_empty_repo():
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
    mock.find_restrictions.return_value = {
        'found': [
            RestrictionEntity(name_entity=RestrictionNameEntity(name=A_RESTRICTION)),
            RestrictionEntity(name_entity=RestrictionNameEntity(name=ANOTHER_RESTRICTION))
        ],
        'not_found': []
    }
    mock.find_requirements.return_value = {
        'found': [
            RequirementEntity(name_entity=RequirementNameEntity(name=A_REQUIREMENT)),
            RequirementEntity(name_entity=RequirementNameEntity(name=ANOTHER_REQUIREMENT))
        ],
        'not_found': []
    }
    mock.find_source.return_value = None
    return mock


def test_givenAJobWithUniqueValues_whenAssemblingAJobEntity_thenAssembleCorrectly(a_job, mock_empty_repo):
    assembler = JobEntityFactory(mock_empty_repo)
    job_entity = assembler.create_job_entity(a_job)

    assert entity_comparer.are_equivalent(a_job, job_entity)
