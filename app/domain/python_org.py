from typing import List, Dict
import requests
from bs4 import BeautifulSoup, Tag


class PythonOrg:

    def __init__(self):
        self.website = 'https://www.python.org/jobs/'
        self.pagination_class = 'pagination menu'
        self.jobs_class = 'list-recent-jobs list-row-container menu'

    def prepare_soup(self) -> None:
        request = requests.get(self.website)
        job_posting = BeautifulSoup(request.text, features='html.parser')
        self.pages = self._get_pages(job_posting)

    def _get_pages(self, job_posting: BeautifulSoup) -> List[BeautifulSoup]:
        npages = self._get_number_of_pages(job_posting)
        second_page = 2

        soups = [job_posting]
        for i in range(second_page, npages):
            request = requests.get(f"{self.website}?page={i}")
            soups.append(BeautifulSoup(request.text, features='html.parser'))

        return soups

    def _get_number_of_pages(self, job_posting: BeautifulSoup) -> int:
        ul = job_posting.find_all('ul', class_=self.pagination_class)
        pages_raw = [el.text for el in ul][0].split('\n')

        pages = [job_posting]
        for el in pages_raw:
            try:
                pages.append(int(el))
            except ValueError:
                pass

        return len(pages)

    def fetch_jobs(self) -> List[Dict]:
        jobs_scraped = []
        for page in self.pages:
            all_jobs = page.find_all('ol', class_=self.jobs_class)[0].find_all('li')

            for job in all_jobs:
                link = job.find('span', class_='listing-company-name').find('a')['href']
                job_request = requests.get(f'https://www.python.org{link}')
                job_description = BeautifulSoup(job_request.text, features='html.parser')
                job_text = job_description.find('article', class_='text')

                jobs_scraped.append(self._scrape_job(job_text))

        return jobs_scraped

    def _scrape_job(self, job: BeautifulSoup) -> Dict:
        info = {}
        listing_company = self._strip_list(job.find('span', 'company-name').text.split('\n'))
        descriptions = job.find('div', class_='job-description').find_all('h2')

        info['title'] = descriptions[0].next_sibling.strip()
        info['company'] = listing_company[1]
        info['location'] = job.find('span', class_='listing-location').text
        info['description'] = self._get_child_tag(descriptions[1]).text
        info['restrictions'] = self._strip_list(self._get_child_tag(descriptions[2]).text.split('\n'))
        info['requirements'] = self._get_requirements(descriptions[3])
        info['about'] = self._get_about(descriptions[4])
        info['contact_info'] = self._get_contact_info(descriptions[5])

        print('\n\n')
        print(info)
        return info

    def _get_requirements(self, parent: BeautifulSoup) -> List:
        requirements = []

        child = self._get_child_tag(parent)
        while child.name == 'p':
            requirements.append(child.text)
            child = self._get_child_tag(child)

        while child.name == 'ul':
            requirements += self._strip_list(child.text.split('\n'))
            child = self._get_child_tag(child)

        return requirements

    def _get_about(self, parent: BeautifulSoup) -> List:
        about = []

        child = self._get_child_tag(parent)
        while child.name == 'p':
            about.append(child.text)
            child = self._get_child_tag(child)

        return about

    def _get_contact_info(self, parent: BeautifulSoup) -> List:
        child = self._get_child_tag(parent)
        while child.name != 'ul':
            child = self._get_child_tag(child)
        ul = self._strip_list(child.text.split('\n'))

        info = {}
        bits = list(map(lambda x: x.split(':'), ul))
        contact_idx = [i for i, s in enumerate(bits) if s[0] == 'Contact']
        email_idx = [i for i, s in enumerate(bits) if 'E-mail' in s[0]]
        website_idx = [i for i, s in enumerate(bits) if 'Web' in s[0]]

        info['contact'] = '' if not contact_idx else ul[contact_idx[0]].split(':')[1].strip()
        info['email'] = '' if not email_idx else ul[email_idx[0]].split(':')[1].strip()
        info['website'] = '' if not website_idx else ul[website_idx[0]].split(':', 1)[1].strip()
        return info

    def _get_child_tag(self, parent: BeautifulSoup) -> str:
        child = parent.next_sibling
        while not isinstance(child, Tag):
            child = child.next_sibling
        return child

    def _strip_list(self, elements: List) -> List:
        return list(map(lambda x: x.strip(), filter(lambda x: x.strip(), elements)))
