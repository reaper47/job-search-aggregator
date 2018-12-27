from job_search.domain.jobs.value_objects.job_type import JobInfoPython
from job_search.domain.jobs.value_objects.simple_objects import LocationInfo, ContactInfo
from job_search.repository.jobs.job_entity_factory import JobEntityFactory
from tests.repository.jobs import entity_comparer


def test_givenANormalJobInfo_whenAssemblingAJobEntity_thenReturnTheExpectedJobEntity():
    a_title = 'Pythonista'
    a_company = 'Python Café'
    a_location = LocationInfo(city='Quebec City', state='Quebec', country='Canada')
    a_description = 'This is a gold mine.'
    some_restrictions = ['No telecommuting', 'No remote work available']
    some_requirements = ['Degree in computer science', 'Deep knowledge of Python 3']
    an_about = ['Python Café is the number one company in providing caffeine to its employees']
    a_contact_info = ContactInfo(contact='Mr. Joshua', email='josh@python.org', website='https://www.pcafe.org')
    a_job = JobInfoPython(title=a_title, company=a_company,
                          location=a_location, description=a_description,
                          restrictions=some_restrictions, about=an_about,
                          requirements=some_requirements, contact_info=a_contact_info)

    assembler = JobEntityFactory()
    job_entity = assembler.create_job_entity(a_job)

    assert entity_comparer.are_equivalent(a_job, job_entity)
