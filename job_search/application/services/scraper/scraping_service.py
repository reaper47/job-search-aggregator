from job_search.application.services.jobs.job_factory import JobFactory
from job_search.domain.jobs.job_repository import JobRepository
from job_search.domain.jobs.job_source import JobSource
from job_search.domain.jobs.value_objects.job_type import JobTypeSource


class JobScrapingService:

    def __init__(self, factory: JobFactory, repository: JobRepository):
        self.factory = factory
        self.repository = repository

    def scrape_jobs(self, scraper: JobSource, source: JobTypeSource):
        scraper.prepare_soup()
        jobs = [self.factory.create_job(x, source) for x in scraper.fetch_jobs()]
        [self.repository.persist(x) for x in jobs]
