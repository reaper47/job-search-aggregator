from job_search.repository.jobs.sqlite_job_repository import SQLiteJobRepository
from job_search.domain.jobs.python_org import PythonOrg
from job_search.application.services.jobs.job_factory import JobFactory
from job_search.application.services.jobs.job_service import JobService


service = JobService(JobFactory(), SQLiteJobRepository())
service.scrape_jobs(PythonOrg())
