import urllib, re, sqlite3
from bs4 import BeautifulSoup

#Create a database and a table Houses
conn = sqlite3.connect("daftinfo.sqlite")
cur = conn.cursor()
cur.execute('''
DROP TABLE IF EXISTS Houses''')
cur.execute('''
CREATE TABLE Houses (
id INTEGER PRIMARY KEY NOT NULL UNIQUE,
price TEXT,
address TEXT,
link TEXT,
image TEXT,
geodata TEXT)''')

#Extract data from daft, clear it and insert into database
url = "http://www.daft.ie/dublin-city/residential-property-for-rent/booterstown,dun-laoghaire,monkstown,sandymount/?s%5Bmxp%5D=1850&s%5Badvanced%5D=1&rental_tab_name=advanced-sf&searchSource=rental"
html_of_search = urllib.request.urlopen(url).read()
# print(type(html_of_search))
soup_of_search = BeautifulSoup(html_of_search,"lxml")

boxes = soup_of_search.find_all('div', "box")
#if len(boxes) > 0:

for box in boxes:
    # print(type(box))
    #print(box)
    ad_a = box.find("a")
    address_full = ad_a.text
    add = address_full.split("-")
    address = add[0].strip()
    #print(address)
    url = ("http://www.daft.ie"+ad_a.get("href"))
    #
    # print(url)
    get_image = box.find("img")
    image =  get_image.get("data-original")
    price = box.find("strong", "price").text
    #print(address, url, image, price)
    cur.execute("""INSERT INTO Houses (price, address, link, image) VALUES (?,?,?,?)""", (price, address, url, image))
    conn.commit()
#(price, address, url, image))

#Use Google API for location
serviceurl = "http://maps.googleapis.com/maps/api/geocode/json?"
scontext = None
address = "31 Willowfield, Sandymount, Dublin 4"
url = serviceurl + urllib.parse.urlencode({"sensor": "false", "address": address})
print('Retrieving', url)
uh = urllib.request.urlopen(url, context=scontext)
data = uh.read()
print(data)
#print('Retrieved', len(data), 'characters')
