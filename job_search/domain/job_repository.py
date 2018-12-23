import abc


class JobRepository(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_jobs(self, job: str, id: int) -> Job:
        pass
