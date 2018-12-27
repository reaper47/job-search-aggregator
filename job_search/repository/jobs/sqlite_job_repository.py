from job_search.domain.jobs.job_repository import JobRepository


class SQLiteJobRepository(JobRepository):

    def __init__(self):
        pass

    def persist(self, job):
        pass

    def load(self):
        pass

    def find_company(self, company):
        pass

    def find_country(self, country):
        pass

    def find_source(self, country):
        pass
