from typing import Dict, List
from urllib.parse import urlparse
from job_search.domain.jobs.value_objects.job_type import JobInfo, ContactInfo, LocationInfo, JobTypeSource
from job_search.domain.jobs.value_objects.simple_objects import Job


class JobFactory:

    def create_job(self, job: Job, job_type: JobTypeSource) -> JobInfo:
        uid = self.__generate_id(job_type.value, job.location, job.company, job.title)
        location = self.__location_to_value_object(job.location)
        contact_info = self.__contact_info_to_value_object(job.contact_info)

        return JobInfo(uid=uid,
                       title=job.title,
                       company=job.company,
                       location=location,
                       description=job.description,
                       restrictions=job.restrictions,
                       requirements=job.requirements,
                       about=job.about,
                       contact_info=contact_info,
                       source=job_type)

    def __generate_id(self, source: str, location: str, company: str, title: str) -> str:
        source_name = urlparse(source).netloc.split('.')[1]
        source_initials = source_name[:2].upper()

        location_split = [y for x in location.split(',') for y in x.split(' ')]
        location_split = self.__rm_empty_strings(location_split)
        location_initials = self.__mk_initials(location_split)

        company_split = self.__rm_empty_strings(company.split(' '))
        company_initials = self.__mk_initials(company_split)

        title_split = self.__rm_empty_strings(title.split(' '))
        title_initials = self.__mk_initials(title_split)

        return f'{source_initials}-{location_initials}-{company_initials}-{title_initials}'

    def __rm_empty_strings(self, strings: List[str]) -> List[str]:
        return list(filter(lambda x: x, strings))

    def __mk_initials(self, strings: List[str]) -> str:
        return ''.join(x[0].upper() for x in strings)

    def __location_to_value_object(self, location: str) -> LocationInfo:
        location_split = list(map(lambda x: x.strip(), location.split(',')))

        state = None
        if len(location_split) == 3:
            state = location_split[1]

        return LocationInfo(city=location_split[0],
                            state=state,
                            country=location_split[-1])

    def __contact_info_to_value_object(self, contact_info: Dict[str, str]) -> ContactInfo:
        contact, email, website = None, None, None

        if 'contact' in contact_info:
            contact = contact_info['contact']

        if 'email' in contact_info:
            email = contact_info['email']

        if 'website' in contact_info:
            website = contact_info['website']

        return ContactInfo(contact=contact, email=email, website=website)
