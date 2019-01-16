from unittest import mock
import pytest
from typing import Dict
from job_search.application.services.jobs.job_factory import JobFactory
from job_search.domain.jobs.value_objects.job_type import ContactInfo, LocationInfo, JobTypeSource
from job_search.domain.jobs.value_objects.simple_objects import Job

A_JOB_TYPE = JobTypeSource.PYTHON_ORG
A_CITY = 'New York City'
A_STATE = 'New York'
A_COUNTRY = 'United States of America'
A_CONTACT = 'Ms. Zuras'
AN_EMAIL = 'zuras@zuru.no'
A_WEBSITE = 'zurulabs.com'
MOCK_GEOHELPERS = 'job_search.application.services.jobs.job_factory.geohelpers'


@pytest.fixture
def a_job() -> Dict:
    return Job(title='Python Guru Expert',
               company='Zuru Labs',
               location=f'{A_CITY}, {A_STATE}, {A_COUNTRY}',
               description='Come program with the gurus at Zuru',
               restrictions=['No telecommuting'],
               requirements=['None'],
               about=['Zuru Labs', 'The best laboratory on Earth'],
               contact_info={'contact': A_CONTACT, 'email': AN_EMAIL, 'website': A_WEBSITE})


@pytest.fixture
def job_factory() -> JobFactory:
    return JobFactory()


@mock.patch(MOCK_GEOHELPERS)
def test_whenCreatingAJob_thenGenerateAnId(mock_geohelpers, a_job, job_factory):
    mock_geohelpers.get_lat_lng.return_value = 0, 0
    job = job_factory.create_job(a_job, A_JOB_TYPE)

    id_expected = 'NYCNYUSOA-ZL-PGE'
    assert id_expected == job.uid


@mock.patch(MOCK_GEOHELPERS)
def test_whenCreatingAJob_thenStoreLocationInAValueObject(mock_geohelpers, a_job, job_factory):
    mock_geohelpers.get_lat_lng.return_value = 0, 0
    job = job_factory.create_job(a_job, A_JOB_TYPE)

    location_info_expected = LocationInfo(city=A_CITY, state=A_STATE, country=A_COUNTRY, lat=0, lng=0)
    assert location_info_expected == job.location


@mock.patch(MOCK_GEOHELPERS)
def test_whenCreatingAJob_thenStoreContactInfoInAValueObject(mock_geohelpers, a_job, job_factory):
    mock_geohelpers.get_lat_lng.return_value = 0, 0
    job = job_factory.create_job(a_job, A_JOB_TYPE)

    contact_info_expected = ContactInfo(contact=A_CONTACT, email=AN_EMAIL, website=A_WEBSITE)
    assert contact_info_expected == job.contact_info
