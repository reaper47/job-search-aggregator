from job_search.domain.jobs.job_repository import JobRepository
from job_search.domain.jobs.value_objects.job_type import JobInfoPython


class SQLiteJobRepository(JobRepository):

    def __init__(self):
        pass

    def persist(self, job: JobInfoPython) -> None:
        pass
