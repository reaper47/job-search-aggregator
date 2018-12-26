from typing import List
from job_search.domain.jobs.value_objects.job_type import JobInfo, JobInfoPython
from job_search.domain.jobs.value_objects.simple_objects import LocationInfo, ContactInfo
from job_search.repository.jobs.entities.job_entity import (JobEntity, ContactInfoEntity, LocationEntity,
                                                            RestrictionEntity, RequirementEntity)
from job_search.repository.jobs.job_entity_factory import JobEntityFactory


def test_givenANormalJobInfo_whenAssemblingAJobEntity_thenReturnTheExpectedJobEntity():
    a_title = 'Pythonista'
    a_company = 'Python Café'
    a_location = LocationInfo(city='Quebec City', state='Quebec', country='Canada')
    a_description = 'This is a gold mine.'
    some_restrictions = ['No telecommuting', 'No remote work available']
    some_requirements = ['Degree in computer science', 'Deep knowledge of Python 3']
    an_about = ['Python Café is the number one company in providing caffeine to its employees']
    a_contact_info = ContactInfo(contact='Mr. Joshua', email='josh@python.org', website='https://www.pcafe.org')
    a_job_info = JobInfoPython(title=a_title, company=a_company,
                               location=a_location, description=a_description,
                               restrictions=some_restrictions, about=an_about,
                               requirements=some_requirements, contact_info=a_contact_info)

    assembler = JobEntityFactory()
    job_entity = assembler.create_job_entity(a_job_info)

    assert are_equivalent(a_job_info, job_entity)


def are_equivalent(job_info: JobInfo, job_entity: JobEntity) -> bool:
    return (job_info.title == job_entity.title and
            job_info.company == job_entity.company_entity.name and
            __are_locations_equivalent(job_info.location, job_entity.location_entity) and
            job_info.description == job_entity.description and
            __are_restrictions_equivalent(job_info.restrictions, job_entity.restrictions_entity) and
            __are_requirements_equivalent(job_info.requirements, job_entity.requirements_entity) and
            job_info.about == job_entity.about and
            __are_contacts_equivalent(job_info.contact_info, job_entity.contact_info_entity))


def __are_locations_equivalent(location_info: LocationInfo, location_entity: LocationEntity) -> bool:
    return (location_info.city == location_entity.city_entity.name and
            location_info.state == location_entity.state_entity.name and
            location_info.country == location_entity.country_entity.name)


def __are_restrictions_equivalent(restrictions: List[str], restrictions_entity: List[RestrictionEntity]) -> bool:
    restrictions_entity = [x.name for x in restrictions_entity.name_entities]
    return set(restrictions) == set(restrictions_entity)


def __are_requirements_equivalent(requirements: List[str], requirements_entity: List[RequirementEntity]) -> bool:
    requirements_entity = [x.name for x in requirements_entity.name_entities]
    return set(requirements) == set(requirements_entity)


def __are_contacts_equivalent(contact_info: ContactInfo, contact_info_entity: ContactInfoEntity) -> bool:
    return (contact_info.contact == contact_info_entity.contact and
            contact_info.email == contact_info_entity.email and
            contact_info.website == contact_info_entity.website)
