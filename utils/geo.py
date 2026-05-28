import math
from typing import NamedTuple

class BoundingBox(NamedTuple):
    # This ensures that the data follows a restrict typing
    min_lat: float
    max_lat: float
    min_lon: float
    max_lon: float

def get_bounding_box(lat: float, lon: float, distance_km: float) -> BoundingBox:
    # Computes a bounding box around the location to filter possible nearby records in the database
    # Earth's mean radius
    R = 6371.0

    angular_distance = distance_km / R

    delta_lat = math.degrees(angular_distance)
    min_lat = lat - delta_lat
    max_lat = lat + delta_lat

    lat_rad = math.radians(lat)
    delta_lon = math.degrees(angular_distance / math.cos(lat_rad))
    min_lon = lon - delta_lon
    max_lon = lon + delta_lon

    return BoundingBox(min_lat, max_lat, min_lon, max_lon)

def is_within_radius(lat1: float, lon1: float, lat2: float, lon2: float, max_distance_km) -> bool:
    #  Uses Haversine algorithm to estimate the radius between the location and the max distance (km) to return accurate nearby records.
    # Earth's mean radius
    R = 6371.0

    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (math.sin(delta_phi / 2) ** 2 +
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2)
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return (R * c) <= max_distance_km