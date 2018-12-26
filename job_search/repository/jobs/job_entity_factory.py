import job_search.repository.jobs.entities.job_entity as entities
from job_search.domain.jobs.value_objects.job_type import JobInfo


class JobEntityFactory:

    def create_job_entity(self, job: JobInfo) -> entities.JobEntity:
        company = entities.CompanyEntity(name=job.company)
        source = entities.SourceEntity(name=job.source)

        city = entities.CityEntity(name=job.location.city)
        state = entities.StateEntity(name=job.location.state)
        country = entities.CountryEntity(name=job.location.country)
        location = entities.LocationEntity(city_entity=city, state_entity=state, country_entity=country)

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
