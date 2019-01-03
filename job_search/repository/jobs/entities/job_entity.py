from pathlib import Path
from sqlalchemy import create_engine, ForeignKey, Column
from sqlalchemy import Integer, Float, String, Boolean, PickleType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

JOB_TABLE = 'job'
COMPANY_TABLE = 'company'
LOCATION_TABLE = 'location'
CONTACT_INFO_TABLE = 'contact_info'
CONTACT_NAME_TABLE = 'contact_name'
CONTACT_EMAIL_TABLE = 'contact_email'
CONTACT_WEBSITE_TABLE = 'contact_website'
SOURCE_TABLE = 'source'
CITY_TABLE = 'city'
STATE_TABLE = 'state'
COUNTRY_TABLE = 'country'
REQUIREMENTS_TABLE = 'requirements'
REQUIREMENT_TABLE = 'requirement'
REQUIREMENT_NAME_TABLE = 'requirement_name'
RESTRICTIONS_TABLE = 'restrictions'
RESTRICTION_TABLE = 'restriction'
RESTRICTION_NAME_TABLE = 'restriction_name'

Base = declarative_base()


class JobEntity(Base):
    __tablename__ = JOB_TABLE

    id = Column(String, autoincrement=False, nullable=False, primary_key=True)
    title = Column(String)
    description = Column(String)
    about = Column(PickleType)

    company_id = Column(Integer, ForeignKey(f'{COMPANY_TABLE}.id'), nullable=False)
    company_entity = relationship('CompanyEntity', backref='job_company', uselist=False)

    location_id = Column(Integer, ForeignKey(f'{LOCATION_TABLE}.id'), nullable=False)
    location_entity = relationship('LocationEntity', backref='job_loc', uselist=False)

    contact_info_id = Column(Integer, ForeignKey(f'{CONTACT_INFO_TABLE}.id'))
    contact_info_entity = relationship('ContactInfoEntity', backref='job_contact', uselist=False)

    restrictions_entity = relationship('RestrictionsEntity', backref='job_restriction', uselist=False)
    requirements_entity = relationship('RequirementsEntity', backref='job_requirement', uselist=False)

    source_id = Column(Integer, ForeignKey(f'{SOURCE_TABLE}.id'), nullable=False)
    source_entity = relationship('SourceEntity', backref='job_src', uselist=False)

    pinned = Column(Boolean, default=False)


class CompanyEntity(Base):
    __tablename__ = COMPANY_TABLE

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)


class LocationEntity(Base):
    __tablename__ = LOCATION_TABLE

    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey(f'{CITY_TABLE}.id'), nullable=False)
    city_entity = relationship('CityEntity', backref='loc_city', uselist=False)

    state_id = Column(Integer, ForeignKey(f'{STATE_TABLE}.id'), nullable=True)
    state_entity = relationship('StateEntity', backref='loc_state', uselist=False)

    country_id = Column(Integer, ForeignKey(f'{COUNTRY_TABLE}.id'), nullable=False)
    country_entity = relationship('CountryEntity', backref='loc_country', uselist=False)

    lat = Column(Float(precision=7), nullable=False)
    lng = Column(Float(precision=7), nullable=False)


class CityEntity(Base):
    __tablename__ = CITY_TABLE

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class StateEntity(Base):
    __tablename__ = STATE_TABLE

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)


class CountryEntity(Base):
    __tablename__ = COUNTRY_TABLE

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)


class RestrictionsEntity(Base):
    __tablename__ = RESTRICTIONS_TABLE

    id = Column(Integer, primary_key=True)
    restriction_entities = relationship('RestrictionEntity', backref='restrictions_name', lazy=True)
    job_id = Column(Integer, ForeignKey(f'{JOB_TABLE}.id'))


class RestrictionEntity(Base):
    __tablename__ = RESTRICTION_TABLE

    id = Column(Integer, primary_key=True)
    name_id = Column(Integer, ForeignKey(f'{RESTRICTION_NAME_TABLE}.id'))
    name_entity = relationship('RestrictionNameEntity', backref='restriction_name', uselist=False)

    restriction_id = Column(Integer, ForeignKey(f'{RESTRICTIONS_TABLE}.id'))


class RestrictionNameEntity(Base):
    __tablename__ = RESTRICTION_NAME_TABLE

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class RequirementsEntity(Base):
    __tablename__ = REQUIREMENTS_TABLE

    id = Column(Integer, primary_key=True)
    requirement_entities = relationship('RequirementEntity', backref='requirements_name', lazy=True)
    job_id = Column(Integer, ForeignKey(f'{JOB_TABLE}.id'))


class RequirementEntity(Base):
    __tablename__ = REQUIREMENT_TABLE

    id = Column(Integer, primary_key=True)
    name_id = Column(Integer, ForeignKey(f'{REQUIREMENT_NAME_TABLE}.id'))
    name_entity = relationship('RequirementNameEntity', backref='requirement_name', uselist=False)

    requirement_id = Column(Integer, ForeignKey(f'{REQUIREMENTS_TABLE}.id'))


class RequirementNameEntity(Base):
    __tablename__ = REQUIREMENT_NAME_TABLE

    id = Column(Integer, primary_key=True)
    name = Column(String)


class ContactInfoEntity(Base):
    __tablename__ = CONTACT_INFO_TABLE

    id = Column(Integer, primary_key=True)
    contact_id = Column(Integer, ForeignKey(f'{CONTACT_NAME_TABLE}.id'))
    name_entity = relationship('ContactNameEntity', backref='contact_name', uselist=False)

    email_id = Column(Integer, ForeignKey(f'{CONTACT_EMAIL_TABLE}.id'))
    email_entity = relationship('ContactEmailEntity', backref='contact_email', uselist=False)

    website_id = Column(Integer, ForeignKey(f'{CONTACT_WEBSITE_TABLE}.id'))
    website_entity = relationship('ContactWebsiteEntity', backref='contact_website', uselist=False)


class ContactNameEntity(Base):
    __tablename__ = CONTACT_NAME_TABLE

    id = Column(Integer, primary_key=True)
    name = Column(String)


class ContactEmailEntity(Base):
    __tablename__ = CONTACT_EMAIL_TABLE

    id = Column(Integer, primary_key=True)
    name = Column(String)


class ContactWebsiteEntity(Base):
    __tablename__ = CONTACT_WEBSITE_TABLE

    id = Column(Integer, primary_key=True)
    name = Column(String)


class SourceEntity(Base):
    __tablename__ = SOURCE_TABLE

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)


if __name__ == '__main__':
    import os
    db_dir = f'{Path(__file__).parent}/../../database/'
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    engine = create_engine(f'sqlite:///{db_dir}/app.db', echo=True)
    Base.metadata.create_all(engine)
