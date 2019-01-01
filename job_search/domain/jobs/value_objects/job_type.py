from enum import Enum
from typing import List
from job_search.domain.jobs.value_objects.simple_objects import ContactInfo, LocationInfo


class JobTypeSource(Enum):
    PYTHON_ORG = 'https://www.python.org/jobs/'


class JobInfo:

    def __init__(self, uid: str, title: str, company: str, location: LocationInfo, description: str,
                 restrictions: List[str], requirements: List[str], about: List[str],
                 contact_info: ContactInfo, source: JobTypeSource, pinned: bool):
        self.uid = uid
        self.title = title
        self.company = company
        self.location = location
        self.description = description
        self.restrictions = restrictions
        self.requirements = requirements
        self.about = about
        self.contact_info = contact_info
        self.source = source
        self.pinned = pinned

    def __eq__(self, other):
        return (self.uid == other.uid and
                self.title == other.title and
                self.company == other.company and
                self.location == other.location and
                self.description == other.description and
                set(self.restrictions) == set(other.restrictions) and
                set(self.requirements) == set(other.requirements) and
                set(self.about) == set(other.about) and
                self.contact_info == other.contact_info and
                self.source == other.source and
                self.pinned == other.pinned)
