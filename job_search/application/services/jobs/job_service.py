from typing import List
from job_search.domain.jobs.value_objects.job_type import JobInfo, JobTypeSource


class JobService:

    def __init__(self, job_factory, job_repository):
        self.job_factory = job_factory
        self.job_repository = job_repository

    def scrape_jobs(self, scraper):  # scraper represents the interface for websites
        scraper.prepare_soup()
        jobs = [self.job_factory.create_job(x, JobTypeSource.PYTHON_ORG) for x in scraper.fetch_jobs()]
        [self.job_repository.persist(x) for x in jobs]

    def consult_job(self, job_id: str) -> JobInfo:
        return self.job_repository.load(job_id)

    def gather_all_jobs(self) -> List[JobInfo]:
        return self.job_repository.load_all_jobs()
