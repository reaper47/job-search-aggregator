import abc
from job_search.domain.jobs.value_objects.job_type import JobInfo
from job_search.domain.jobs.value_objects.simple_objects import LocationInfo
import job_search.repository.jobs.entities.job_entity as entities


class JobRepository(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def persist(self, job: JobInfo) -> None:
        raise NotImplementedError('persist is not implemented')

    @abc.abstractmethod
    def load(self) -> JobInfo:
        raise NotImplementedError('load is not implemented')

    @abc.abstractmethod
    def find_company(self, company: str) -> entities.CompanyEntity:
        raise NotImplementedError('find_company is not implemented')

    @abc.abstractmethod
    def find_location(self, location: LocationInfo) -> entities.LocationEntity:
        raise NotImplementedError('find_location is not implemented')

    @abc.abstractmethod
    def find_city(self, city: str) -> entities.CityEntity:
        raise NotImplementedError('find_city is not implemented')

    @abc.abstractmethod
    def find_state(self, state: str) -> entities.StateEntity:
        raise NotImplementedError('find_state is not implemented')

    @abc.abstractmethod
    def find_country(self, country: str) -> entities.CountryEntity:
        raise NotImplementedError('find_country is not implemented')

    @abc.abstractmethod
    def find_source(self, source: str) -> entities.SourceEntity:
        raise NotImplementedError('find_source is not implemented')
