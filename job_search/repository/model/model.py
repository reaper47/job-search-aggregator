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


class Job(Base):
    __tablename__ = JOB_TABLE

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    about = Column(PickleType)

    source_id = Column(ForeignKey(f'{SOURCE_TABLE}.id'), nullable=False)
    source = relationship('Source', backref=backref(JOB_TABLE, uselist=False))

    company_id = Column(ForeignKey(f'{COMPANY_TABLE}.id'), nullable=False)
    company = relationship('Company', backref=backref(JOB_TABLE, uselist=False))

    location_id = Column(ForeignKey(f'{LOCATION_TABLE}.id'), nullable=False)
    location = relationship('Location', backref=backref(JOB_TABLE, uselist=False))

    contact_info_id = Column(ForeignKey(f'{CONTACT_INFO_TABLE}.id'))
    contact_info = relationship('ContactInfo', backref=backref(JOB_TABLE, uselist=False))

    restrictions = relationship('Restriction', backref=JOB_TABLE, lazy='dynamic')
    requirements = relationship('Requirement', backref=JOB_TABLE, lazy='dynamic')

    source_id = Column(ForeignKey(f'{SOURCE_TABLE}.id'), nullable=False)
    source = relationship('Source', backref=backref(SOURCE_TABLE, uselist=False))


class Company(Base):
    __tablename__ = COMPANY_TABLE

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)


class Location(Base):
    __tablename__ = LOCATION_TABLE

    id = Column(Integer, primary_key=True)
    city_id = Column(ForeignKey(f'{CITY_TABLE}.id'), nullable=False)
    city = relationship('City', backref=backref(LOCATION_TABLE, uselist=False))

    state_id = Column(ForeignKey(f'{STATE_TABLE}.id'))
    state = relationship('State', backref=backref(LOCATION_TABLE, uselist=False))

    country = Column(ForeignKey(f'{COUNTRY_TABLE}.id'), nullable=False)
    country = relationship('Country', backref=backref(LOCATION_TABLE, uselist=False))


class City(Base):
    __tablename__ = CITY_TABLE

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class State(Base):
    __tablename__ = STATE_TABLE

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Country(Base):
    __tablename__ = COUNTRY_TABLE

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)


class Restriction(Base):
    __tablename__ = RESTRICTIONS_TABLE

    id = Column(Integer, primary_key=True)
    name_id = Column(ForeignKey(f'{RESTRICTION_NAME_TABLE}.id'))
    name = relationship('RestrictionName', backref=backref(RESTRICTIONS_TABLE, uselist=False))

    job_id = Column(Integer, ForeignKey(f'{JOB_TABLE}.id'))


class RestrictionName(Base):
    __tablename__ = RESTRICTION_NAME_TABLE

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Requirement(Base):
    __tablename__ = REQUIREMENTS_TABLE

    id = Column(Integer, primary_key=True)
    name_id = Column(ForeignKey(f'{REQUIREMENT_NAME_TABLE}.id'))
    name = relationship('RequirementName', backref=backref(REQUIREMENTS_TABLE, uselist=False))

    job_id = Column(Integer, ForeignKey(f'{JOB_TABLE}.id'))
    job = relationship('Job', backref=backref(REQUIREMENTS_TABLE, uselist=False))


class RequirementName(Base):
    __tablename__ = REQUIREMENT_NAME_TABLE

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class ContactInfo(Base):
    __tablename__ = CONTACT_INFO_TABLE

    id = Column(Integer, primary_key=True)
    contact = Column(String)
    email = Column(String)
    website = Column(String)


class Source(Base):
    __tablename__ = SOURCE_TABLE

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)


if __name__ == '__main__':
    BASE_DIR = Path(__file__).parent
    engine = create_engine(f'sqlite:///{BASE_DIR}/../app.db', echo=True)
    Base.metadata.create_all(engine)
