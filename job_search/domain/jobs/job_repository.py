import abc
from job_search.domain.jobs.value_objects.job_type import JobInfoPython
import job_search.repository.jobs.entities.job_entity as entities


class JobRepository(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def persist(self, job: JobInfoPython) -> None:
        raise NotImplementedError('persist is not implemented')

    def load(self):
        raise NotImplementedError('load is not implemented')

    @abc.abstractmethod
    def find_company(self, company: str) -> entities.CompanyEntity:
        raise NotImplementedError('find_company is not implemented')

    @abc.abstractmethod
    def find_country(self, country: str) -> entities.CountryEntity:
        raise NotImplementedError('find_country is not implemented')

    @abc.abstractmethod
    def find_source(self, country: str) -> entities.SourceEntity:
        raise NotImplementedError('find_source is not implemented')
