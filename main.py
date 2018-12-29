from job_search.repository.jobs.sqlite_job_repository import SQLiteJobRepository
from job_search.domain.jobs.value_objects.simple_objects import ContactInfo, LocationInfo
from job_search.domain.jobs.value_objects.job_type import JobInfoPython
from job_search.domain.jobs.python_org import PythonOrg

repository = SQLiteJobRepository()
py_org = PythonOrg()

print('preparing soup...')
py_org.prepare_soup()

print('fetching jobs...')
jobs = py_org.fetch_jobs()
print('finished fetching jobs...')
for job in jobs:
    print(f'inserting {job}...')
    repository.persist(job)
