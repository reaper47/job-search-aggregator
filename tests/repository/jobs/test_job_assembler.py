from tests.repository.jobs import entity_comparer
from job_search.repository.jobs.job_assembler import JobAssembler
import job_search.repository.jobs.entities.job_entity as entities


def test_givenANormalJobEntity_whenAssemblingAJob_thenReturnTheExpectedJob():
    a_title = 'a title'
    a_description = 'a description'
    an_about = ['an', 'about', 'section']
    a_source = entities.SourceEntity(name='a source')
    a_company = entities.CompanyEntity(name='a company')
    a_location = entities.LocationEntity(city_entity=entities.CityEntity(name='munich'),
                                         state_entity=entities.StateEntity(name='bavaria'),
                                         country_entity=entities.CountryEntity(name='germany'))
    restrictions = [entities.RestrictionNameEntity(name=str(i)) for i in range(10)]
    some_restrictions = entities.RestrictionEntity(name_entities=restrictions)
    requirements = [entities.RequirementNameEntity(name=str(i)) for i in range(10)]
    some_requirements = entities.RequirementEntity(name_entities=requirements)
    a_contact_info = entities.ContactInfoEntity(contact='a contact', email='gimme@moar.no', website='goals.com')
    a_job_entity = entities.JobEntity(title=a_title, description=a_description, about=an_about,
                                      company_entity=a_company, location_entity=a_location,
                                      restrictions_entity=some_restrictions,
                                      requirements_entity=some_requirements,
                                      contact_info_entity=a_contact_info, source_entity=a_source)

    assembler = JobAssembler()
    job = assembler.to_domain_object(a_job_entity)

    assert entity_comparer.are_equivalent(job, a_job_entity)
