from typing import Tuple
import geocoder


def get_lat_lng(place: str) -> Tuple[float, float]:
    geo = geocoder.osm(place)
    if geo.ok:
        return geo.lat, geo.lng
    return 0, 0
