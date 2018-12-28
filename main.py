from job_search.repository.jobs.sqlite_job_repository import SQLiteJobRepository
from job_search.domain.jobs.value_objects.simple_objects import ContactInfo, LocationInfo
from job_search.domain.jobs.value_objects.job_type import JobInfoPython

a_title = 'Pythonista'
a_company = 'Python Café'
a_location = LocationInfo(city='Montreal', state='Quebec', country='Canada')
a_description = 'This is a gold mine.'
some_restrictions = ['No telecommuting', 'No remote work available']
some_requirements = ['Degree in computer science', 'Deep knowledge of Python 3']
an_about = ['Python Café is the number one company in providing caffeine to its employees']
a_contact_info = ContactInfo(contact='Ms. Joshua', email='josh@python.org', website='https://www.pcafe.org')
job = JobInfoPython(title=a_title, company=a_company,
                    location=a_location, description=a_description,
                    restrictions=some_restrictions, about=an_about,
                    requirements=some_requirements, contact_info=a_contact_info)

s = SQLiteJobRepository()
s.persist(job)
