import googlemaps


def get_distance(origin_address, destination_address):
    gmaps = googlemaps.Client(key='AIzaSyCpqCdiOg69YK9-tf2YOPLXRVXGxPuabPk')
    matrix = gmaps.distance_matrix(origin_address, destination_address)
    return matrix["rows"][0]["elements"][0]["distance"]["value"]

print (get_distance("o'connell bridge, dublin","oneview, blackrock"))