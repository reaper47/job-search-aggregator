from job_search.repository.jobs.sqlite_job_repository import SQLiteJobRepository
from job_search.domain.jobs.sources.python_org import PythonOrg
from job_search.domain.jobs.value_objects.job_type import JobTypeSource
from job_search.application.services.jobs.job_factory import JobFactory
from job_search.application.services.scraper.scraping_service import JobScrapingService


service = JobScrapingService(JobFactory(), SQLiteJobRepository())
service.scrape_jobs(PythonOrg(), JobTypeSource.PYTHON_ORG)
