from typing import List
import requests
from bs4 import BeautifulSoup, Tag
from job_search.domain.jobs.value_objects.simple_objects import Job

HTML = 'html.parser'


class PythonOrg:

    def __init__(self):
        self.website = 'https://www.python.org/jobs/'
        self.pagination_class = 'pagination menu'
        self.jobs_class = 'list-recent-jobs list-row-container menu'

    def prepare_soup(self) -> None:
        request = requests.get(self.website)
        job_posting = BeautifulSoup(request.text, features=HTML)
        self.pages = self.__get_pages(job_posting)

    def __get_pages(self, job_posting: BeautifulSoup) -> List[BeautifulSoup]:
        npages = self.__get_number_of_pages(job_posting)
        second_page = 2

        soups = [job_posting]
        for i in range(second_page, npages):
            request = requests.get(f"{self.website}?page={i}")
            soups.append(BeautifulSoup(request.text, features=HTML))

        return soups

    def __get_number_of_pages(self, job_posting: BeautifulSoup) -> int:
        ul = job_posting.find_all('ul', class_=self.pagination_class)
        pages_raw = [el.text for el in ul][0].split('\n')

        pages = [job_posting]
        for el in pages_raw:
            try:
                pages.append(int(el))
            except ValueError:
                pass

        return len(pages)

    def fetch_jobs(self) -> List[Job]:
        jobs_scraped = []
        for page in self.pages:
            all_jobs = page.find_all('ol', class_=self.jobs_class)[0].find_all('li')

            for job in all_jobs:
                link = job.find('span', class_='listing-company-name').find('a')['href']
                job_request = requests.get(f'https://www.python.org{link}')
                job_soup = BeautifulSoup(job_request.text, features=HTML)
                job_text = job_soup.find('article', class_='text')
                jobs_scraped.append(self.__scrape_job(job_text))

        return jobs_scraped

    def __scrape_job(self, job: BeautifulSoup) -> Job:
        descriptions = job.find('div', class_='job-description').find_all('h2')

        title_tag = descriptions[0]
        descr_tag = descriptions[1]
        restr_tag = descriptions[2]
        reqs_tag = descriptions[3]
        about_tag = descriptions[4]
        contact_tag = descriptions[5]
        company_tag = job.find('span', 'company-name')

        return Job(title=title_tag.next_sibling.strip(),
                   company=self.__strip_list(company_tag.text.split('\n'))[-1],
                   location=job.find('span', class_='listing-location').text,
                   description=self.__get_description(descr_tag),
                   restrictions=self.__strip_list(self.__get_child_tag(restr_tag).text.split('\n')),
                   requirements=self.__get_requirements(reqs_tag),
                   about=self.__get_about(about_tag),
                   contact_info=self.__get_contact_info(contact_tag))

    def __get_description(self, parent: BeautifulSoup) -> str:
        description = ''
        child = self.__get_child_tag(parent)
        while child.name != 'h2':
            if child.name == 'ul':
                for li in child.find_all('li'):
                    description += f'- {li.text}\n'
                description += '\n'
            else:
                description += f'{child.text}\n\n'
            child = self.__get_child_tag(child)
        return description.strip()

    def __get_requirements(self, parent: BeautifulSoup) -> List:
        requirements = []
        child = self.__get_child_tag(parent)
        while child.name != 'h2':
            if child.name == 'p':
                requirements.append(child.text)
            elif child.name == 'ul':
                requirements += list(map(lambda x: f'- {x}', self.__strip_list(child.text.split('\n'))))
            child = self.__get_child_tag(child)
        return requirements

    def __get_about(self, parent: BeautifulSoup) -> List:
        about = []
        child = self.__get_child_tag(parent)
        while child.name != 'h2':
            if child.name == 'ul':
                about.append(self.__strip_list(child.text.split('\n')))
            else:
                about.append(child.text)
            child = self.__get_child_tag(child)
        return about

    def __get_contact_info(self, parent: BeautifulSoup) -> List:
        child = self.__get_child_tag(parent)
        while child.name != 'ul':
            child = self.__get_child_tag(child)
        ul = self.__strip_list(child.text.split('\n'))
        fields = list(map(lambda x: x.split(':', 1), ul))

        contact, email, website = None, None, None
        for field in fields:
            name, value = field[0].lower(), field[1].strip()
            if name == 'contact':
                contact = value
            elif 'e-mail' in name:
                email = value
            elif 'web' in name:
                website = value

        return {'contact': contact, 'email': email, 'website': website}

    def __get_child_tag(self, parent: BeautifulSoup) -> str:
        child = parent.next_sibling
        while not isinstance(child, Tag):
            child = child.next_sibling
        return child

    def __strip_list(self, elements: List) -> List:
        return list(map(self.__strip, filter(self.__strip, elements)))

    def __strip(self, x: str) -> str:
        return x.strip()
