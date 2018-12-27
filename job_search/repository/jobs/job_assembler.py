from job_search.domain.jobs.value_objects.job_type import JobInfo
from job_search.domain.jobs.value_objects.simple_objects import ContactInfo, LocationInfo
from job_search.repository.jobs.entities.job_entity import JobEntity


class JobAssembler:

    def to_domain_object(self, job_entity: JobEntity) -> JobInfo:
        location = LocationInfo(city=job_entity.location_entity.city_entity.name,
                                state=job_entity.location_entity.state_entity.name,
                                country=job_entity.location_entity.country_entity.name)
        restrictions = [x.name for x in job_entity.restrictions_entity.name_entities]
        requirements = [x.name for x in job_entity.requirements_entity.name_entities]
        contact_info = ContactInfo(contact=job_entity.contact_info_entity.contact,
                                   email=job_entity.contact_info_entity.email,
                                   website=job_entity.contact_info_entity.website)

        return JobInfo(title=job_entity.title,
                       company=job_entity.company_entity.name,
                       location=location,
                       description=job_entity.description,
                       restrictions=restrictions,
                       requirements=requirements,
                       about=job_entity.about,
                       contact_info=contact_info)
