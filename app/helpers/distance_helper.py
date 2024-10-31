
import math

from helpers import R_FEET
from models import Analysis

# Calculates the distance along the longitude meridian (east-west) (Y-axis) between two points 
def calculate_longtitude_distance(latitude, longitude1, longitude2) -> float:
    delta_longitude = longitude2 - longitude1
    distance = delta_longitude * math.cos(math.radians(latitude)) * math.pi / 180 * R_FEET
    return int("{:.0f}".format(round(distance)))

# Calculates the distance along the latitude meridian (north-south) (X-axis) between two points 
def calculate_latitude_distance(latitude1, latitude2) -> float:
    delta_latitude = latitude2 - latitude1
    distance = delta_latitude * math.pi / 180 * R_FEET
    return int("{:.0f}".format(round(distance)))

# Deprecated
# Calculates the distance along the longitude axis (east-west) (Y-axis) between two points 
def calculate_east_west_distance(lat, lon1, lon2) -> tuple[float, str]:
    delta_lon = lon2 - lon1
    distance = delta_lon * math.cos(math.radians(lat)) * math.pi / 180 * R_FEET
    if delta_lon > 0:
        direction = "E"
    else:
        direction = "W"
    return int("{:.0f}".format(round(distance))), direction

# Deprecated
# Calculates the distance along the latitude (north-sout) (X-axis) between two points 
def calculate_north_south_distance(lat1, lat2) -> tuple[float, str]:
    delta_lat = lat2 - lat1
    distance = delta_lat * math.pi / 180 * R_FEET
    if delta_lat > 0:
        direction = "N"
    else:
        direction = "S"
    return int("{:.0f}".format(round(distance))), direction

def average_distance(start, mid, end):
    distance = (start + mid + end) / 3
    return int("{:.0f}".format(round(distance)))

def average_abstolute_distance(start, mid, end):
    distance = (abs(start) + abs(mid) + abs(end)) / 3
    return int("{:.0f}".format(round(distance)))

