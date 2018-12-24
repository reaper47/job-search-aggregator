import abc
from job_search.domain.jobs.value_objects.job_type import JobInfoPython


class JobRepository(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def persist(self, job: JobInfoPython) -> None:
        raise NotImplementedError('persist is not implemented')
