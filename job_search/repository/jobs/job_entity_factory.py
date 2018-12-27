import job_search.repository.jobs.entities.job_entity as entities
from job_search.domain.jobs.value_objects.job_type import JobInfo
from job_search.domain.jobs.value_objects.simple_objects import LocationInfo
from job_search.domain.jobs.job_repository import JobRepository


class JobEntityFactory:

    def __init__(self, repository: JobRepository):
        self.repository = repository

    def create_job_entity(self, job: JobInfo) -> entities.JobEntity:
        company = self.__assemble_company_entity(job.company)
        source = self.__assemble_source_entity(job.source)

        '''city = entities.CityEntity(name=job.location.city)
        state = entities.StateEntity(name=job.location.state)
        country = self.__assemble_country_entity(job.location.country)
        location = entities.LocationEntity(city_entity=city, state_entity=state, country_entity=country)'''
        location = self.__assemble_location_entity(job.location)

        restriction_names = [entities.RestrictionNameEntity(name=x) for x in job.restrictions]
        restrictions = entities.RestrictionEntity(name_entities=restriction_names)

        requirement_names = [entities.RequirementNameEntity(name=x) for x in job.requirements]
        requirements = entities.RequirementEntity(name_entities=requirement_names)

        contact_info = entities.ContactInfoEntity(contact=job.contact_info.contact,
                                                  email=job.contact_info.email,
                                                  website=job.contact_info.website)

        return entities.JobEntity(title=job.title,
                                  description=job.description,
                                  about=job.about,
                                  company_entity=company,
                                  location_entity=location,
                                  contact_info_entity=contact_info,
                                  restrictions_entity=restrictions,
                                  requirements_entity=requirements,
                                  source_entity=source)

    def __assemble_company_entity(self, company: str) -> entities.CompanyEntity:
        entity = self.repository.find_company(company)
        if entity is None:
            entity = entities.CompanyEntity(name=company)
        return entity

    def __assemble_source_entity(self, source: str) -> entities.SourceEntity:
        entity = self.repository.find_source(source)
        if entity is None:
            entity = entities.SourceEntity(name=source)
        return entity

    def __assemble_location_entity(self, location: LocationInfo) -> entities.LocationEntity:
        location_entity = self.repository.find_location(location)
        if location_entity is None:
            city, state, country = location.city, location.state, location.country

            city_entity = self.repository.find_city(city)
            if city_entity is None:
                city_entity = entities.CityEntity(name=city)

            state_entity = self.repository.find_state(state)
            if state_entity is None:
                state_entity = entities.StateEntity(name=state)

            country_entity = self.repository.find_country(country)
            if country_entity is None:
                country_entity = entities.CountryEntity(name=country)

            location_entity = entities.LocationEntity(city_entity=city_entity,
                                                      state_entity=state_entity,
                                                      country_entity=country_entity)

        return location_entity
