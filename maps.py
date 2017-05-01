from datetime import datetime
import time

import googlemaps
# import responses
def get_distance(origin_address, destination_address):
    gmaps = googlemaps.Client(key='AIzaSyCpqCdiOg69YK9-tf2YOPLXRVXGxPuabPk')
    # origins = ["o'connell bridge, dublin"]
    # destinations = ["oneview, blackrock"]
    matrix = gmaps.distance_matrix(origin_address, destination_address)
    # print (matrix)
    # print (type(matrix['rows'][0]))
    # print (matrix['rows'][0])
    # #elements = {matrix["rows"][0]}
    # print(matrix["rows"][0]["elements"][0]["distance"]["value"])
    return matrix["rows"][0]["elements"][0]["distance"]["value"]

get_distance("o'connell bridge, dublin","oneview, blackrock")