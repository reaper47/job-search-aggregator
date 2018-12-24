from typing import List, Dict


class JobInfo:

    def __init__(self, title: str, company: str, location: str, description: str,
                 restrictions: List[str], requirements: List[str],
                 about: List[str], contact_info: Dict[str, str]):
        self.title = title
        self.company = company
        self.location = location
        self.description = description
        self.restrictions = restrictions
        self.requirements = requirements
        self.about = about
        self.contact_info = contact_info

    def __eq__(self, other):
        return (self.title == other.title and
                self.company == other.company and
                self.location == other.location and
                self.description == other.description and
                set(self.restrictions) == set(other.restrictions) and
                set(self.requirements) == set(other.requirements) and
                set(self.about) == set(other.about) and
                self.contact_info == other.contact_info)


class JobInfoPython(JobInfo):

    def __init__(self, title, company, location, description,
                 restrictions, requirements, about, contact_info):
        super().__init__(title, company, location, description, restrictions,
                         requirements, about, contact_info)
        self.source = 'https://www.python.org/jobs/'
