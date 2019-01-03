from job_search.domain.jobs.value_objects.simple_objects import LocationInfo

A_CITY = 'Munich'
A_STATE = 'Bavaria'
A_COUNTRY = 'Germany'


def test_givenALocationInfoWithNoMissingData_whenPrintingTheObject_thenFormatAsCityStateCountry():
    location_info = LocationInfo(city=A_CITY, state=A_STATE, country=A_COUNTRY, lat=0, lng=0)

    location_formatted = str(location_info)

    location_expected = f'{A_CITY}, {A_STATE}, {A_COUNTRY}'
    assert location_expected == location_formatted


def test_givenALocationInfoWithoutAState_whenPrintingTheObject_thenFormatAsCityCountry():
    location_info = LocationInfo(city=A_CITY, state=None, country=A_COUNTRY, lat=0, lng=0)

    location_formatted = str(location_info)

    location_expected = f'{A_CITY}, {A_COUNTRY}'
    assert location_expected == location_formatted
