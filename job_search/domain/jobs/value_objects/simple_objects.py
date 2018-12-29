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

    def __init__(self, city: str, state: str, country: str):
        self.city = city
        self.state = state
        self.country = country

    def __eq__(self, other):
        return (self.city == other.city and
                self.state == other.state and
                self.country == other.country)

    def __str__(self):
        string = f'{self.city}, '
        if self.state is not None:
            string += f'{self.state}, '
        return string + f'{self.country}'
