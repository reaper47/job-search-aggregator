import paths
import pytest
from unittest import mock

import helpers.soup_helpers as soup_helpers
from helpers.stubs import RequestsStub
from python_org import PythonOrg

from pathlib import Path

@pytest.fixture
def python_org():
    return PythonOrg()

@mock.patch('python_org.requests')
def test_givenAJobPosting_whenGettingJobPages_thenReturnAllJobPages(mock_requests, python_org):
    a_job_posting = soup_helpers.brew_soup(f'{Path(__file__).parent}/samples/job_posting.html')
    mock_requests.get.return_value = RequestsStub('trivial')
    npages_expected = 4

    pages = python_org.get_pages(a_job_posting)

    assert npages_expected == len(pages)
