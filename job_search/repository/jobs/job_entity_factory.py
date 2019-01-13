from typing import List
import job_search.repository.jobs.entities.job_entity as entities
from job_search.domain.jobs.value_objects.job_type import JobInfo
from job_search.domain.jobs.value_objects.simple_objects import ContactInfo, LocationInfo
from job_search.domain.jobs.job_repository import JobRepository


class JobEntityFactory:

    def __init__(self, repository: JobRepository):
        self.repository = repository

    def create_job_entity(self, job: JobInfo) -> entities.JobEntity:
        title = self.__assemble_title_entity(job.title)
        company = self.__assemble_company_entity(job.company)
        source = self.__assemble_source_entity(job.source)
        location = self.__assemble_location_entity(job.location)
        contact_info = self.__assemble_contact_info_entity(job.contact_info)
        restrictions = self.__assemble_restrictions(job.restrictions)
        requirements = self.__assemble_requirements(job.requirements)

        return entities.JobEntity(id=job.uid,
                                  title_entity=title,
                                  description=job.description,
                                  about=job.about,
                                  company_entity=company,
                                  location_entity=location,
                                  contact_info_entity=contact_info,
                                  restrictions_entity=restrictions,
                                  requirements_entity=requirements,
                                  source_entity=source,
                                  pinned=job.pinned)

    def __rm_empty_strings(self, strings: List[str]) -> List[str]:
        return list(filter(lambda x: x, strings))

    def __assemble_title_entity(self, title: str) -> entities.TitleEntity:
        entity = self.repository.find_title(title)
        if entity is None:
            entity = entities.TitleEntity(name=title)
        return entity

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
                                                      country_entity=country_entity,
                                                      lat=location.lat, lng=location.lng)

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

    def __assemble_restrictions(self, restrictions: List[str]) -> entities.RestrictionsEntity:
        restrictions_in_repo = self.repository.find_restrictions(restrictions)
        restriction_entities = restrictions_in_repo['found']
        not_found = restrictions_in_repo['not_found']

        new_restriction_entities = []
        for entity in restriction_entities:
            new_entity = entities.RestrictionEntity(name_id=entity.name_entity.id, name_entity=entity.name_entity)
            new_restriction_entities.append(new_entity)

        if not_found:
            new_name_entities = [entities.RestrictionNameEntity(name=x) for x in not_found]
            new_entities = [entities.RestrictionEntity(name_entity=x) for x in new_name_entities]
            new_restriction_entities.extend(new_entities)

        return entities.RestrictionsEntity(restriction_entities=new_restriction_entities)

    def __assemble_requirements(self, requirements: List[str]) -> entities.RequirementsEntity:
        requirements_in_repo = self.repository.find_requirements(requirements)
        requirement_entities = requirements_in_repo['found']
        not_found = requirements_in_repo['not_found']

        new_requirement_entities = []
        for entity in requirement_entities:
            new_entity = entities.RequirementEntity(name_id=entity.name_entity.id, name_entity=entity.name_entity)
            new_requirement_entities.append(new_entity)

        if not_found:
            new_name_entities = [entities.RequirementNameEntity(name=x) for x in not_found]
            new_entities = [entities.RequirementEntity(name_entity=x) for x in new_name_entities]
            new_requirement_entities.extend(new_entities)

        return entities.RequirementsEntity(requirement_entities=new_requirement_entities)
