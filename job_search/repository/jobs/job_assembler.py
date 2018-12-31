from job_search.domain.jobs.value_objects.job_type import JobInfo
from job_search.domain.jobs.value_objects.simple_objects import ContactInfo, LocationInfo
from job_search.repository.jobs.entities.job_entity import JobEntity


class JobAssembler:

    def to_domain_object(self, job_entity: JobEntity) -> JobInfo:
        location = LocationInfo(city=job_entity.location_entity.city_entity.name,
                                state=job_entity.location_entity.state_entity.name,
                                country=job_entity.location_entity.country_entity.name)
        restrictions = [x.name_entity.name for x in job_entity.restrictions_entity.restriction_entities]
        requirements = [x.name_entity.name for x in job_entity.requirements_entity.requirement_entities]
        contact_info = ContactInfo(contact=job_entity.contact_info_entity.name_entity.name,
                                   email=job_entity.contact_info_entity.email_entity.name,
                                   website=job_entity.contact_info_entity.website_entity.name)

        return JobInfo(uid=job_entity.id,
                       title=job_entity.title,
                       company=job_entity.company_entity.name,
                       location=location,
                       description=job_entity.description,
                       restrictions=restrictions,
                       requirements=requirements,
                       about=job_entity.about,
                       contact_info=contact_info,
                       source=job_entity.source_entity.name)
