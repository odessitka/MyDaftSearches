import googlemaps


def get_distance_duration_matrix(destination_address, origin_address):
    gmaps = googlemaps.Client(key='AIzaSyCpqCdiOg69YK9-tf2YOPLXRVXGxPuabPk')
    matrix = gmaps.distance_matrix(origin_address, destination_address, transit_mode="walking")
    return matrix["rows"][0]["elements"][0]["distance"]["value"], matrix["rows"][0]["elements"][0]["duration"]["value"]




class CommuteMatrix:
    def __init__(self, destination_address, origin_address):
        matrix = get_distance_duration_matrix(destination_address, origin_address)
        self.__distance = matrix[0]
        self.__duration = matrix[1]

    @property
    def distance(self):
        return self.__distance

    @property
    def duration(self):
        return self.__duration
