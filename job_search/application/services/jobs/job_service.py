from typing import List
from job_search.domain.jobs.value_objects.job_type import JobInfo


class JobService:

    def __init__(self, job_repository):
        self.job_repository = job_repository

    def consult_job(self, job_id: str) -> JobInfo:
        return self.job_repository.load(job_id)

    def gather_all_jobs(self) -> List[JobInfo]:
        return self.job_repository.load_all_jobs()
