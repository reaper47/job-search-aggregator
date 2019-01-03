import pytest
import job_search.utils.geohelpers as geohelpers

EPSILON = 1e-3


def test_givenANormalAddress_whenRequestingCoordinates_thenReturnTheCorrectCoordinates():
    place = 'Munich, Bavaria, Germany'

    lat, lng = geohelpers.get_lat_lng(place)

    lat_expected, lng_expected = 48.1371079, 11.5753822
    assert lat_expected == pytest.approx(lat, EPSILON) and lng_expected == pytest.approx(lng, EPSILON)


def test_givenAnInvalidAddress_whenRequestingLatLng_thenReturnNullCoordinates():
    place = ''

    lat, lng = geohelpers.get_lat_lng(place)

    lat_expected, lng_expected = 0, 0
    assert lat_expected == lat and lng_expected == lng
