from tests.repository.jobs import entity_comparer
from job_search.repository.jobs.job_assembler import JobAssembler
import job_search.repository.jobs.entities.job_entity as entities


def test_givenANormalJobEntity_whenAssemblingAJob_thenReturnTheExpectedJob():
    a_title = entities.TitleEntity(name='a title')
    a_description = 'a description'
    an_about = ['an', 'about', 'section']
    a_source = entities.SourceEntity(name='a source')
    a_company = entities.CompanyEntity(name='a company')
    a_location = entities.LocationEntity(city_entity=entities.CityEntity(name='munich'),
                                         state_entity=entities.StateEntity(name='bavaria'),
                                         country_entity=entities.CountryEntity(name='germany'),
                                         lat=0, lng=0)
    some_restrictions = __make_some_restrictions()
    some_requirements = __make_some_requirements()
    a_contact_info = __make_a_contact_info()
    is_pinned = False
    a_job_entity = entities.JobEntity(title_entity=a_title, description=a_description, about=an_about,
                                      company_entity=a_company, location_entity=a_location,
                                      restrictions_entity=some_restrictions,
                                      requirements_entity=some_requirements, pinned=is_pinned,
                                      contact_info_entity=a_contact_info, source_entity=a_source)

    assembler = JobAssembler()
    job = assembler.to_domain_object(a_job_entity)

    assert entity_comparer.are_equivalent(job, a_job_entity)


def __make_some_restrictions():
    a_restriction_name = entities.RestrictionNameEntity(name='test')
    restrictions = [entities.RestrictionEntity(name_entity=a_restriction_name)]
    return entities.RestrictionsEntity(restriction_entities=restrictions)


def __make_some_requirements():
    a_requirement_name = entities.RequirementNameEntity(name='test')
    requirements = [entities.RequirementEntity(name_entity=a_requirement_name)]
    return entities.RequirementsEntity(requirement_entities=requirements)


def __make_a_contact_info():
    contact_name_entity = entities.ContactNameEntity(name='a contact')
    contact_email_entity = entities.ContactEmailEntity(name='gimme@moar.no')
    contact_website_entity = entities.ContactWebsiteEntity(name='goals.com')
    return entities.ContactInfoEntity(name_entity=contact_name_entity,
                                      email_entity=contact_email_entity,
                                      website_entity=contact_website_entity)
