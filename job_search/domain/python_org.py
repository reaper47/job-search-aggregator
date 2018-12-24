from typing import List
import requests
from bs4 import BeautifulSoup, Tag
from job_search.domain.job_type import JobInfoPython

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

    def fetch_jobs(self) -> List[JobInfoPython]:
        jobs_scraped = []
        for page in self.pages:
            all_jobs = page.find_all('ol', class_=self.jobs_class)[0].find_all('li')

            for job in all_jobs:
                link = job.find('span', class_='listing-company-name').find('a')['href']
                job_request = requests.get(f'https://www.python.org{link}')
                job_description = BeautifulSoup(job_request.text, features=HTML)
                job_text = job_description.find('article', class_='text')
                jobs_scraped.append(self.__scrape_job(job_text))

        return jobs_scraped

    def __scrape_job(self, job: BeautifulSoup) -> JobInfoPython:
        listing_company = self.__strip_list(job.find('span', 'company-name').text.split('\n'))
        descriptions = job.find('div', class_='job-description').find_all('h2')

        title_tag = descriptions[0]
        descr_tag = descriptions[1]
        restr_tag = descriptions[2]
        reqs_tag = descriptions[3]
        about_tag = descriptions[4]
        contact_tag = descriptions[5]

        return JobInfoPython(title=title_tag.next_sibling.strip(),
                             company=listing_company[1],
                             location=job.find('span', class_='listing-location').text,
                             description=self.__get_child_tag(descr_tag).text,
                             restrictions=self.__strip_list(self.__get_child_tag(restr_tag).text.split('\n')),
                             requirements=self._get_requirements(reqs_tag),
                             about=self.__get_about(about_tag),
                             contact_info=self.__get_contact_info(contact_tag))

    def _get_requirements(self, parent: BeautifulSoup) -> List:
        requirements = []

        child = self.__get_child_tag(parent)
        while child.name == 'p':
            requirements.append(child.text)
            child = self.__get_child_tag(child)

        while child.name == 'ul':
            requirements += self.__strip_list(child.text.split('\n'))
            child = self.__get_child_tag(child)

        return requirements

    def __get_about(self, parent: BeautifulSoup) -> List:
        about = []
        child = self.__get_child_tag(parent)
        while child.name == 'p':
            about.append(child.text)
            child = self.__get_child_tag(child)
        return about

    def __get_contact_info(self, parent: BeautifulSoup) -> List:
        child = self.__get_child_tag(parent)
        while child.name != 'ul':
            child = self.__get_child_tag(child)
        ul = self.__strip_list(child.text.split('\n'))

        info = {}
        bits = list(map(lambda x: x.split(':'), ul))
        contact_idx = [i for i, s in enumerate(bits) if s[0] == 'Contact']
        email_idx = [i for i, s in enumerate(bits) if 'E-mail' in s[0]]
        website_idx = [i for i, s in enumerate(bits) if 'Web' in s[0]]

        fields = [('contact', contact_idx), ('email', email_idx), ('website', website_idx)]
        for field in fields:
            name, idx = field[0], field[1]
            info[name] = '' if not idx else ul[idx[0]].split(':', 1)[1].strip()

        return info

    def __get_child_tag(self, parent: BeautifulSoup) -> str:
        child = parent.next_sibling
        while not isinstance(child, Tag):
            child = child.next_sibling
        return child

    def __strip_list(self, elements: List) -> List:
        return list(map(lambda x: x.strip(), filter(lambda x: x.strip(), elements)))
