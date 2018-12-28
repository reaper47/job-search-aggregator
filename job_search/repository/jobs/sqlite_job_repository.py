from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from job_search.domain.jobs.job_repository import JobRepository
import job_search.repository.jobs.entities.job_entity as entities
from job_search.repository.jobs.job_assembler import JobAssembler
from job_search.repository.jobs.job_entity_factory import JobEntityFactory
from config import Config


class SQLiteJobRepository(JobRepository):

    def __init__(self):
        engine = create_engine(Config.SQLITE_DATABASE_URI, echo=Config.SQLALCHEMY_ECHO)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.entity_factory = JobEntityFactory(self)
        self.assembler = JobAssembler()

    def persist(self, job):
        job_entity = self.entity_factory.create_job_entity(job)
        self.session.add(job_entity)
        self.session.commit()

    def load(self):
        pass

    def find_company(self, company):
        return self.session.query(entities.CompanyEntity).filter_by(name=company).first()

    def find_location(self, location):
        city_entity = self.find_city(location.city)
        state_entity = self.find_state(location.state)
        country_entity = self.find_country(location.country)

        try:
            return (self.session.query(entities.LocationEntity)
                                .filter_by(city_id=city_entity.id,
                                           state_id=state_entity.id,
                                           country_id=country_entity.id)
                                .first())
        except AttributeError:
            return None

    def find_city(self, city):
        return self.session.query(entities.CityEntity).filter_by(name=city).first()

    def find_state(self, state):
        return self.session.query(entities.StateEntity).filter_by(name=state).first()

    def find_country(self, country):
        return self.session.query(entities.CountryEntity).filter_by(name=country).first()

    def find_contact_info(self, info):
        name_entity = self.find_contact_name(info.contact)
        email_entity = self.find_contact_email(info.email)
        website_entity = self.find_contact_website(info.website)

        try:
            return (self.session.query(entities.ContactInfoEntity)
                                .filter_by(contact_id=name_entity.id,
                                           email_id=email_entity.id,
                                           website_id=website_entity.id)
                                .first())
        except AttributeError:
            return None

    def find_contact_name(self, name):
        return self.session.query(entities.ContactNameEntity).filter_by(name=name).first()

    def find_contact_email(self, email):
        return self.session.query(entities.ContactEmailEntity).filter_by(name=email).first()

    def find_contact_website(self, website):
        return self.session.query(entities.ContactWebsiteEntity).filter_by(name=website).first()

    def find_source(self, source):
        return self.session.query(entities.SourceEntity).filter_by(name=source).first()
