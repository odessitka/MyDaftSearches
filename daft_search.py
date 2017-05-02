import urllib, re, sqlite3, googlemaps
from bs4 import BeautifulSoup
import dbhelpers
import maps
import webbrowser
import os


def main():
    dbhelpers.initialize_db()
    extract_and_insert()
    calc_distances()
    filename = create_report()
    webbrowser.open_new_tab(filename)


def create_report():
    houses = dbhelpers.get_houses()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    f = open(dir_path + '\\report.html', 'w')
    message = compose_html(houses)
    f.write(message)
    f.close()
    filename = dir_path + '\\report.html'
    return filename


def calc_distances():
    addresses = dbhelpers.get_addresses()
    for (address, id) in addresses:
        matrix = maps.CommuteMatrix(address, "oneview, blackrock")
        dbhelpers.update_house(id, matrix.distance, matrix.duration)


def extract_and_insert():
    # Extract data from daft, clear it and insert into database
    url = "http://www.daft.ie/dublin-city/residential-property-for-rent/booterstown,dun-laoghaire,monkstown,sandymount/?s%5Bmxp%5D=1850&s%5Badvanced%5D=1&rental_tab_name=advanced-sf&searchSource=rental"
    html_of_search = urllib.request.urlopen(url).read()
    # print(type(html_of_search))
    soup_of_search = BeautifulSoup(html_of_search, "lxml")
    boxes = soup_of_search.find_all('div', "box")
    # if len(boxes) > 0:
    for box in boxes:
        ad_a = box.find("a")
        address_full = ad_a.text
        add = address_full.split("-")
        address = add[0].strip()
        url = ('http://www.daft.ie' + ad_a.get("href"))
        get_image = box.find("img")
        image = get_image.get("data-original")
        price = box.find("strong", "price").text
        dbhelpers.insert_house(price, address, url, image)


def compose_html(houses):
    message = """<html>
    <head></head>
    <body>
    <h1> Houses close to Oneview Healthcare </h1>
    <table border="1" width=90%>
    <tr><th>Time</th><th>Address</th><th>Price</th><th>Link</th></tr>"""
    for house in houses:
        message += "<tr><td>" + str(house[0]) + "</td><td>" + house[1] + "</td><td>" + house[2] + "</td><td>" + house[3] + "</td></tr>"
    message += """</table>
    </body>
    </html>"""
    return message


main()