from job_search.application.job_factory import JobFactory
from job_search.domain.jobs.job_repository import JobRepository


class JobScrapingService:

    def __init__(self, repository: JobRepository, job_factory: JobFactory):
        self.repository = repository
        self.job_factory = job_factory

    def scrape(self, source) -> None:
        pass
