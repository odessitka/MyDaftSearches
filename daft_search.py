import urllib, re, sqlite3, googlemaps
from bs4 import BeautifulSoup
import dbhelpers
import maps
import webbrowser

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


import os

db = sqlite3.connect("daftinfo.sqlite")
cur = db.cursor()
cur.execute("""SELECT time_walk_to_ov, address, price, link FROM Houses ORDER BY time_walk_to_ov""")
tables = cur.fetchall()
#print(tables)

    #print(table)
    #print(type(table))
    # print(table[0])
    # print(table[1])
db.commit()
db.close()

dir_path = os.path.dirname(os.path.realpath(__file__))

f = open(dir_path + '\\report.html', 'w')

message = """<html>
<head></head>
<body>
<table border = "1">
<tr><th>Time</th><th>Address</th><th>Price</th><th>Link</th></tr>"""
for table in tables:
    message += "<tr><td>" + str(table[0]) + "</td><td>" + table[1] + "</td><td>" + table[2] + "</td><td>" + table[3] + "</td></tr>"

message += """</table>
</body>
</html>"""

f.write(message)
f.close()

filename = dir_path + '\\report.html'
webbrowser.open_new_tab(filename)

