from sqlalchemy import create_engine, exc, desc
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
        try:
            self.session.add(job_entity)
            self.session.commit()
        except exc.IntegrityError:
            self.session.rollback()
            print(f"Job '{job_entity.id}' already exists in the database.")

    def load(self, job_id):
        try:
            job_found = (self.session.query(entities.JobEntity)
                                     .filter_by(id=job_id)
                                     .first())
            return self.assembler.to_domain_object(job_found)
        except AttributeError:
            return None

    def load_all_jobs(self):
        all_jobs = (self.session.query(entities.JobEntity)
                                .order_by(desc(entities.JobEntity.id))
                                .all())
        return [self.assembler.to_domain_object(x) for x in all_jobs]

    def find_company(self, company):
        return self.session.query(entities.CompanyEntity).filter_by(name=company).first()

    def find_location(self, location):
        try:
            city_entity = self.find_city(location.city)
            state_entity = self.find_state(location.state)
            country_entity = self.find_country(location.country)
            location_entity = (self.session.query(entities.LocationEntity)
                                           .filter_by(city_id=city_entity.id,
                                                      state_id=state_entity.id,
                                                      country_id=country_entity.id)
                                           .first())
            return location_entity
        except AttributeError:
            return None

    def find_city(self, city):
        return self.session.query(entities.CityEntity).filter_by(name=city).first()

    def find_state(self, state):
        return self.session.query(entities.StateEntity).filter_by(name=state).first()

    def find_country(self, country):
        return self.session.query(entities.CountryEntity).filter_by(name=country).first()

    def find_contact_info(self, info):
        try:
            name_entity = self.find_contact_name(info.contact)
            email_entity = self.find_contact_email(info.email)
            website_entity = self.find_contact_website(info.website)
            contact_info_entity = (self.session.query(entities.ContactInfoEntity)
                                               .filter_by(contact_id=name_entity.id,
                                                          email_id=email_entity.id,
                                                          website_id=website_entity.id)
                                               .first())
            return contact_info_entity
        except AttributeError:
            return None

    def find_contact_name(self, name):
        return self.session.query(entities.ContactNameEntity).filter_by(name=name).first()

    def find_contact_email(self, email):
        return self.session.query(entities.ContactEmailEntity).filter_by(name=email).first()

    def find_contact_website(self, website):
        return self.session.query(entities.ContactWebsiteEntity).filter_by(name=website).first()

    def find_restrictions(self, restrictions):
        found, not_found = [], []
        for name in restrictions:
            name_entity = (self.session.query(entities.RestrictionNameEntity)
                                       .filter_by(name=name)
                                       .first())
            if name_entity is None:
                not_found.append(name)
            else:
                restriction_entity = (self.session.query(entities.RestrictionEntity)
                                          .filter_by(name_id=name_entity.id)
                                          .first())
                found.append(restriction_entity)

        return {'found': found, 'not_found': not_found}

    def find_requirements(self, requirements):
        found, not_found = [], []
        for name in requirements:
            name_entity = (self.session.query(entities.RequirementNameEntity)
                                       .filter_by(name=name)
                                       .first())

            if name_entity is None:
                not_found.append(name)
            else:
                requirement_entity = (self.session.query(entities.RequirementEntity)
                                                  .filter_by(name_id=name_entity.id)
                                                  .first())
                found.append(requirement_entity)

        return {'found': found, 'not_found': not_found}

    def find_source(self, source):
        return self.session.query(entities.SourceEntity).filter_by(name=source).first()
