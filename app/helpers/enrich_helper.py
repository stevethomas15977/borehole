import math
import requests
import utm
from models import (Analysis, Well)

R_FEET = 6371000 * 3.28084  # Earth radius in feet

def adjust_coordinate(lat, lon, distance_feet, direction):
    distance_radians = distance_feet / R_FEET
    lat_radians = math.radians(lat)
    lon_radians = math.radians(lon)
    
    if direction == "N":
        new_lat_radians = lat_radians + distance_radians
        new_lon_radians = lon_radians
    elif direction == "S":
        new_lat_radians = lat_radians - distance_radians
        new_lon_radians = lon_radians
    elif direction == "E":
        new_lat_radians = lat_radians
        new_lon_radians = lon_radians + distance_radians / math.cos(lat_radians)
    elif direction == "W":
        new_lat_radians = lat_radians
        new_lon_radians = lon_radians - distance_radians / math.cos(lat_radians)
    elif direction == "NE":
        new_lat_radians = lat_radians + distance_radians / math.sqrt(2)
        new_lon_radians = lon_radians + (distance_radians / math.sqrt(2)) / math.cos(lat_radians)
    elif direction == "NW":
        new_lat_radians = lat_radians + distance_radians / math.sqrt(2)
        new_lon_radians = lon_radians - (distance_radians / math.sqrt(2)) / math.cos(lat_radians)
    elif direction == "SE":
        new_lat_radians = lat_radians - distance_radians / math.sqrt(2)
        new_lon_radians = lon_radians + (distance_radians / math.sqrt(2)) / math.cos(lat_radians)
    elif direction == "SW":
        new_lat_radians = lat_radians - distance_radians / math.sqrt(2)
        new_lon_radians = lon_radians - (distance_radians / math.sqrt(2)) / math.cos(lat_radians)
    else:
        raise ValueError(f"Received direction of {direction} but direction must be N, S, E, W, NE, NW, SE, or SW")

    new_lat = math.degrees(new_lat_radians)
    new_lon = math.degrees(new_lon_radians)

    return float(format(new_lat, '.15f')), float(format(new_lon, '.15f'))

def calculate_bearing(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    delta_lon = lon2 - lon1
    x = math.sin(delta_lon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(delta_lon))
    initial_bearing = math.atan2(x, y)
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360
    return compass_bearing

def compass_direction(bearing):
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    idx = round(bearing / 45) % 8
    return directions[idx]

def dominant_direction(bearing):
    directions = ["N", "E", "S", "W"]
    idx = round(bearing / 90) % 4
    return directions[idx]

def latlon_to_utm_feet(lat: float, lon: float) -> tuple[float, float]:

   # Ensure the inputs are floats
    lat = float(lat)
    lon = float(lon)
    
    # Convert latitude and longitude to UTM coordinates using the utm library
    u = utm.from_latlon(lat, lon)
    x, y = u[0], u[1]  # UTM coordinates in meters

    # Convert meters to feet
    x_feet = x * 3.28084
    y_feet = y * 3.28084

    return round(x_feet,2), round(y_feet,2)

def spc_feet_to_latlon(northing=None, 
                       easting=None, 
                       units="usft", 
                       spcZone=None,
                       inDatum=None) -> tuple[float, float]:
    """
    Function to get the source latitude and longitude (srcLat, srcLon)
    by converting State Plane Coordinates (SPC) using the NOAA NCAT API.

    Parameters:
    - spcZone: The 4-digit SPC zone. Texas Central Zone is 4203.
    - northing (Y): The northing value in feet or meters.
    - easting (X): The easting value in feet or meters.
    - units: The units of the input coordinates ('usft' for U.S. survey feet, 'm' for meters, etc.).
    - inDatum: The datum of the input coordinates (e.g., 'NAD27', 'NAD83(2011)').
    - outDatum: The datum for the output coordinates (e.g., 'NAD27', 'NAD83(2011)').

    Returns:
    - A tuple of (srcLat, srcLon) as floats if the API call is successful.
    - None if the request fails.
    """
    
    # Define the base URL for the NOAA NCAT SPC service
    url = "https://geodesy.noaa.gov/api/ncat/spc"

    # Set up the parameters for the API call
    params = {
        "spcZone": spcZone,
        "northing": northing,
        "easting": easting,
        "units": units,
        "inDatum": inDatum,
        "outDatum": inDatum
    }

    # Send the GET request to the API
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        result = response.json()
        # Extract srcLat and srcLon from the JSON response
        src_lat = result.get('srcLat')
        src_lon = result.get('srcLon')
        return src_lat, src_lon
    else:
        print(f"Error: {response.status_code}")
        return None
    
def calculate_3d_distance(x1:float, y1:float, depth1:float, x2:float, y2:float, depth2:float) -> float:
    """
    Calculate the Euclidean distance between two points (x1, y1, z1) and (x2, y2, z2) in 3D space.

    Parameters:
    x1 (float): X coordinate of the first point
    y1 (float): Y coordinate of the first point
    z1 (float): Z coordinate of the first point (depth)
    x2 (float): X coordinate of the second point
    y2 (float): Y coordinate of the second point
    z2 (float): Z coordinate of the second point (depth)

    Returns:
    float: The distance between the two points
    """
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (depth2 - depth1)**2)
    return distance

