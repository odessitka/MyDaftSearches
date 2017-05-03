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


class DetailsHouse:
    def __init__(self, box):
        ad_a = box.find("a")
        address_full = ad_a.text
        add = address_full.split("-")
        self.__address = add[0].strip()
        self.__url = ('http://www.daft.ie' + ad_a.get("href"))
        get_image = box.find("img")
        self.__image = get_image.get("data-original")
        self.__price = box.find("strong", "price").text

    @property
    def address(self):
        return self.__address

    @property
    def url(self):
        return self.__url

    @property
    def image(self):
        return self.__image

    @property
    def price(self):
        return self.__price
