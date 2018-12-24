from pathlib import Path
from sqlalchemy import create_engine, ForeignKey, Column
from sqlalchemy import Integer, String, PickleType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

JOB_TABLE = 'job'
COMPANY_TABLE = 'company'
LOCATION_TABLE = 'location'
CONTACT_INFO_TABLE = 'contact_info'
SOURCE_TABLE = 'source'
CITY_TABLE = 'city'
STATE_TABLE = 'state'
COUNTRY_TABLE = 'country'
REQUIREMENTS_TABLE = 'requirement'
RESTRICTIONS_TABLE = 'restriction'
REQUIREMENT_NAME_TABLE = 'requirement_name'
RESTRICTION_NAME_TABLE = 'restriction_name'

Base = declarative_base()


class JobEntity(Base):
    __tablename__ = JOB_TABLE

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    about = Column(PickleType)

    company_id = Column(ForeignKey(f'{COMPANY_TABLE}.id'), nullable=False)
    company = relationship('CompanyEntity', backref=backref('job_company', uselist=False))

    location_id = Column(ForeignKey(f'{LOCATION_TABLE}.id'), nullable=False)
    location = relationship('LocationEntity', backref=backref('job_loc', uselist=False))

    contact_info_id = Column(ForeignKey(f'{CONTACT_INFO_TABLE}.id'))
    contact_info = relationship('ContactInfoEntity', backref=backref('job_contact', uselist=False))

    restrictions = relationship('RestrictionEntity', backref='job_restriction', lazy='dynamic')
    requirements = relationship('RequirementEntity', backref='job_requirement', lazy='dynamic')

    source_id = Column(ForeignKey(f'{SOURCE_TABLE}.id'), nullable=False)
    source = relationship('SourceEntity', backref=backref('job_src', uselist=False))


class CompanyEntity(Base):
    __tablename__ = COMPANY_TABLE

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)


class LocationEntity(Base):
    __tablename__ = LOCATION_TABLE

    id = Column(Integer, primary_key=True)
    city_id = Column(ForeignKey(f'{CITY_TABLE}.id'), nullable=False)
    city = relationship('CityEntity', backref=backref('loc_city', uselist=False))

    state_id = Column(ForeignKey(f'{STATE_TABLE}.id'))
    state = relationship('StateEntity', backref=backref('loc_state', uselist=False))

    country_id = Column(ForeignKey(f'{COUNTRY_TABLE}.id'), nullable=False)
    country = relationship('CountryEntity', backref=backref('loc_country', uselist=False))


class CityEntity(Base):
    __tablename__ = CITY_TABLE

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class StateEntity(Base):
    __tablename__ = STATE_TABLE

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class CountryEntity(Base):
    __tablename__ = COUNTRY_TABLE

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)


class RestrictionEntity(Base):
    __tablename__ = RESTRICTIONS_TABLE

    id = Column(Integer, primary_key=True)
    name_id = Column(ForeignKey(f'{RESTRICTION_NAME_TABLE}.id'))
    name = relationship('RestrictionNameEntity', backref=backref('restriction_name', uselist=False))

    job_id = Column(Integer, ForeignKey(f'{JOB_TABLE}.id'))


class RestrictionNameEntity(Base):
    __tablename__ = RESTRICTION_NAME_TABLE

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class RequirementEntity(Base):
    __tablename__ = REQUIREMENTS_TABLE

    id = Column(Integer, primary_key=True)
    name_id = Column(ForeignKey(f'{REQUIREMENT_NAME_TABLE}.id'))
    name = relationship('RequirementNameEntity', backref=backref('requirement_name', uselist=False))

    job_id = Column(Integer, ForeignKey(f'{JOB_TABLE}.id'))
    job = relationship('JobEntity', backref=backref('requirement_job', uselist=False))


class RequirementNameEntity(Base):
    __tablename__ = REQUIREMENT_NAME_TABLE

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class ContactInfoEntity(Base):
    __tablename__ = CONTACT_INFO_TABLE

    id = Column(Integer, primary_key=True)
    contact = Column(String)
    email = Column(String)
    website = Column(String)


class SourceEntity(Base):
    __tablename__ = SOURCE_TABLE

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)


if __name__ == '__main__':
    BASE_DIR = Path(__file__).parent
    engine = create_engine(f'sqlite:///{BASE_DIR}/../app.db', echo=True)
    Base.metadata.create_all(engine)