def create_survey_from_well_data(logger, well: Well) -> Analysis:
    analysis = None
    if well is not None:
        analysis = Analysis()
        # Determine the lateral length and subsurface depth
        if well.lateral_length is not None:
            analysis.lateral_length = math.ceil(well.lateral_length)
        elif well.total_vertical_depth is not None and well.measured_depth is not None:
                analysis.lateral_length = math.ceil(well.measured_depth - well.total_vertical_depth)
        else:
            raise Exception(f"Unable to determine well survey lateral length for well: {well.name}")

        # Determine the subsurface depth
        if well.total_vertical_depth is not None and well.kelly_bushing_elevation is not None:
            analysis.subsurface_depth = math.ceil(well.kelly_bushing_elevation - well.total_vertical_depth)
        elif well.measured_depth is not None and well.lateral_length is not None and well.kelly_bushing_elevation is not None:
            analysis.subsurface_depth = math.ceil(well.kelly_bushing_elevation - well.measured_depth - well.lateral_length)
        
        # Determine the lateral location
        if (well.surface_latitude is not None and well.surface_longitude is not None and 
            well.bottom_hole_latitude is not None and well.bottom_hole_longitude is not None):

            analysis.dominant_direction = dominant_direction(calculate_bearing(well.surface_latitude, 
                                                                                                well.surface_longitude, 
                                                                                                well.bottom_hole_latitude, 
                                                                                                well.bottom_hole_longitude))
            if well.direction is not None:
                analysis.direction = well.direction
            else:
                analysis.direction = compass_direction(calculate_bearing(well.surface_latitude, 
                                                                            well.surface_longitude, 
                                                                            well.bottom_hole_latitude, 
                                                                            well.bottom_hole_longitude))
                    
            analysis.lateral_start_latitude, analysis.lateral_start_longitude = adjust_coordinate(well.bottom_hole_latitude, 
                                                                                                well.bottom_hole_longitude, 
                                                                                                analysis.lateral_length,
                                                                                                analysis.direction)
                
            analysis.lateral_midpoint_latitude, analysis.lateral_midpoint_longitude = adjust_coordinate(well.bottom_hole_latitude, 
                                                                                                        well.bottom_hole_longitude, 
                                                                                                        analysis.lateral_length / 2,
                                                                                                        analysis.direction)
                
            analysis.lateral_end_latitude = well.bottom_hole_latitude
            analysis.lateral_end_longitude = well.bottom_hole_longitude


            analysis.lateral_start_grid_x, analysis.lateral_start_grid_y = latlon_to_utm_feet(analysis.lateral_start_latitude, analysis.lateral_start_longitude)
            analysis.lateral_start_subsurface_depth = analysis.subsurface_depth
            analysis.lateral_midpoint_grid_x, analysis.lateral_midpoint_grid_y = latlon_to_utm_feet(analysis.lateral_midpoint_latitude, analysis.lateral_midpoint_longitude)
            analysis.lateral_midpoint_subsurface_depth = analysis.subsurface_depth
            analysis.lateral_end_grid_x, analysis.lateral_end_grid_y = latlon_to_utm_feet(analysis.lateral_end_latitude, analysis.lateral_end_longitude)
            analysis.lateral_end_subsurface_depth = analysis.subsurface_depth
            
        else:
            logger.warning(f"Unable to determine well survey lateral location for well: {well.name}")
            return None

    return analysis

def create_survey_from_survey_data(logger, surveys) -> Analysis:
    start_index = None 
    analysis = Analysis()
    debug = None
    for index, survey in enumerate(surveys): 
        debug = survey.api
        if survey.inclination > 85:
            start_index = index
            break

    if start_index is not None:
        end_index = len(surveys) - 1
        mid_index = (end_index + start_index) // 2 

        analysis.lateral_start_latitude = surveys[start_index].latitude
        analysis.lateral_start_longitude = surveys[start_index].longitude
        analysis.lateral_midpoint_latitude = surveys[mid_index].latitude
        analysis.lateral_midpoint_longitude = surveys[mid_index].longitude
        analysis.lateral_end_latitude = surveys[end_index].latitude
        analysis.lateral_end_longitude = surveys[end_index].longitude

        analysis.lateral_length = math.ceil(surveys[end_index].md - surveys[start_index].md)

        analysis.dominant_direction = dominant_direction(calculate_bearing(surveys[start_index].latitude, 
                                                                                            surveys[start_index].longitude, 
                                                                                            surveys[end_index].latitude, 
                                                                                            surveys[end_index].longitude))
        analysis.direction = compass_direction(surveys[end_index].azimuth)
        
        analysis.lateral_start_grid_x = surveys[start_index].grid_x
        analysis.lateral_start_grid_y = surveys[start_index].grid_y
        analysis.lateral_start_subsurface_depth = surveys[start_index].subsurface_depth
        
        analysis.lateral_midpoint_grid_x = surveys[mid_index].grid_x
        analysis.lateral_midpoint_grid_y = surveys[mid_index].grid_y
        analysis.lateral_midpoint_subsurface_depth = surveys[mid_index].subsurface_depth

        analysis.lateral_end_grid_x = surveys[end_index].grid_x
        analysis.lateral_end_grid_y = surveys[end_index].grid_y
        analysis.lateral_end_subsurface_depth = surveys[end_index].subsurface_depth

        analysis.subsurface_depth = math.ceil((surveys[mid_index].subsurface_depth + surveys[end_index].subsurface_depth) / 2)
        
    else:
        logger.warning(f"Survey data does not include a station with an inclination of greater than 85 degrees for: {debug}")
        return None
    
    return analysis