from typing import Dict, List


class Job:

    def __init__(self, title: str, company: str, location: str,
                 description: str, restrictions: List[str], requirements: List[str],
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
        for a, b in zip(self.__dict__.values(), other.__dict__.values()):
            if a != b:
                return False
        return True


class ContactInfo:

    def __init__(self, contact: str, email: str, website: str):
        self.contact = contact
        self.email = email
        self.website = website

    def __eq__(self, other):
        return (self.contact == other.contact and
                self.email == other.email and
                self.website == other.website)


class LocationInfo:

    def __init__(self, city: str, state: str, country: str, lat: float, lng: float):
        self.city = city
        self.state = state
        self.country = country
        self.lat = lat
        self. lng = lng

    def __eq__(self, other):
        return (self.city == other.city and
                self.state == other.state and
                self.country == other.country and
                self.lat == other.lat and
                self.lng == other. lng)

    def __str__(self):
        string = f'{self.city}, '
        if self.state is not None:
            string += f'{self.state}, '
        return string + f'{self.country}'
