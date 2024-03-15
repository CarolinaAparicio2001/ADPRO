from geopy.distance import geodesic

def distance_geo(latitude_source, longitude_source, latitude_destination, longitude_destination):
    """
    Calculates the geodesic distance in kilometers between two geographical points.

    Args:
    - latitude_source (float): Latitude of the source point.
    - longitude_source (float): Longitude of the source point.
    - latitude_destination (float): Latitude of the destination point.
    - longitude_destination (float): Longitude of the destination point.

    Returns:
    - float: Distance between the two points in kilometers. Returns 0 in case of error.
    """
    
    try:
        geoval = geodesic((latitude_source, longitude_source), (latitude_destination, longitude_destination)).km
    except:
        geoval = 0
    
    return geoval 


