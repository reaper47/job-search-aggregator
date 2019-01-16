import abc
from typing import List
from job_search.domain.jobs.value_objects.simple_objects import Job


class JobSource(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def prepare_soup(self) -> None:
        raise NotImplementedError('prepare_soup is not implemented')

    @abc.abstractmethod
    def fetch_jobs(self) -> List[Job]:
        raise NotImplementedError('fetch_jobs is not implemented')
