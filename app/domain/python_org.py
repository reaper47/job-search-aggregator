import requests
from bs4 import BeautifulSoup


class PythonOrg:

    def __init__(self):
        self.website = 'https://www.python.org/jobs/'
        self.pagination_class = 'pagination menu'

    def prepare_soup(self):
        request = requests.get(self.website)
        job_posting = BeautifulSoup(request.text, features='html.parser')
        self.pages = self.get_pages(job_posting)
        
    def get_pages(self, job_posting):
        npages = self.get_number_of_pages(job_posting)
        print(npages)
        second_page = 2
        
        soups = []
        for i in range(second_page, npages+1):
            request = requests.get(f"{self.website}?page={i}")
            soups.append(BeautifulSoup(request.text, features='html.parser'))
        
        return soups

    def get_number_of_pages(self, job_posting):
        ul = job_posting.find_all('ul', class_=self.pagination_class)
        pages_raw = [el.text for el in ul][0].split('\n')

        pages = [job_posting]
        for el in pages_raw:
            try:
                pages.append(int(el))
            except ValueError:
                pass
        print(pages)
        return len(pages)

    def fetch_jobs(self):
        pass
