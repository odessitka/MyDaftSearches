import urllib, re, sqlite3, googlemaps
from bs4 import BeautifulSoup
import dbhelpers
import maps


#Create a database and a table Houses
dbhelpers.initialize_db()

#Extract data from daft, clear it and insert into database
url = "http://www.daft.ie/dublin-city/residential-property-for-rent/booterstown,dun-laoghaire,monkstown,sandymount/?s%5Bmxp%5D=1850&s%5Badvanced%5D=1&rental_tab_name=advanced-sf&searchSource=rental"
html_of_search = urllib.request.urlopen(url).read()
# print(type(html_of_search))
soup_of_search = BeautifulSoup(html_of_search,"lxml")

boxes = soup_of_search.find_all('div', "box")
#if len(boxes) > 0:

for box in boxes:
    ad_a = box.find("a")
    address_full = ad_a.text
    add = address_full.split("-")
    address = add[0].strip()
    url = ('http://www.daft.ie' + ad_a.get("href"))
    get_image = box.find("img")
    image =  get_image.get("data-original")
    price = box.find("strong", "price").text

    dbhelpers.insert_house(price, address, url, image)

addresses = dbhelpers.get_addresses()

for (address, id) in addresses:
    matrix = maps.CommuteMatrix(address, "oneview, blackrock")
    dbhelpers.update_house(id, matrix.distance, matrix.duration)

