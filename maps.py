from datetime import datetime
import time

import googlemaps
# import responses

gmaps = googlemaps.Client(key='AIzaSyCpqCdiOg69YK9-tf2YOPLXRVXGxPuabPk')
origins = ["o'connell bridge, dublin"]
destinations = ["oneview, blackrock"]

matrix = gmaps.distance_matrix(origins, destinations)
print (matrix)
print(type(matrix))
print(matrix['destination_addresses'])
print(type(matrix['destination_addresses']))
print(matrix['destination_addresses'][0])

