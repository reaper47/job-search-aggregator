import job_search.utils.geohelpers as geohelpers


def test_givenANormalAddress_whenRequestingCoordinates_thenReturnTheCorrectCoordinates():
    place = 'Munich, Bavaria, Germany'

    lat, lng = geohelpers.get_lat_lng(place)

    lat_expected, lng_expected = 48.1371079, 11.5753822
    assert lat_expected == lat and lng_expected == lng


def test_givenAWeirdAddress_whenRequestingLatLng_thenReturnNullCoordinates():
    place = 'Any, Any, Any'

    lat, lng = geohelpers.get_lat_lng(place)

    lat_expected, lng_expected = 0, 0
    assert lat_expected == lat and lng_expected == lng
