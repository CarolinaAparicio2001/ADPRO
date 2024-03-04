from geopy.distance import geodesic

def distance_geo(latitude_source, longitude_source, latitude_destination, longitude_destination):
    try:
        geoval = geodesic((latitude_source, longitude_source), (latitude_destination, longitude_destination)).km
    except:
        geoval = 0
    
    return geoval 


