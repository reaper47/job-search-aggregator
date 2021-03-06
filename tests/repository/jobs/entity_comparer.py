from typing import List
from job_search.domain.jobs.value_objects.job_type import JobInfo
from job_search.domain.jobs.value_objects.simple_objects import LocationInfo, ContactInfo
from job_search.repository.jobs.entities.job_entity import (JobEntity, ContactInfoEntity, LocationEntity,
                                                            RestrictionEntity, RequirementEntity)


def are_equivalent(job_info: JobInfo, job_entity: JobEntity) -> bool:
    return (job_info.uid == job_entity.id and
            job_info.title == job_entity.title_entity.name and
            job_info.company == job_entity.company_entity.name and
            __are_locations_equivalent(job_info.location, job_entity.location_entity) and
            job_info.description == job_entity.description and
            __are_restrictions_equivalent(job_info.restrictions, job_entity.restrictions_entity) and
            __are_requirements_equivalent(job_info.requirements, job_entity.requirements_entity) and
            job_info.about == job_entity.about and
            __are_contacts_equivalent(job_info.contact_info, job_entity.contact_info_entity) and
            job_info.source == job_entity.source_entity.name and
            job_info.pinned == job_entity.pinned)


def __are_locations_equivalent(location_info: LocationInfo, location_entity: LocationEntity) -> bool:
    return (location_info.city == location_entity.city_entity.name and
            location_info.state == location_entity.state_entity.name and
            location_info.country == location_entity.country_entity.name and
            location_info.lat == location_entity.lat and
            location_info.lng == location_info.lng)


def __are_restrictions_equivalent(restrictions: List[str], restrictions_entity: List[RestrictionEntity]) -> bool:
    restriction_entities = restrictions_entity.restriction_entities
    restriction_name_entities = [x.name_entity.name for x in restriction_entities]
    return set(restrictions) == set(restriction_name_entities)


def __are_requirements_equivalent(requirements: List[str], requirements_entity: List[RequirementEntity]) -> bool:
    requirement_entities = requirements_entity.requirement_entities
    requirements_entity = [x.name_entity.name for x in requirement_entities]
    return set(requirements) == set(requirements_entity)


def __are_contacts_equivalent(contact_info: ContactInfo, contact_info_entity: ContactInfoEntity) -> bool:
    return (contact_info.contact == contact_info_entity.name_entity.name and
            contact_info.email == contact_info_entity.email_entity.name and
            contact_info.website == contact_info_entity.website_entity.name)
