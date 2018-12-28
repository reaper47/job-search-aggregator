import job_search.repository.jobs.entities.job_entity as entities
from job_search.domain.jobs.value_objects.job_type import JobInfo
from job_search.domain.jobs.value_objects.simple_objects import ContactInfo, LocationInfo
from job_search.domain.jobs.job_repository import JobRepository


class JobEntityFactory:

    def __init__(self, repository: JobRepository):
        self.repository = repository

    def create_job_entity(self, job: JobInfo) -> entities.JobEntity:
        company = self.__assemble_company_entity(job.company)
        source = self.__assemble_source_entity(job.source)
        location = self.__assemble_location_entity(job.location)
        contact_info = self.__assemble_contact_info_entity(job.contact_info)

        restriction_names = [entities.RestrictionNameEntity(name=x) for x in job.restrictions]
        restrictions = entities.RestrictionEntity(name_entities=restriction_names)

        requirement_names = [entities.RequirementNameEntity(name=x) for x in job.requirements]
        requirements = entities.RequirementEntity(name_entities=requirement_names)

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

    def __assemble_contact_info_entity(self, info: ContactInfo) -> entities.ContactInfoEntity:
        contact_info_entity = self.repository.find_contact_info(info)
        if contact_info_entity is None:
            name_entity = self.repository.find_contact_name(info.contact)
            if name_entity is None:
                name_entity = entities.ContactNameEntity(name=info.contact)

            email_entity = self.repository.find_contact_email(info.email)
            if email_entity is None:
                email_entity = entities.ContactEmailEntity(name=info.email)

            website_entity = self.repository.find_contact_website(info.website)
            if website_entity is None:
                website_entity = entities.ContactWebsiteEntity(name=info.website)

            contact_info_entity = entities.ContactInfoEntity(name_entity=name_entity,
                                                             email_entity=email_entity,
                                                             website_entity=website_entity)

        return contact_info_entity
